import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="IntelliCredit AI", layout="wide")

if "screen" not in st.session_state:
    st.session_state.screen = 1
if "company_data" not in st.session_state:
    st.session_state.company_data = None
if "financials" not in st.session_state:
    st.session_state.financials = None

def generate_financials(company, sector):
    base = np.random.uniform(50, 500)
    return {"fy2024": {"revenue": base, "ebitda": base*0.18, "debt": base*0.9, "equity": base*1.6},"fy2023": {"revenue": base*0.85, "ebitda": base*0.85*0.16, "debt": base*0.8, "equity": base*1.5},"fy2022": {"revenue": base*0.7, "ebitda": base*0.7*0.14, "debt": base*0.7, "equity": base*1.4}}

def calculate_five_cs(financials):
    latest = financials["fy2024"]
    prev = financials["fy2023"]
    composite = 20 + (25 if (latest["ebitda"]*0.8)/(latest["debt"]*0.15) > 2 else 15) + (25 if latest["equity"]/(latest["equity"]+latest["debt"]) > 0.4 else 15) + 20 + (25 if (latest["revenue"]-prev["revenue"])/prev["revenue"] > 0.15 else 15)
    return {"composite": composite, "recommendation": "APPROVE" if composite >= 95 else ("CONDITIONAL" if composite >= 80 else "REVIEW")}

if st.session_state.screen == 1:
    st.markdown("# 🏢 IntelliCredit AI\n**AI-Powered Corporate Credit Risk Assessment**")
    company_name = st.text_input("Company Name")
    sector = st.selectbox("Sector", ["Manufacturing", "Technology", "Retail", "Healthcare"])
    loan_amount = st.number_input("Loan Amount (₹ Cr)", min_value=1.0, value=50.0)
    if st.button("📊 ANALYZE", type="primary"):
        if company_name:
            st.session_state.company_data = {"name": company_name, "sector": sector, "loan_amount": loan_amount}
            st.session_state.financials = generate_financials(company_name, sector)
            st.session_state.screen = 2
            st.rerun()
elif st.session_state.screen == 2:
    st.markdown("# 📊 Financial Dashboard")
    latest = st.session_state.financials["fy2024"]
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", f"₹{latest['revenue']:.1f} Cr")
    col2.metric("EBITDA", f"₹{latest['ebitda']:.1f} Cr")
    col3.metric("Debt", f"₹{latest['debt']:.1f} Cr")
    if st.button("➡️ RISK ANALYSIS", type="primary"):
        st.session_state.screen = 3
        st.rerun()
elif st.session_state.screen == 3:
    st.markdown("# 🎯 Risk Scoring")
    scores = calculate_five_cs(st.session_state.financials)
    st.markdown(f"### Score: {scores['composite']}/125")
    st.markdown(f"### Recommendation: **{scores['recommendation']}**")
    if st.button("✅ DONE"):
        st.session_state.screen = 1
        st.rerun()
