from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "churn_retention_data.csv"

def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["signup_date", "last_active_date", "churn_date"])
    df["engagement_band"] = pd.cut(df["engagement_score"], bins=[-1, 33, 66, 101], labels=["Low Engagement", "Medium Engagement", "High Engagement"])
    df["tenure_band"] = pd.cut(df["tenure_days"], bins=[-1, 30, 90, 180, 10000], labels=["0–30 Days", "31–90 Days", "91–180 Days", "181+ Days"])
    return df

def kpis(df):
    churn_rate = df["churn"].mean()
    return {
        "total_customers": len(df),
        "churn_rate": churn_rate,
        "retention_rate": 1 - churn_rate,
        "revenue_at_risk": df.loc[df["churn"] == 1, "revenue"].sum(),
        "avg_engagement": df["engagement_score"].mean(),
    }
