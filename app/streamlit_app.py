import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Churn & Retention Decision Dashboard",
    layout="wide"
)

DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "churn_retention_clean.csv"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_PATH)

        date_columns = ["signup_date", "last_active_date", "churn_date"]
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")

        return df

    except FileNotFoundError:
        st.error(
            "Dataset not found. Please confirm that `churn_retention_clean.csv` exists inside `data/processed/`."
        )
        st.stop()

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()


df = load_data()

# --------------------------------------------------
# REQUIRED COLUMN VALIDATION
# --------------------------------------------------
required_columns = [
    "customer_id",
    "segment",
    "plan_type",
    "region",
    "engagement_band",
    "tenure_band",
    "churn_flag",
    "engagement_score",
    "revenue_at_risk",
    "last_active_date",
    "churn_reason"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(
        "The dataset is missing the following required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

# --------------------------------------------------
# DATA CLEANING SAFETY
# --------------------------------------------------
df["churn_flag"] = pd.to_numeric(df["churn_flag"], errors="coerce").fillna(0)
df["engagement_score"] = pd.to_numeric(df["engagement_score"], errors="coerce").fillna(0)
df["revenue_at_risk"] = pd.to_numeric(df["revenue_at_risk"], errors="coerce").fillna(0)

df["segment"] = df["segment"].fillna("Unknown")
df["plan_type"] = df["plan_type"].fillna("Unknown")
df["region"] = df["region"].fillna("Unknown")
df["engagement_band"] = df["engagement_band"].fillna("Unknown")
df["tenure_band"] = df["tenure_band"].fillna("Unknown")
df["churn_reason"] = df["churn_reason"].fillna("Not Provided")

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 46px;
        font-weight: 900;
        color: #1f4e8c;
        text-align: center;
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        color: #4b5563;
        font-size: 18px;
        margin-bottom: 26px;
    }

    .section-title {
        color: #1f2937;
        font-size: 24px;
        font-weight: 800;
        margin-top: 14px;
        margin-bottom: 10px;
    }

    .kpi-card {
        background-color: #f8fafc;
        border: 1px solid #d9e2ef;
        border-radius: 16px;
        padding: 18px;
        text-align: center;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    }

    .kpi-label {
        color: #3569ad;
        font-size: 15px;
        font-weight: 700;
    }

    .kpi-value {
        color: #111827;
        font-size: 29px;
        font-weight: 900;
    }

    .insight-caption {
        font-size: 14px;
        color: #374151;
        background-color: #f8fafc;
        border-left: 4px solid #3569ad;
        padding: 10px 12px;
        border-radius: 8px;
        margin-top: -8px;
        margin-bottom: 18px;
    }

    .summary-card {
        border-radius: 16px;
        padding: 18px;
        min-height: 180px;
        border: 1px solid #d6dee8;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.04);
    }

    .impact-box {
        background-color: #f8fafc;
        border: 1px solid #d9e2ef;
        border-radius: 16px;
        padding: 18px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.markdown(
    '<div class="main-title">Churn & Retention Decision Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Business + product analytics dashboard for monitoring churn risk, retention behavior,
    engagement decline, and revenue exposure to support executive retention decisions.
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
with st.sidebar:
    st.header("Dashboard Filters")

    min_date = df["last_active_date"].min()
    max_date = df["last_active_date"].max()

    if pd.notna(min_date) and pd.notna(max_date):
        date_range = st.date_input(
            "Last Active Date Range",
            value=(min_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date()
        )
    else:
        date_range = None

    segment = st.multiselect(
        "Segment",
        sorted(df["segment"].unique()),
        default=sorted(df["segment"].unique())
    )

    plan = st.multiselect(
        "Plan Type",
        sorted(df["plan_type"].unique()),
        default=sorted(df["plan_type"].unique())
    )

    region = st.multiselect(
        "Region",
        sorted(df["region"].unique()),
        default=sorted(df["region"].unique())
    )

    engagement = st.multiselect(
        "Engagement Band",
        sorted(df["engagement_band"].unique()),
        default=sorted(df["engagement_band"].unique())
    )

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------
filtered = df[
    df["segment"].isin(segment)
    & df["plan_type"].isin(plan)
    & df["region"].isin(region)
    & df["engagement_band"].isin(engagement)
].copy()

if date_range and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["last_active_date"] >= pd.to_datetime(start_date))
        & (filtered["last_active_date"] <= pd.to_datetime(end_date))
    ]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your filter selections.")
    st.stop()

# --------------------------------------------------
# DOWNLOAD FILTERED DATA
# --------------------------------------------------
st.download_button(
    label="Download Filtered Dataset",
    data=filtered.to_csv(index=False),
    file_name="filtered_churn_retention_data.csv",
    mime="text/csv"
)

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------
total_customers = filtered["customer_id"].nunique()
churn_rate = filtered["churn_flag"].mean()
retention_rate = 1 - churn_rate
revenue_at_risk = filtered["revenue_at_risk"].sum()
avg_engagement = filtered["engagement_score"].mean()
churned_customers = filtered.loc[filtered["churn_flag"] == 1, "customer_id"].nunique()

# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)

metrics = [
    ("Total Customers", f"{total_customers:,.0f}"),
    ("Churn Rate", f"{churn_rate:.2%}"),
    ("Retention Rate", f"{retention_rate:.2%}"),
    ("Revenue at Risk", f"${revenue_at_risk:,.0f}"),
    ("Avg Engagement", f"{avg_engagement:.2f}")
]

for col, (label, value) in zip([k1, k2, k3, k4, k5], metrics):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# --------------------------------------------------
# VISUAL SECTION
# --------------------------------------------------
st.markdown('<div class="section-title">Retention Risk & Product Health Visuals</div>', unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    trend = filtered.dropna(subset=["last_active_date"]).copy()

    if trend.empty:
        st.info("No valid date data available for churn trend.")
    else:
        trend["month"] = trend["last_active_date"].dt.to_period("M").dt.to_timestamp()
        trend_df = trend.groupby("month", as_index=False)["churn_flag"].mean()

        fig = px.line(
            trend_df,
            x="month",
            y="churn_flag",
            title="Monthly Churn Trend",
            markers=True
        )
        fig.update_yaxes(tickformat=".0%", title=None, showgrid=False)
        fig.update_xaxes(title=None, showgrid=False)
        fig.update_layout(height=360, title_x=0.5, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-caption"><b>Insight:</b> Monthly churn movement identifies when customer loss accelerates and where retention review should begin.</div>',
        unsafe_allow_html=True
    )

with row1_col2:
    segment_df = (
        filtered.groupby("segment", as_index=False)["churn_flag"]
        .mean()
        .sort_values("churn_flag", ascending=False)
    )

    fig = px.bar(
        segment_df,
        x="segment",
        y="churn_flag",
        title="Churn Rate by Segment",
        text=segment_df["churn_flag"].map(lambda x: f"{x:.1%}")
    )
    fig.update_yaxes(tickformat=".0%", title=None, showgrid=False)
    fig.update_xaxes(title=None, showgrid=False)
    fig.update_layout(height=360, title_x=0.5, plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-caption"><b>Insight:</b> Segment-level churn helps prioritize retention investment toward customer groups with the highest risk.</div>',
        unsafe_allow_html=True
    )

with row1_col3:
    tenure_df = (
        filtered.groupby("tenure_band", as_index=False, observed=False)["churn_flag"]
        .mean()
        .sort_values("churn_flag", ascending=True)
    )

    fig = px.bar(
        tenure_df,
        y="tenure_band",
        x="churn_flag",
        orientation="h",
        title="Churn Rate by Tenure",
        text=tenure_df["churn_flag"].map(lambda x: f"{x:.1%}")
    )
    fig.update_xaxes(tickformat=".0%", title=None, showgrid=False)
    fig.update_yaxes(title=None, showgrid=False)
    fig.update_layout(height=360, title_x=0.5, plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-caption"><b>Insight:</b> Tenure churn shows whether retention risk is concentrated during onboarding or after longer product use.</div>',
        unsafe_allow_html=True
    )

row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    engagement_df = (
        filtered.groupby("engagement_band", as_index=False, observed=False)["churn_flag"]
        .mean()
        .sort_values("churn_flag", ascending=True)
    )

    fig = px.bar(
        engagement_df,
        y="engagement_band",
        x="churn_flag",
        orientation="h",
        title="Engagement Band vs Churn",
        text=engagement_df["churn_flag"].map(lambda x: f"{x:.1%}")
    )
    fig.update_xaxes(tickformat=".0%", title=None, showgrid=False)
    fig.update_yaxes(title=None, showgrid=False)
    fig.update_layout(height=360, title_x=0.5, plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-caption"><b>Insight:</b> Engagement is a leading churn signal that helps teams intervene before customers fully disengage.</div>',
        unsafe_allow_html=True
    )

with row2_col2:
    revenue_df = (
        filtered.groupby("engagement_band", as_index=False, observed=False)["revenue_at_risk"]
        .sum()
        .sort_values("revenue_at_risk", ascending=False)
    )

    fig = px.bar(
        revenue_df,
        x="engagement_band",
        y="revenue_at_risk",
        title="Revenue at Risk by Engagement",
        text=revenue_df["revenue_at_risk"].map(lambda x: f"${x/1000:.1f}K")
    )
    fig.update_yaxes(title=None, showgrid=False)
    fig.update_xaxes(title=None, showgrid=False)
    fig.update_layout(height=360, title_x=0.5, plot_bgcolor="white", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-caption"><b>Insight:</b> Revenue exposure connects churn risk to financial impact, helping leadership prioritize high-value retention actions.</div>',
        unsafe_allow_html=True
    )

with row2_col3:
    reasons = (
        filtered[filtered["churn_flag"] == 1]
        .groupby("churn_reason", as_index=False)["customer_id"]
        .count()
        .rename(columns={"customer_id": "churned_customers"})
        .sort_values("churned_customers", ascending=True)
    )

    if reasons.empty:
        st.info("No churned customers available for churn reason analysis.")
    else:
        fig = px.bar(
            reasons,
            y="churn_reason",
            x="churned_customers",
            orientation="h",
            title="Top Churn Reasons",
            text="churned_customers"
        )
        fig.update_xaxes(title=None, showgrid=False)
        fig.update_yaxes(title=None, showgrid=False)
        fig.update_layout(height=360, title_x=0.5, plot_bgcolor="white", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        '<div class="insight-caption"><b>Insight:</b> Churn reasons identify the product, service, or experience issues most connected to customer loss.</div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# --------------------------------------------------
# MEASURABLE BUSINESS IMPACT
# --------------------------------------------------
st.markdown('<div class="section-title">Measurable Business Impact</div>', unsafe_allow_html=True)

estimated_save_rate = 0.15
potential_revenue_saved = revenue_at_risk * estimated_save_rate

st.markdown(
    f"""
    <div class="impact-box">
        <b>Business Impact Estimate:</b><br><br>
        This dashboard identifies <b>{churned_customers:,.0f}</b> churned customers and 
        <b>${revenue_at_risk:,.0f}</b> in revenue at risk across the selected customer base.
        If targeted retention actions recover only <b>15%</b> of exposed revenue, the business could protect approximately 
        <b>${potential_revenue_saved:,.0f}</b> in revenue.
        <br><br>
        <b>Decision Value:</b> The dashboard helps product, customer success, and leadership teams prioritize retention
        investment by customer segment, engagement behavior, tenure, churn reason, and financial exposure.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --------------------------------------------------
# EXECUTIVE DECISION SUMMARY
# --------------------------------------------------
st.markdown('<div class="section-title">Executive Decision Summary</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

cards = [
    (
        "INSIGHT",
        "Low-engagement and high-risk customer groups show measurable churn exposure and should be treated as early-warning retention segments.",
        "#e8f3ff"
    ),
    (
        "ACTION",
        "Monitor churn rate, engagement band, tenure, churn reason, and revenue exposure weekly to detect retention deterioration earlier.",
        "#fff7dc"
    ),
    (
        "RECOMMENDATION",
        "Launch targeted retention campaigns for high-value customers with declining engagement before increasing acquisition spend.",
        "#e7f7ed"
    ),
    (
        "DECISION",
        "Prioritize retention investment toward the highest-risk, highest-value segments to reduce preventable churn and protect revenue.",
        "#fdecef"
    )
]

for col, (title, body, color) in zip([s1, s2, s3, s4], cards):
    with col:
        st.markdown(
            f"""
            <div class="summary-card" style="background-color:{color};">
                <h4 style="text-align:center; color:#111827;">{title}</h4>
                <p style="text-align:center; color:#374151;">{body}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------
with st.expander("View Filtered Data Preview"):
    st.dataframe(filtered.head(100), use_container_width=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.caption(
    "Built with Streamlit, Python, Pandas, and Plotly to support churn monitoring, retention prioritization, product analytics, and executive decision-making."
)