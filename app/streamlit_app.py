# =========================================================
# Churn & Retention Dashboard
# Streamlit recreation of the Tableau dashboard
# =========================================================

from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Churn & Retention Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# Styling
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .main {background-color: #ffffff;}
        h1, h2, h3 {color: #2F5F9F;}
        .kpi-card {
            background: #f7f9fc;
            border: 1px solid #e5e9f0;
            border-radius: 10px;
            padding: 14px 16px;
            min-height: 110px;
        }
        .kpi-label {
            color: #2F5F9F;
            font-size: 18px;
            line-height: 1.1;
        }
        .kpi-value {
            color: #333333;
            font-size: 28px;
            font-weight: 700;
            margin-top: 10px;
        }
        .summary-box {
            border-radius: 10px;
            padding: 16px;
            min-height: 190px;
            font-size: 16px;
            line-height: 1.55;
        }
        .insight {background-color:#e8f2ff; color:#0050a4;}
        .action {background-color:#fff9db; color:#8a6400;}
        .recommendation {background-color:#e6f7ed; color:#087b35;}
        .decision {background-color:#fde7e9; color:#b4232f;}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    possible_paths = [
        Path("data/churn_retention.csv"),
        Path("../data/churn_retention.csv"),
        Path("data/churn & retention.csv"),
        Path("../data/churn & retention.csv"),
        Path("churn_retention.csv"),
    ]

    for path in possible_paths:
        if path.exists():
            return pd.read_csv(path)

    st.error("Dataset not found. Place churn_retention.csv inside the data folder.")
    st.stop()


df = load_data()

# ---------------------------------------------------------
# Data Preparation for Dashboard
# ---------------------------------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)

for date_col in ["signup_date", "last_active_date", "churn_date"]:
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

numeric_cols = [
    "tenure_days", "sessions_last_30d", "avg_session_duration",
    "feature_usage_score", "engagement_score", "revenue", "lifetime_value", "churn"
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

required = [
    "customer_id", "signup_date", "last_active_date", "tenure_days", "segment",
    "plan_type", "region", "device", "acquisition_channel", "engagement_score",
    "revenue", "churn", "churn_reason"
]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error(f"Missing required columns: {missing}")
    st.write("Available columns:", list(df.columns))
    st.stop()

# Clean categories
for col in ["segment", "plan_type", "region", "device", "acquisition_channel", "churn_reason"]:
    df[col] = df[col].fillna("Unknown").astype(str)

# Clean numeric values
for col in ["tenure_days", "engagement_score", "revenue", "lifetime_value", "churn"]:
    df[col] = df[col].fillna(df[col].median())

# Feature engineering used by the dashboard
if "engagement_band" not in df.columns:
    df["engagement_band"] = pd.cut(
        df["engagement_score"],
        bins=[-1, 25, 50, 100],
        labels=["Low Engagement", "Medium Engagement", "High Engagement"]
    ).astype(str)

if "tenure_band" not in df.columns:
    df["tenure_band"] = pd.cut(
        df["tenure_days"],
        bins=[-1, 30, 90, 180, np.inf],
        labels=["0–30 Days", "31–90 Days", "91–180 Days", "181+ Days"]
    ).astype(str)

df["churn"] = df["churn"].astype(int)
df["retention_flag"] = 1 - df["churn"]
df["revenue_at_risk"] = df["revenue"] * df["churn"]
df["dashboard_date"] = df["churn_date"].fillna(df["last_active_date"]).fillna(df["signup_date"])

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("Dashboard Filters")

def multiselect_filter(label, column):
    values = sorted(df[column].dropna().astype(str).unique())
    return st.sidebar.multiselect(label, values, default=values)

channel_filter = multiselect_filter("Channel", "acquisition_channel")
device_filter = multiselect_filter("Device", "device")
engagement_filter = multiselect_filter("Engagement Band", "engagement_band")
plan_filter = multiselect_filter("Plan Type", "plan_type")
region_filter = multiselect_filter("Region", "region")
segment_filter = multiselect_filter("Segment", "segment")

date_min = df["dashboard_date"].min().date()
date_max = df["dashboard_date"].max().date()
date_range = st.sidebar.date_input("Date", value=(date_min, date_max), min_value=date_min, max_value=date_max)

filtered_df = df[
    df["acquisition_channel"].astype(str).isin(channel_filter)
    & df["device"].astype(str).isin(device_filter)
    & df["engagement_band"].astype(str).isin(engagement_filter)
    & df["plan_type"].astype(str).isin(plan_filter)
    & df["region"].astype(str).isin(region_filter)
    & df["segment"].astype(str).isin(segment_filter)
].copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["dashboard_date"] >= start_date)
        & (filtered_df["dashboard_date"] <= end_date)
    ]

if filtered_df.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def pct(x):
    return f"{x:.2f}%"

def money(x):
    return f"${x:,.0f}"

def kpi_card(label, value):
    st.markdown(
        f"""
        <div class='kpi-card'>
            <div class='kpi-label'>{label}</div>
            <div class='kpi-value'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def bar_label(ax, fmt="{:.2f}%", horizontal=False):
    for patch in ax.patches:
        if horizontal:
            value = patch.get_width()
            ax.text(value + max(1, value * 0.02), patch.get_y() + patch.get_height()/2, fmt.format(value), va="center", fontsize=9, fontweight="bold")
        else:
            value = patch.get_height()
            ax.text(patch.get_x() + patch.get_width()/2, value, fmt.format(value), ha="center", va="bottom", fontsize=9, fontweight="bold")

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------
st.markdown(
    """
    <h1 style='text-align:center;'>Churn and Retention Dashboard</h1>
    <p style='text-align:center; color:#4a4a4a;'>Customer retention intelligence, revenue-risk exposure, engagement behavior, and executive decision support.</p>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# KPI Cards
# ---------------------------------------------------------
total_customers = filtered_df["customer_id"].nunique()
churn_rate = filtered_df["churn"].mean() * 100
retention_rate = 100 - churn_rate
revenue_at_risk = filtered_df["revenue_at_risk"].sum()
avg_engagement = filtered_df["engagement_score"].mean()

k1, k2, k3, k4, k5 = st.columns(5)
with k1: kpi_card("Total<br>Customers", f"{total_customers:,.0f}")
with k2: kpi_card("Churn<br>Rate", pct(churn_rate))
with k3: kpi_card("Retention<br>Rate", pct(retention_rate))
with k4: kpi_card("Revenue at<br>Risk", money(revenue_at_risk))
with k5: kpi_card("Avg<br>Engagement", f"{avg_engagement:.2f}")

st.write("")

# ---------------------------------------------------------
# Row 1 Visuals
# ---------------------------------------------------------
row1_col1, row1_col2, row1_col3 = st.columns(3)

with row1_col1:
    st.subheader("Churn Trend")
    trend = (
        filtered_df.assign(month=filtered_df["dashboard_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month")["churn"]
        .mean()
        .mul(100)
        .reset_index(name="churn_rate")
        .sort_values("month")
    )
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(trend["month"], trend["churn_rate"], marker="o", linewidth=2)
    ax.axhline(churn_rate, linewidth=1, linestyle="--")
    ax.text(trend["month"].min(), churn_rate + 0.4, "Average", fontsize=9)
    ax.set_ylabel("Churn Rate")
    ax.set_xlabel("")
    ax.set_ylim(0, max(45, trend["churn_rate"].max() + 5))
    ax.grid(axis="y", alpha=0.25)
    st.pyplot(fig, use_container_width=True)

with row1_col2:
    st.subheader("Segment Churn Rate")
    segment = filtered_df.groupby("segment")["churn"].mean().mul(100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    segment.plot(kind="bar", ax=ax)
    ax.set_ylabel("Churn Rate")
    ax.set_xlabel("")
    ax.set_ylim(0, max(35, segment.max() + 5))
    bar_label(ax)
    st.pyplot(fig, use_container_width=True)

with row1_col3:
    st.subheader("Churn by Tenure")
    tenure_order = ["181+ Days", "91–180 Days", "31–90 Days", "0–30 Days"]
    tenure = filtered_df.groupby("tenure_band")["churn"].mean().mul(100).reindex(tenure_order).dropna()
    fig, ax = plt.subplots(figsize=(6, 4))
    tenure.plot(kind="barh", ax=ax)
    ax.set_xlabel("Churn Rate")
    ax.set_ylabel("")
    ax.set_xlim(0, max(45, tenure.max() + 8))
    bar_label(ax, horizontal=True)
    st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------
# Row 2 Visuals
# ---------------------------------------------------------
row2_col1, row2_col2, row2_col3 = st.columns(3)

with row2_col1:
    st.subheader("Engagement vs Churn")
    engagement_order = ["Low Engagement", "Medium Engagement", "High Engagement"]
    engagement = filtered_df.groupby("engagement_band")["churn"].mean().mul(100).reindex(engagement_order).dropna()
    fig, ax = plt.subplots(figsize=(6, 4))
    engagement.plot(kind="barh", ax=ax)
    ax.axvline(churn_rate, linewidth=1, linestyle="--")
    ax.text(churn_rate + 0.2, -0.35, "Average", fontsize=9)
    ax.set_xlabel("Churn Rate")
    ax.set_ylabel("")
    ax.set_xlim(0, max(45, engagement.max() + 8))
    bar_label(ax, horizontal=True)
    st.pyplot(fig, use_container_width=True)

with row2_col2:
    st.subheader("Revenue Exposure")
    revenue = filtered_df.groupby("segment")["revenue_at_risk"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    revenue.plot(kind="bar", ax=ax)
    ax.set_ylabel("Revenue at Risk")
    ax.set_xlabel("")
    ax.ticklabel_format(style="plain", axis="y")
    for patch in ax.patches:
        value = patch.get_height()
        ax.text(patch.get_x() + patch.get_width()/2, value, money(value), ha="center", va="bottom", fontsize=9, fontweight="bold")
    st.pyplot(fig, use_container_width=True)

with row2_col3:
    st.subheader("Churn Reasons")
    reasons = filtered_df[filtered_df["churn"] == 1]["churn_reason"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(6, 4))
    reasons.plot(kind="barh", ax=ax)
    ax.set_xlabel("Customers")
    ax.set_ylabel("")
    for patch in ax.patches:
        value = patch.get_width()
        ax.text(value + 1, patch.get_y() + patch.get_height()/2, f"{int(value)}", va="center", fontsize=9, fontweight="bold")
    st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------
# Additional Visuals
# ---------------------------------------------------------
st.divider()
st.subheader("Additional Retention Views")

extra1, extra2, extra3 = st.columns(3)

with extra1:
    st.markdown("**Churn by Device**")
    device = filtered_df.groupby("device")["churn"].mean().mul(100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 3.4))
    device.plot(kind="bar", ax=ax)
    ax.set_ylabel("Churn Rate")
    ax.set_xlabel("")
    bar_label(ax)
    st.pyplot(fig, use_container_width=True)

with extra2:
    st.markdown("**Churn by Channel**")
    channel = filtered_df.groupby("acquisition_channel")["churn"].mean().mul(100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 3.4))
    channel.plot(kind="bar", ax=ax)
    ax.set_ylabel("Churn Rate")
    ax.set_xlabel("")
    bar_label(ax)
    st.pyplot(fig, use_container_width=True)

with extra3:
    st.markdown("**Revenue Risk by Region**")
    region = filtered_df.groupby("region")["revenue_at_risk"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(5, 3.4))
    region.plot(kind="bar", ax=ax)
    ax.set_ylabel("Revenue at Risk")
    ax.set_xlabel("")
    st.pyplot(fig, use_container_width=True)

# ---------------------------------------------------------
# Detail Table
# ---------------------------------------------------------
st.divider()
st.subheader("Customer Detail Table")

detail_cols = [
    "customer_id", "segment", "region", "plan_type", "device", "acquisition_channel",
    "engagement_band", "tenure_band", "engagement_score", "revenue",
    "revenue_at_risk", "churn", "churn_reason"
]
st.dataframe(
    filtered_df[detail_cols].sort_values(["revenue_at_risk", "engagement_score"], ascending=[False, True]),
    use_container_width=True,
    height=350
)

# ---------------------------------------------------------
# Insight, Action, Recommendation, Decision
# ---------------------------------------------------------
st.divider()
st.markdown("<h2 style='color:#303241;'>Executive Decision Summary</h2>", unsafe_allow_html=True)

low_engagement_churn = filtered_df[filtered_df["engagement_band"].astype(str) == "Low Engagement"]["churn"].mean() * 100
if np.isnan(low_engagement_churn):
    low_engagement_churn = churn_rate

top_segment = filtered_df.groupby("segment")["revenue_at_risk"].sum().sort_values(ascending=False).index[0]
top_reason = filtered_df[filtered_df["churn"] == 1]["churn_reason"].value_counts().index[0]
top_region = filtered_df.groupby("region")["revenue_at_risk"].sum().sort_values(ascending=False).index[0]

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("### 🔎 Insight")
    st.markdown(
        f"""
        <div class='summary-box insight'>
        Low-engagement customers show a <b>{low_engagement_churn:.2f}% churn rate</b>,
        making engagement decline one of the strongest early warning signals for retention risk.
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:
    st.markdown("### ⚙️ Action")
    st.markdown(
        f"""
        <div class='summary-box action'>
        Monitor customers with declining sessions, low feature usage, short tenure, and churn reason patterns such as <b>{top_reason}</b>.
        </div>
        """,
        unsafe_allow_html=True
    )

with s3:
    st.markdown("### ✅ Recommendation")
    st.markdown(
        f"""
        <div class='summary-box recommendation'>
        Launch targeted retention campaigns for <b>{top_segment}</b> customers and prioritize revenue-risk controls in the <b>{top_region}</b> region.
        </div>
        """,
        unsafe_allow_html=True
    )

with s4:
    st.markdown("### ⭐ Decision")
    st.markdown(
        """
        <div class='summary-box decision'>
        Prioritize retention investment on low-engagement, high-value customers before increasing acquisition spend.
        </div>
        """,
        unsafe_allow_html=True
    )

st.caption("Dashboard focus: churn monitoring, retention intelligence, engagement analysis, revenue-risk exposure, and executive decision support.")
