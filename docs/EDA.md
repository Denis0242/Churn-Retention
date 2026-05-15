# Churn & Retention Dashboard — EDA & Data Cleaning

## 1. Import Libraries

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

## 2. Load Dataset

```python
df = pd.read_csv("data/raw_churn_retention.csv")
```

## 3. Initial Dataset Inspection

```python
df.head()
df.shape
df.info()
df.describe()
df.columns
```

## 4. Standardize Column Names

```python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
)
```

Purpose:

- makes columns easier to reference
- prevents dashboard errors caused by spaces or inconsistent casing
- supports SQL, Python, and Streamlit naming consistency

## 5. Check Missing Values

```python
df.isnull().sum()
```

Cleaning decision:

- categorical missing values are replaced with `Unknown`
- numeric missing values are replaced with the median
- date values are converted with `errors="coerce"`

## 6. Handle Missing Values

```python
categorical_cols = [
    "segment", "plan_type", "region", "device",
    "acquisition_channel", "churn_reason"
]

for col in categorical_cols:
    df[col] = df[col].fillna("Unknown")
```

```python
numeric_cols = [
    "tenure_days", "sessions_last_30d", "avg_session_duration",
    "feature_usage_score", "engagement_score", "revenue",
    "lifetime_value", "churn"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median())
```

## 7. Check and Remove Duplicates

```python
df.duplicated().sum()
df = df.drop_duplicates()
```

Purpose:

- avoids duplicate customers
- protects churn rate accuracy
- prevents revenue at risk from being overstated

## 8. Convert Date Columns

```python
date_cols = ["signup_date", "last_active_date", "churn_date"]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")
```

Purpose:

- supports churn trend analysis
- enables tenure validation
- supports date filtering in Streamlit

## 9. Validate Numeric Ranges

```python
df[[
    "tenure_days", "sessions_last_30d", "avg_session_duration",
    "feature_usage_score", "engagement_score", "revenue",
    "lifetime_value"
]].describe()
```

Validation checks:

- engagement score should be within a reasonable 0–100 scale
- revenue should not be negative
- tenure should not be negative
- sessions should not be negative

```python
df = df[df["tenure_days"] >= 0]
df = df[df["revenue"] >= 0]
df = df[df["sessions_last_30d"] >= 0]
```

## 10. Validate Categorical Columns

```python
for col in ["segment", "plan_type", "region", "device", "acquisition_channel", "churn_reason"]:
    print(col)
    print(df[col].value_counts())
```

Purpose:

- confirms dashboard filter values
- identifies spelling inconsistencies
- validates segmentation categories

## 11. Outlier Detection

```python
df["revenue"].plot(kind="box", title="Revenue Outlier Check")
plt.show()
```

```python
df["engagement_score"].plot(kind="box", title="Engagement Score Outlier Check")
plt.show()
```

```python
df["lifetime_value"].plot(kind="box", title="Lifetime Value Outlier Check")
plt.show()
```

Purpose:

- identifies high-value customers
- highlights unusual revenue-risk records
- checks if extreme values could distort KPIs

## 12. Feature Engineering

### Churn Flag

```python
df["churn"] = df["churn"].astype(int)
df["churn_flag"] = df["churn"]
```

### Retention Flag

```python
df["retention_flag"] = 1 - df["churn_flag"]
```

### Churn Rate and Retention Rate

```python
df["churn_rate"] = df["churn_flag"] * 100
df["retention_rate"] = df["retention_flag"] * 100
```

### Revenue at Risk

```python
df["revenue_at_risk"] = df["revenue"] * df["churn_flag"]
```

### Engagement Band

```python
df["engagement_band"] = pd.cut(
    df["engagement_score"],
    bins=[-1, 25, 50, 100],
    labels=["Low Engagement", "Medium Engagement", "High Engagement"]
)
```

### Tenure Band

```python
df["tenure_band"] = pd.cut(
    df["tenure_days"],
    bins=[-1, 30, 90, 180, np.inf],
    labels=["0–30 Days", "31–90 Days", "91–180 Days", "181+ Days"]
)
```

## 13. KPI Validation

```python
total_customers = df["customer_id"].nunique()
churn_rate = df["churn_flag"].mean() * 100
retention_rate = df["retention_flag"].mean() * 100
revenue_at_risk = df["revenue_at_risk"].sum()
avg_engagement = df["engagement_score"].mean()
```

Purpose:

- validates dashboard KPI cards
- confirms churn and retention formulas
- confirms revenue exposure calculation

## 14. EDA Questions Answered

### What is the overall churn rate?

```python
df["churn_flag"].mean() * 100
```

### Which segment has the highest churn?

```python
df.groupby("segment")["churn_flag"].mean().sort_values(ascending=False) * 100
```

### Which tenure group has the highest churn?

```python
df.groupby("tenure_band")["churn_flag"].mean().sort_values(ascending=False) * 100
```

### Does engagement affect churn?

```python
df.groupby("engagement_band")["churn_flag"].mean().sort_values(ascending=False) * 100
```

### Which churn reasons occur most often?

```python
df[df["churn_flag"] == 1]["churn_reason"].value_counts()
```

## 15. Export Cleaned Dataset

```python
df.to_csv("data/churn_retention.csv", index=False)
```

## Business Insight

Low-engagement customers show higher churn behavior and create revenue-risk exposure across key customer segments.

## Action

Monitor low-engagement customers early using sessions, feature usage, tenure patterns, and churn reason signals.

## Recommendation

Launch targeted retention campaigns for low-engagement and high-revenue-risk customers.

## Decision

Prioritize retention investment on low-engagement, high-value customers before increasing acquisition spend.
