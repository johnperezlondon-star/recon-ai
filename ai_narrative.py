"""
ai_narrative.py
───────────────
GPT-4o integration for generating reconciliation narratives.
Produces three output types:
  1. Exception action list    — what to do with each unmatched item
  2. Sign-off summary         — audit-ready reconciliation narrative
  3. Risk commentary          — highlights material items for management
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL       = "gpt-4o"
TEMPERATURE = 0.3   # Low = consistent, professional output


# ─── BANK RECONCILIATION NARRATIVE ───────────────────────────────────────────

def generate_bank_commentary(
    exceptions_df: pd.DataFrame,
    timing_df: pd.DataFrame,
    stats: dict,
    context: str = ""
) -> str:
    """
    Generate a bank reconciliation sign-off narrative.

    Args:
        exceptions_df:  DataFrame of unmatched items
        timing_df:      DataFrame of timing differences
        stats:          Summary statistics dict from recon_engine
        context:        Optional business context from user

    Returns:
        Professional narrative string ready for audit file
    """
    exc_str    = exceptions_df.to_string(index=False) if not exceptions_df.empty else "No exceptions."
    timing_str = timing_df.to_string(index=False) if not timing_df.empty else "No timing differences."

    prompt = f"""
You are a senior financial controller completing a bank reconciliation sign-off.

Reconciliation statistics:
- Total bank statement lines: {stats['total_bank_lines']}
- Matched: {stats['matched_count']} ({stats['match_rate_pct']}% match rate)
- Exceptions requiring investigation: {stats['exception_count']}
- Timing differences: {stats['timing_count']}
- Total unreconciled value: £{stats['unreconciled_value']:,.2f}

Exceptions:
{exc_str}

Timing differences:
{timing_str}

{f"Additional context: {context}" if context else ""}

Write a formal bank reconciliation sign-off narrative in exactly 3 paragraphs:
1. Overall status and match rate — 2-3 sentences.
2. Key exceptions — describe each material item specifically, including amounts and recommended actions.
3. Timing differences and sign-off recommendation.

Write in formal finance language. Reference specific amounts. Do not use bullet points.
This narrative will be attached to the audit file.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a senior financial controller writing audit documentation."},
            {"role": "user",   "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=700
    )
    return response.choices[0].message.content


def generate_exception_actions(exceptions_df: pd.DataFrame, recon_type: str = "bank") -> pd.DataFrame:
    """
    Generate a specific investigation action for each exception item.

    Sends all exceptions in one API call to keep cost low.
    Returns the DataFrame with an 'action' column populated.

    Args:
        exceptions_df:  DataFrame of exception items
        recon_type:     'bank', 'intercompany', or 'ap'

    Returns:
        DataFrame with 'action' column filled
    """
    if exceptions_df.empty:
        return exceptions_df

    # Convert to minimal JSON for the prompt
    items = exceptions_df[["description", "amount"]].to_dict(orient="records")
    items_str = json.dumps(items, indent=2)

    prompt = f"""
You are a financial controller reviewing {recon_type} reconciliation exceptions.

For each item below, provide a specific, actionable investigation step (max 15 words each).
Respond ONLY with a JSON array in this exact format — no preamble, no markdown:
[
  {{"description": "exact description from input", "action": "specific action here"}},
  ...
]

Items:
{items_str}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a financial controller. Reply only with valid JSON."},
            {"role": "user",   "content": prompt}
        ],
        temperature=0.2,
        max_tokens=800
    )

    try:
        raw     = response.choices[0].message.content
        cleaned = raw.strip().replace("```json", "").replace("```", "")
        actions = json.loads(cleaned)

        action_map = {a["description"]: a["action"] for a in actions}
        exceptions_df = exceptions_df.copy()
        exceptions_df["action"] = exceptions_df["description"].map(
            lambda d: action_map.get(d, "Investigate and obtain supporting documentation")
        )
    except Exception:
        exceptions_df["action"] = "Investigate and obtain supporting documentation"

    return exceptions_df


# ─── INTERCOMPANY NARRATIVE ───────────────────────────────────────────────────

def generate_ic_commentary(
    disagreements_df: pd.DataFrame,
    fx_diffs_df: pd.DataFrame,
    stats: dict,
    context: str = ""
) -> str:
    """
    Generate an intercompany reconciliation narrative for group consolidation.
    """
    dis_str = disagreements_df.to_string(index=False) if not disagreements_df.empty else "No disagreements."
    fx_str  = fx_diffs_df.to_string(index=False) if not fx_diffs_df.empty else "No FX differences."

    prompt = f"""
You are a group financial controller preparing intercompany elimination notes for consolidation.

Reconciliation statistics:
- Total intercompany transactions: {stats.get('agreed_count', 0) + stats.get('disagreement_count', 0)}
- In agreement: {stats.get('agreed_count', 0)}
- Disagreements: {stats.get('disagreement_count', 0)}
- FX differences: {stats.get('fx_diff_count', 0)}
- Net difference at group level: £{stats.get('net_difference', 0):,.2f}
- Entity A balance: £{stats.get('entity_a_balance', 0):,.2f}
- Entity B balance: £{stats.get('entity_b_balance', 0):,.2f}

Disagreements:
{dis_str}

FX differences:
{fx_str}

{f"Additional context: {context}" if context else ""}

Write a formal intercompany reconciliation commentary in exactly 3 paragraphs:
1. Overall position — confirm whether net difference is zero, agreement rate.
2. Disagreements — explain each item, root cause, and elimination treatment required.
3. FX differences and sign-off recommendation, referencing IFRS 10 if relevant.

Write in formal group accounting language. Reference IFRS where appropriate.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a group financial controller specialising in consolidation."},
            {"role": "user",   "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=700
    )
    return response.choices[0].message.content


# ─── AP RECONCILIATION NARRATIVE ─────────────────────────────────────────────

def generate_ap_commentary(
    missing_df: pd.DataFrame,
    duplicates_df: pd.DataFrame,
    stats: dict,
    context: str = ""
) -> str:
    """
    Generate an AP supplier statement reconciliation narrative.
    """
    missing_str = missing_df.to_string(index=False) if not missing_df.empty else "No missing invoices."
    dup_str     = duplicates_df.to_string(index=False) if not duplicates_df.empty else "No duplicates."

    prompt = f"""
You are an accounts payable controller reviewing supplier statement reconciliations.

Reconciliation statistics:
- Total invoices on supplier statements: {stats.get('total_invoices', 0)}
- Total supplier statement value: £{stats.get('total_value', 0):,.2f}
- Matched to ledger: {stats.get('matched_count', 0)}
- Missing from ledger: {stats.get('missing_count', 0)}
- Duplicate risk items: {stats.get('duplicate_count', 0)}
- Total unreconciled value: £{stats.get('unreconciled_value', 0):,.2f}

Missing invoices (not in ledger):
{missing_str}

Potential duplicate payments:
{dup_str}

{f"Additional context: {context}" if context else ""}

Write a formal AP reconciliation exception report in exactly 3 paragraphs:
1. Overall reconciliation status and match rate.
2. Missing invoices — highlight overdue items and accrual requirements.
3. Duplicate payment risk — state urgency and recommended actions before next payment run.

Write in formal AP/finance language. Flag any items requiring immediate action.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are an accounts payable controller writing control documentation."},
            {"role": "user",   "content": prompt}
        ],
        temperature=TEMPERATURE,
        max_tokens=700
    )
    return response.choices[0].message.content
