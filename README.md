# AI Reconciliation Tool

> Three reconciliation types. One tool. GPT-4o writes the narrative so you don't have to.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o-OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=flat-square&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Portfolio%20Ready-brightgreen?style=flat-square)

---

## The business problem this solves

Finance teams spend **an entire day every month** on manual reconciliations:

- Copying bank statement lines into spreadsheets and manually searching the GL
- Emailing back and forth between entities to resolve intercompany differences
- Chasing AP teams about invoices that appear on supplier statements but not in the ledger
- Writing the same reconciliation commentary for every audit file, every month

This tool automates all three workflows. Upload two files, click run, and receive a fully matched reconciliation with exception flags and a GPT-4o narrative ready for the audit file — in under two minutes.

---

## Live demo

**[View the interactive UI demo →](app_demo.html)**

Shows all three reconciliation types with sample data pre-loaded. Click "Run reconciliation" on any tab to see the matching engine in action, then click "Generate AI actions" for the GPT-4o commentary.

---

## Three reconciliation types

### 1. Bank reconciliation
Matches bank statement lines against general ledger entries using exact and fuzzy string matching. Classifies results into matched, exceptions, and timing differences. GPT-4o generates a formal sign-off narrative for the audit file.

**Key technical features:**
- Fuzzy description matching using `SequenceMatcher` (configurable threshold — default 80%)
- Automatic exception classification (missing entry, duplicate, wrong amount, bank charge)
- Timing difference detection for near-matches in adjacent periods
- Configurable materiality thresholds

### 2. Intercompany reconciliation
Reconciles intercompany balances between two entities for group consolidation. Matches on transaction reference first, falls back to fuzzy description matching. Identifies FX translation differences separately from genuine disagreements.

**Key technical features:**
- Reference-first matching with fuzzy fallback
- FX difference isolation (below £500 threshold = FX, above = genuine disagreement)
- Root cause classification for each disagreement
- IFRS 10 elimination commentary from GPT-4o

### 3. Accounts payable reconciliation
Matches supplier statement invoices against the AP ledger. Detects missing invoices (not posted) and duplicate payment risk (same invoice number appearing twice).

**Key technical features:**
- Invoice number exact matching with amount validation
- Duplicate detection using pandas `duplicated()` on invoice + amount
- Risk scoring for duplicate items (High/Medium based on amount)
- GPT-4o generates specific action for each missing invoice

---

## Sample output

**Bank reconciliation sign-off narrative (GPT-4o generated):**

> *The HSBC Operating Account bank reconciliation for June 2024 has been completed with a match rate of 94.2%, representing 128 of 142 transactions successfully reconciled. The reconciliation is materially complete; the remaining unreconciled balance of £34,250 comprises eight exception items requiring investigation...*

**AP exception action (GPT-4o generated, per invoice):**

> *INV-9012 — Acme Corp £8,400: Post immediately — payment due 18 July, risk of late payment penalty.*

---

## How it works

```
Source A (CSV)  ──┐
                   ├──► recon_engine.py  ──► matched / exceptions / timing
Source B (CSV)  ──┘    (pandas + fuzzy)           │
                                                   ▼
context notes  ─────────────────────────► ai_narrative.py (GPT-4o)
                                                   │
                                    ┌──────────────┼──────────────┐
                                    ▼              ▼              ▼
                            Exception         Sign-off        Excel
                            actions           narrative       report
```

---

## Project structure

```
recon-ai/
├── data/
│   ├── sample_bank_statement.csv
│   ├── sample_gl_extract.csv
│   ├── sample_entity_a.csv
│   ├── sample_entity_b.csv
│   ├── sample_supplier_statements.csv
│   └── sample_ap_ledger.csv
├── outputs/
├── recon_engine.py       # Core matching logic — pandas + fuzzy matching
├── ai_narrative.py       # GPT-4o integration — 3 prompt types
├── app.py                # Streamlit UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quickstart (beginner-friendly)

### Step 1 — Install Python

Go to [python.org/downloads](https://python.org/downloads) and download Python 3.10 or higher.
During installation, tick **"Add Python to PATH"** — this is important.

Verify it worked: open Terminal (Mac) or Command Prompt (Windows) and type:
```
python --version
```
You should see something like `Python 3.11.4`.

### Step 2 — Download the project

Click the green **Code** button on this GitHub page → **Download ZIP** → unzip it somewhere easy to find (e.g. your Desktop).

### Step 3 — Open a terminal in the project folder

**Windows:** Open the unzipped folder, hold Shift + right-click in the folder → "Open PowerShell window here"

**Mac:** Open Terminal, type `cd ` (with a space), then drag the unzipped folder into the Terminal window and press Enter.

### Step 4 — Install the required packages

Copy and paste this into your terminal, then press Enter:
```bash
pip install pandas openpyxl openai streamlit python-dotenv
```
Wait for it to finish (takes 1–2 minutes).

### Step 5 — Add your OpenAI API key

Rename `.env.example` to `.env`. Open it with any text editor (Notepad on Windows, TextEdit on Mac) and replace the placeholder:
```
OPENAI_API_KEY=sk-paste-your-key-here
```
Get a free API key at [platform.openai.com](https://platform.openai.com). The reconciliation tool uses approximately $0.02–0.05 of API credits per run.

### Step 6 — Run the app

In your terminal, type:
```bash
streamlit run app.py
```

Your browser will open automatically at `http://localhost:8501`. Upload the sample CSV files from `/data` to see it working immediately.

---

## Data format

All six sample CSV files are included in `/data`. Here are the column requirements:

**Bank statement:**
```csv
date,description,amount,reference
2024-06-01,BACS Payroll June,287450.00,REF001
```

**GL extract:**
```csv
date,description,amount,account_ref
2024-06-01,Payroll June 2024,287450.00,10001-001
```

**Supplier statements:**
```csv
invoice_number,supplier,invoice_date,amount
INV-8821,Acme Corp,2024-06-04,12400.00
```

**AP ledger:**
```csv
invoice_number,supplier,invoice_date,amount,gl_ref
INV-8821,Acme Corp,2024-06-04,12400.00,GL-40021
```

---

## Configuration

In `recon_engine.py`, adjust these settings to match your team's standards:

```python
MATERIALITY_ABS  = 500    # Flag exceptions above £500
MATERIALITY_PCT  = 0.01   # Flag exceptions above 1% of total
FUZZY_THRESHOLD  = 0.80   # 80% description similarity = match
EXACT_THRESHOLD  = 0.001  # Amount tolerance of £0.001
```

---

## Key technical decisions

**Why fuzzy matching instead of exact matching?**
In real-world reconciliations, bank descriptions and GL descriptions are never identical. "BACS — Payroll June 2024" in the bank won't exactly match "Payroll June 2024 — Staff" in the GL. `SequenceMatcher` catches these near-matches without requiring manual mapping.

**Why send only exceptions to GPT-4o?**
Sending 142 bank statement lines to the API would be slow and expensive. By pre-filtering to exception items (typically 5–15% of total), the AI call is fast, cheap, and focused — and produces tighter, more relevant commentary.

**Why three separate narrative prompts?**
Bank, intercompany, and AP reconciliations have completely different audiences and sign-off requirements. A bank recon narrative is for the audit file. An intercompany narrative is for the consolidation pack. An AP narrative is for the AP manager before the payment run. Each prompt is written for its specific context.

---

## Requirements

```
pandas>=2.0
openpyxl>=3.1
openai>=1.0
streamlit>=1.28
python-dotenv>=1.0
```

---

## Roadmap

- [ ] Support for multi-currency bank reconciliations
- [ ] Automated journal entry drafts for common exceptions
- [ ] Scheduled monthly runs via GitHub Actions
- [ ] ERP integration (SAP, Sage, Xero API connectors)
- [ ] Historical exception pattern analysis ("this supplier always has timing diffs")

---

## Skills demonstrated

| Area | What this project shows |
|------|------------------------|
| Finance domain | Bank recon, intercompany elimination, AP controls, IFRS 10, duplicate detection |
| Python / Pandas | CSV processing, fuzzy string matching, duplicate detection, conditional classification |
| AI / Prompt engineering | Three specialised GPT-4o prompts, JSON-structured output, exception batch processing |
| Software design | Modular architecture, separation of concerns, configurable thresholds |
| UI | Multi-page Streamlit app with tab navigation and file upload |

---

## About

Built as part of a Finance AI portfolio demonstrating practical automation of core reconciliation workflows. Background in financial accounting and controllership — these are real tasks I've observed consuming significant manual effort in finance teams.

*Connect on [LinkedIn](#) · See more projects at [johnperezlondon-star.github.io](https://johnperezlondon-star.github.io)*

---

## Licence

MIT — free to use, adapt, and build on.
