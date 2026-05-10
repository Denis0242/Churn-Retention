import streamlit as st

def metric_card(label, value):
    st.metric(label, value)

def insight_panel():
    st.markdown("""
### Insight → Action → Recommendation → Decision

**Insight:** Low-engagement customers show elevated churn exposure and create avoidable revenue risk.  
**Action:** Identify low-engagement customers early using sessions, feature usage, tenure, and segment filters.  
**Recommendation:** Launch targeted retention campaigns and onboarding improvements for high-risk customers.  
**Decision:** Prioritize retention investment before increasing acquisition spend.
""")
