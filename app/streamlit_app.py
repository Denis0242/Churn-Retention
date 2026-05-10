import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, kpis
from components import insight_panel

st.set_page_config(page_title="Churn & Retention Intelligence Platform", layout="wide")
st.title("Churn & Retention Intelligence Platform")
st.caption("Portfolio project for Data Analyst / Product Data Analyst positioning")

df = load_data()

with st.sidebar:
    st.header("Filters")
    segment = st.multiselect("Segment", sorted(df["segment"].dropna().unique()), default=sorted(df["segment"].dropna().unique()))
    region = st.multiselect("Region", sorted(df["region"].dropna().unique()), default=sorted(df["region"].dropna().unique()))
    engagement = st.multiselect("Engagement Band", list(df["engagement_band"].cat.categories), default=list(df["engagement_band"].cat.categories))

filtered = df[df["segment"].isin(segment) & df["region"].isin(region) & df["engagement_band"].isin(engagement)]
metrics = kpis(filtered)

cols = st.columns(5)
cols[0].metric("Total Customers", f"{metrics['total_customers']:,}")
cols[1].metric("Churn Rate", f"{metrics['churn_rate']:.2%}")
cols[2].metric("Retention Rate", f"{metrics['retention_rate']:.2%}")
cols[3].metric("Revenue at Risk", f"${metrics['revenue_at_risk']:,.0f}")
cols[4].metric("Avg Engagement", f"{metrics['avg_engagement']:.2f}")

st.divider()

left, mid, right = st.columns(3)
with left:
    seg = filtered.groupby("segment", as_index=False)["churn"].mean()
    seg["churn_rate"] = seg["churn"] * 100
    st.plotly_chart(px.bar(seg, x="segment", y="churn_rate", title="Segment Churn Rate"), use_container_width=True)
with mid:
    ten = filtered.groupby("tenure_band", observed=False, as_index=False)["churn"].mean()
    ten["churn_rate"] = ten["churn"] * 100
    st.plotly_chart(px.bar(ten, x="tenure_band", y="churn_rate", title="Churn by Tenure"), use_container_width=True)
with right:
    reason = filtered[filtered["churn"] == 1].groupby("churn_reason", as_index=False).size().sort_values("size", ascending=False)
    st.plotly_chart(px.bar(reason, x="size", y="churn_reason", orientation="h", title="Churn Reasons"), use_container_width=True)

st.subheader("Customer-Level Risk Table")
st.dataframe(filtered.sort_values(["churn", "revenue", "engagement_score"], ascending=[False, False, True]).head(50), use_container_width=True)

insight_panel()
