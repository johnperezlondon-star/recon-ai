"""
recon_engine.py
───────────────
Core reconciliation engine.
Handles bank, intercompany, and accounts payable reconciliations.
Uses pandas for data processing and fuzzy matching for approximate matches.
"""

import pandas as pd
from difflib import SequenceMatcher


# ─── CONFIGURATION ────────────────────────────────────────────────────────────

MATERIALITY_ABS = 500        # Flag exceptions above this absolute value (£)
MATERIALITY_PCT = 0.01       # Flag exceptions above this % of total (1%)
FUZZY_THRESHOLD = 0.80       # Minimum similarity score for a fuzzy match (0-1)
EXACT_THRESHOLD = 0.001      # Tolerance for exact amount matching (£0.001)


# ─── UTILITY FUNCTIONS ────────────────────────────────────────────────────────

def fuzzy_score(a: str, b: str) -> float:
    """Return similarity score between two strings (0 to 1)."""
    return SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()


def fmt_gbp(value: float) -> str:
    """Format a number as GBP string."""
    prefix = "-£" if value < 0 else "£"
    return f"{prefix}{abs(value):,.2f}"


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file and standardise column names."""
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


# ─── BANK RECONCILIATION ─────────────────────────────────────────────────────

def run_bank_reconciliation(bank_path: str, gl_path: str) -> dict:
    """
    Match bank statement lines against general ledger entries.

    Args:
        bank_path: Path to bank statement CSV
        gl_path:   Path to GL extract CSV

    Returns:
        Dictionary with keys: matched, exceptions, timing, summary_stats
    """
    bank = load_csv(bank_path)
    gl   = load_csv(gl_path)

    # Ensure required columns exist
    # Bank CSV expected: date, description, amount, reference
    # GL CSV expected:   date, description, amount, account_ref

    matched   = []
    exceptions = []
    timing    = []
    gl_used   = set()

    for _, bank_row in bank.iterrows():
        best_match   = None
        best_score   = 0
        best_gl_idx  = None

        for gl_idx, gl_row in gl.iterrows():
            if gl_idx in gl_used:
                continue

            # Amount must match within tolerance
            amount_diff = abs(float(bank_row["amount"]) - float(gl_row["amount"]))
            if amount_diff > EXACT_THRESHOLD:
                continue

            # Score description similarity
            score = fuzzy_score(
                str(bank_row["description"]),
                str(gl_row["description"])
            )

            if score > best_score:
                best_score   = score
                best_match   = gl_row
                best_gl_idx  = gl_idx

        if best_score >= FUZZY_THRESHOLD and best_match is not None:
            # Matched — determine match type
            match_type = "Exact" if best_score >= 0.98 else "Fuzzy"
            confidence = round(best_score * 100, 1)

            matched.append({
                "bank_date":        bank_row["date"],
                "bank_description": bank_row["description"],
                "gl_description":   best_match["description"],
                "amount":           float(bank_row["amount"]),
                "match_type":       match_type,
                "confidence_score": confidence,
            })
            gl_used.add(best_gl_idx)

        elif best_score >= 0.60:
            # Close match — possible timing difference
            timing.append({
                "bank_date":     bank_row["date"],
                "gl_date":       best_match["date"] if best_match is not None else "—",
                "description":   bank_row["description"],
                "amount":        float(bank_row["amount"]),
                "reason":        "Timing difference — close match found in adjacent period",
            })
            if best_gl_idx is not None:
                gl_used.add(best_gl_idx)

        else:
            # Exception — no match found
            exceptions.append({
                "date":        bank_row["date"],
                "description": bank_row["description"],
                "source":      "Bank statement",
                "amount":      float(bank_row["amount"]),
                "type":        classify_exception(bank_row["description"]),
                "action":      "",   # Filled by AI narrative engine
            })

    # GL lines with no match are also exceptions
    for gl_idx, gl_row in gl.iterrows():
        if gl_idx not in gl_used:
            exceptions.append({
                "date":        gl_row["date"],
                "description": gl_row["description"],
                "source":      "General ledger",
                "amount":      float(gl_row["amount"]),
                "type":        "Missing bank entry",
                "action":      "",
            })

    total_lines   = len(bank)
    match_rate    = round(len(matched) / total_lines * 100, 1) if total_lines else 0

    return {
        "matched":      pd.DataFrame(matched),
        "exceptions":   pd.DataFrame(exceptions),
        "timing":       pd.DataFrame(timing),
        "summary_stats": {
            "total_bank_lines":     total_lines,
            "matched_count":        len(matched),
            "exception_count":      len(exceptions),
            "timing_count":         len(timing),
            "match_rate_pct":       match_rate,
            "unreconciled_value":   sum(e["amount"] for e in exceptions),
        },
    }


def classify_exception(description: str) -> str:
    """Classify an exception item based on its description."""
    desc_lower = description.lower()
    if any(kw in desc_lower for kw in ["duplicate", "dup", "repeat"]):
        return "Duplicate"
    if any(kw in desc_lower for kw in ["reversal", "reverse", "rev"]):
        return "Reversal"
    if any(kw in desc_lower for kw in ["charge", "fee", "interest"]):
        return "Bank charge"
    return "Missing entry"


# ─── INTERCOMPANY RECONCILIATION ─────────────────────────────────────────────

def run_intercompany_reconciliation(entity_a_path: str, entity_b_path: str) -> dict:
    """
    Reconcile intercompany balances between two entities.

    Args:
        entity_a_path: CSV of Entity A intercompany transactions
        entity_b_path: CSV of Entity B intercompany transactions

    Returns:
        Dictionary with keys: agreed, disagreements, fx_diffs, summary_stats
    """
    entity_a = load_csv(entity_a_path)
    entity_b = load_csv(entity_b_path)

    # Expected columns: transaction_ref, description, amount, currency, entity

    agreed        = []
    disagreements = []
    fx_diffs      = []
    b_used        = set()

    for _, row_a in entity_a.iterrows():
        matched_b = None

        # Match on transaction reference first (exact)
        ref_matches = entity_b[
            entity_b["transaction_ref"] == row_a["transaction_ref"]
        ]

        if not ref_matches.empty:
            matched_b = ref_matches.iloc[0]
            b_used.add(ref_matches.index[0])

        if matched_b is None:
            # Fallback: fuzzy description match
            for b_idx, row_b in entity_b.iterrows():
                if b_idx in b_used:
                    continue
                if fuzzy_score(row_a["description"], row_b["description"]) > 0.85:
                    matched_b = row_b
                    b_used.add(b_idx)
                    break

        if matched_b is None:
            disagreements.append({
                "ref":         row_a["transaction_ref"],
                "description": row_a["description"],
                "entity_a":    float(row_a["amount"]),
                "entity_b":    0,
                "difference":  float(row_a["amount"]),
                "root_cause":  "Missing entry — not recorded in Entity B",
            })
            continue

        diff = abs(float(row_a["amount"]) - float(matched_b["amount"]))

        if diff < EXACT_THRESHOLD:
            agreed.append({
                "ref":         row_a["transaction_ref"],
                "description": row_a["description"],
                "entity_a":    float(row_a["amount"]),
                "entity_b":    float(matched_b["amount"]),
                "difference":  0,
            })
        elif row_a.get("currency", "GBP") != "GBP" and diff < 500:
            fx_diffs.append({
                "ref":         row_a["transaction_ref"],
                "description": row_a["description"],
                "eur_amount":  row_a.get("eur_amount", "—"),
                "rate_a":      row_a.get("fx_rate", "—"),
                "rate_b":      matched_b.get("fx_rate", "—"),
                "gbp_diff":    round(diff, 2),
            })
        else:
            disagreements.append({
                "ref":         row_a["transaction_ref"],
                "description": row_a["description"],
                "entity_a":    float(row_a["amount"]),
                "entity_b":    float(matched_b["amount"]),
                "difference":  round(diff, 2),
                "root_cause":  classify_ic_difference(diff, row_a, matched_b),
            })

    net_diff = (
        entity_a["amount"].sum() - entity_b["amount"].sum()
        if "amount" in entity_a.columns and "amount" in entity_b.columns
        else 0
    )

    return {
        "agreed":        pd.DataFrame(agreed),
        "disagreements": pd.DataFrame(disagreements),
        "fx_diffs":      pd.DataFrame(fx_diffs),
        "summary_stats": {
            "entity_a_balance":  entity_a["amount"].sum() if "amount" in entity_a.columns else 0,
            "entity_b_balance":  entity_b["amount"].sum() if "amount" in entity_b.columns else 0,
            "agreed_count":      len(agreed),
            "disagreement_count":len(disagreements),
            "fx_diff_count":     len(fx_diffs),
            "net_difference":    round(net_diff, 2),
        },
    }


def classify_ic_difference(diff: float, row_a, row_b) -> str:
    """Classify root cause of intercompany disagreement."""
    if diff > 10000:
        return "Significant amount dispute — escalate to group finance"
    if diff < 2000:
        return "Cut-off difference — check period of recognition"
    return "Posting error — verify invoice copy and re-post"


# ─── ACCOUNTS PAYABLE RECONCILIATION ─────────────────────────────────────────

def run_ap_reconciliation(supplier_path: str, ledger_path: str) -> dict:
    """
    Reconcile supplier statements against the AP ledger.

    Args:
        supplier_path: CSV of supplier statement invoices
        ledger_path:   CSV of AP ledger entries

    Returns:
        Dictionary with keys: matched, missing, duplicates, summary_stats
    """
    supplier = load_csv(supplier_path)
    ledger   = load_csv(ledger_path)

    # Expected columns: invoice_number, supplier, invoice_date, amount

    matched    = []
    missing    = []
    duplicates = []
    ledger_used = set()

    # Detect duplicates in ledger first
    dup_mask = ledger.duplicated(subset=["invoice_number", "amount"], keep=False)
    dup_invoice_numbers = set(ledger[dup_mask]["invoice_number"].tolist())

    for _, sup_row in supplier.iterrows():
        inv_num = str(sup_row["invoice_number"])

        # Check for exact invoice number match in ledger
        ledger_match = ledger[ledger["invoice_number"] == inv_num]

        if not ledger_match.empty:
            gl_row = ledger_match.iloc[0]
            ledger_used.add(ledger_match.index[0])

            amount_diff = abs(float(sup_row["amount"]) - float(gl_row["amount"]))

            if amount_diff < EXACT_THRESHOLD:
                entry = {
                    "invoice_number": inv_num,
                    "supplier":       sup_row["supplier"],
                    "invoice_date":   sup_row["invoice_date"],
                    "amount":         float(sup_row["amount"]),
                    "gl_ref":         gl_row.get("gl_ref", "—"),
                    "status":         "Matched",
                }
                # Flag if this invoice number also appears as a duplicate
                if inv_num in dup_invoice_numbers:
                    duplicates.append({
                        "invoice_number":    inv_num,
                        "supplier":          sup_row["supplier"],
                        "amount":            float(sup_row["amount"]),
                        "original_posting":  gl_row.get("gl_ref", "—"),
                        "duplicate_posting": "See ledger",
                        "risk_level":        "High" if float(sup_row["amount"]) > 5000 else "Medium",
                    })
                matched.append(entry)
            else:
                # Amount mismatch
                missing.append({
                    "invoice_number":  inv_num,
                    "supplier":        sup_row["supplier"],
                    "invoice_date":    sup_row["invoice_date"],
                    "amount":          float(sup_row["amount"]),
                    "days_outstanding": 0,
                    "action":          f"Amount mismatch: supplier £{sup_row['amount']:,.0f} vs ledger £{gl_row['amount']:,.0f} — obtain credit note or correcting entry",
                })
        else:
            # Invoice not in ledger
            missing.append({
                "invoice_number":  inv_num,
                "supplier":        sup_row["supplier"],
                "invoice_date":    sup_row["invoice_date"],
                "amount":          float(sup_row["amount"]),
                "days_outstanding": 0,
                "action":          "",    # Filled by AI
            })

    total        = len(supplier)
    total_value  = supplier["amount"].sum() if "amount" in supplier.columns else 0
    missing_val  = sum(m["amount"] for m in missing)

    return {
        "matched":    pd.DataFrame(matched),
        "missing":    pd.DataFrame(missing),
        "duplicates": pd.DataFrame(duplicates),
        "summary_stats": {
            "total_invoices":    total,
            "total_value":       total_value,
            "matched_count":     len(matched),
            "missing_count":     len(missing),
            "duplicate_count":   len(duplicates),
            "unreconciled_value":missing_val,
        },
    }
