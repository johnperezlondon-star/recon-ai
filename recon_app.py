"""
app.py
──────
Streamlit web application for the AI Reconciliation Tool.
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import io
from recon_engine import (
    run_bank_reconciliation,
    run_intercompany_reconciliation,
    run_ap_reconciliation,
)
from ai_narrative import (
    generate_bank_commentary,
    generate_ic_commentary,
    generate_ap_commentary,
    generate_exception_actions,
)

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="AI Reconciliation Tool",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

st.sidebar.title("ReconAI")
st.sidebar.caption("AI-powered reconciliation engine v1.0")
st.sidebar.divider()

recon_type = st.sidebar.radio(
    "Reconciliation type",
    ["Bank reconciliation", "Intercompany", "Accounts payable"],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.caption("Built with Python + fuzzy matching + GPT-4o")
st.sidebar.caption("Portfolio project — John Perez")

# ─── MAIN ─────────────────────────────────────────────────────────────────────

if recon_type == "Bank reconciliation":

    st.title("Bank reconciliation")
    st.caption("Match bank statement lines against your general ledger. GPT-4o writes the sign-off narrative.")

    col1, col2 = st.columns(2)
    with col1:
        bank_file = st.file_uploader("Upload bank statement CSV", type="csv", key="bank")
    with col2:
        gl_file = st.file_uploader("Upload GL extract CSV", type="csv", key="gl")

    context = st.text_area(
        "Optional: add context for the AI",
        placeholder="e.g. Month-end payroll was processed on 28th. Unusual CHAPS receipt from HMRC on 22nd.",
        height=80
    )

    if bank_file and gl_file:
        if st.button("Run reconciliation", type="primary"):
            with st.spinner("Matching transactions... this takes a few seconds"):
                results = run_bank_reconciliation(bank_file, gl_file)

            stats = results["summary_stats"]

            # KPI metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total lines", stats["total_bank_lines"])
            c2.metric("Matched", stats["matched_count"], f"{stats['match_rate_pct']}% rate")
            c3.metric("Exceptions", stats["exception_count"], f"£{stats['unreconciled_value']:,.0f}", delta_color="inverse")
            c4.metric("Timing diffs", stats["timing_count"])

            st.divider()

            # Result tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                f"Matched ({stats['matched_count']})",
                f"Exceptions ({stats['exception_count']})",
                f"Timing diffs ({stats['timing_count']})",
                "AI sign-off summary"
            ])

            with tab1:
                st.dataframe(results["matched"], use_container_width=True)

            with tab2:
                exc_df = results["exceptions"]
                if not exc_df.empty:
                    if st.button("Generate AI investigation actions"):
                        with st.spinner("GPT-4o generating actions..."):
                            exc_df = generate_exception_actions(exc_df, "bank")
                    st.dataframe(exc_df, use_container_width=True)

            with tab3:
                st.dataframe(results["timing"], use_container_width=True)

            with tab4:
                if st.button("Generate sign-off narrative"):
                    with st.spinner("GPT-4o writing reconciliation narrative..."):
                        narrative = generate_bank_commentary(
                            results["exceptions"],
                            results["timing"],
                            stats,
                            context
                        )
                    st.write(narrative)

                    # Download button
                    st.download_button(
                        "Download narrative (.txt)",
                        data=narrative,
                        file_name="bank_recon_signoff.txt",
                        mime="text/plain"
                    )

            # Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                results["matched"].to_excel(writer, sheet_name="Matched", index=False)
                results["exceptions"].to_excel(writer, sheet_name="Exceptions", index=False)
                results["timing"].to_excel(writer, sheet_name="Timing", index=False)

            st.download_button(
                "Download full Excel report",
                data=output.getvalue(),
                file_name="bank_reconciliation.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:
        st.info("Upload both CSV files to begin. Sample files are in the /data folder.")
        with st.expander("Expected CSV format — bank statement"):
            st.code("date,description,amount,reference\n2024-06-01,BACS Payroll June,287450.00,REF001")
        with st.expander("Expected CSV format — GL extract"):
            st.code("date,description,amount,account_ref\n2024-06-01,Payroll June 2024,287450.00,10001-001")


elif recon_type == "Intercompany":

    st.title("Intercompany reconciliation")
    st.caption("Reconcile intercompany balances between entities for group consolidation.")

    col1, col2 = st.columns(2)
    with col1:
        ea_file = st.file_uploader("Upload Entity A CSV", type="csv", key="ea")
        st.caption("e.g. UK HoldCo interco ledger")
    with col2:
        eb_file = st.file_uploader("Upload Entity B CSV", type="csv", key="eb")
        st.caption("e.g. EU OpCo interco ledger")

    context = st.text_area("Optional context", placeholder="e.g. FX rate used: EUR/GBP 1.1682 at 30 June 2024.", height=60)

    if ea_file and eb_file:
        if st.button("Run intercompany reconciliation", type="primary"):
            with st.spinner("Matching intercompany transactions..."):
                results = run_intercompany_reconciliation(ea_file, eb_file)

            stats = results["summary_stats"]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Entity A balance", f"£{stats['entity_a_balance']:,.0f}")
            c2.metric("Entity B balance", f"£{stats['entity_b_balance']:,.0f}")
            c3.metric("In agreement", stats["agreed_count"])
            c4.metric("Net difference", f"£{stats['net_difference']:,.2f}", delta_color="off")

            tab1, tab2, tab3, tab4 = st.tabs([
                f"Agreed ({stats['agreed_count']})",
                f"Disagreements ({stats['disagreement_count']})",
                f"FX diffs ({stats['fx_diff_count']})",
                "AI consolidation summary"
            ])

            with tab1:
                st.dataframe(results["agreed"], use_container_width=True)
            with tab2:
                st.dataframe(results["disagreements"], use_container_width=True)
                if st.button("Generate AI analysis"):
                    with st.spinner("GPT-4o analysing disagreements..."):
                        narrative = generate_ic_commentary(
                            results["disagreements"], results["fx_diffs"], stats, context
                        )
                    st.write(narrative)
            with tab3:
                st.dataframe(results["fx_diffs"], use_container_width=True)
            with tab4:
                if st.button("Generate consolidation narrative"):
                    with st.spinner("GPT-4o writing consolidation commentary..."):
                        narrative = generate_ic_commentary(
                            results["disagreements"], results["fx_diffs"], stats, context
                        )
                    st.write(narrative)


elif recon_type == "Accounts payable":

    st.title("Accounts payable reconciliation")
    st.caption("Match supplier statements against your AP ledger. Detects missing invoices and duplicate payment risk.")

    col1, col2 = st.columns(2)
    with col1:
        sup_file = st.file_uploader("Upload supplier statements CSV", type="csv", key="sup")
    with col2:
        ledger_file = st.file_uploader("Upload AP ledger CSV", type="csv", key="ledger")

    context = st.text_area("Optional context", placeholder="e.g. Payment run scheduled 5 July. New supplier DataSoft Inc added June.", height=60)

    if sup_file and ledger_file:
        if st.button("Run AP reconciliation", type="primary"):
            with st.spinner("Matching supplier invoices..."):
                results = run_ap_reconciliation(sup_file, ledger_file)

            stats = results["summary_stats"]
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total invoices", stats["total_invoices"])
            c2.metric("Matched", stats["matched_count"])
            c3.metric("Missing", stats["missing_count"], delta_color="inverse")
            c4.metric("Duplicate risk", stats["duplicate_count"], delta_color="inverse")

            if stats["duplicate_count"] > 0:
                st.error(f"⚠️ {stats['duplicate_count']} potential duplicate payment(s) detected — review before next payment run")

            tab1, tab2, tab3, tab4 = st.tabs([
                f"Matched ({stats['matched_count']})",
                f"Missing in ledger ({stats['missing_count']})",
                f"Duplicate risk ({stats['duplicate_count']})",
                "AI exception report"
            ])

            with tab1:
                st.dataframe(results["matched"], use_container_width=True)
            with tab2:
                miss_df = results["missing"]
                if not miss_df.empty:
                    if st.button("Generate AI actions for missing invoices"):
                        with st.spinner("GPT-4o generating investigation actions..."):
                            miss_df = generate_exception_actions(miss_df, "accounts payable")
                    st.dataframe(miss_df, use_container_width=True)
            with tab3:
                st.dataframe(results["duplicates"], use_container_width=True)
            with tab4:
                if st.button("Generate AP exception report"):
                    with st.spinner("GPT-4o writing exception narrative..."):
                        narrative = generate_ap_commentary(
                            results["missing"], results["duplicates"], stats, context
                        )
                    st.write(narrative)
