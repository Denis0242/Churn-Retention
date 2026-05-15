# Churn & Retention Dashboard

## Executive Summary

This project analyzes customer churn, retention performance, engagement behavior, and revenue at risk. It recreates the Tableau dashboard as a Streamlit dashboard and adds a documented EDA workflow, SQL analysis, KPI definitions, and executive decision summary.

## Business Problem

Customer churn reduces recurring revenue and weakens long-term customer value. The business needs to identify which customer groups are most likely to churn, understand why they leave, and decide where to prioritize retention investment.

## KPI Goals

- Total Customers
- Churn Rate
- Retention Rate
- Revenue at Risk
- Average Engagement
- Segment Churn Rate
- Churn by Tenure
- Engagement vs Churn
- Churn Reasons

## Dataset Overview

- Rows: 1,200
- Columns: 24
- Grain: Customer-level churn and engagement records
- Key fields: customer_id, signup_date, last_active_date, tenure_days, segment, plan_type, region, device, acquisition_channel, engagement_score, revenue, lifetime_value, churn, churn_reason

## Data Cleaning & EDA

The EDA includes:

- column standardization
- missing value checks
- duplicate checks
- date conversion
- numeric validation
- categorical validation
- outlier detection
- churn flag validation
- retention rate creation
- tenure band creation
- engagement band creation
- revenue at risk calculation
- cleaned dataset export

See: `docs/EDA.md`

## SQL Transformations

SQL queries are included for:

- KPI summary
- churn trend
- segment churn rate
- churn by tenure
- engagement vs churn
- revenue exposure
- churn reasons
- customer detail table

See: `sql/analysis_queries.sql`

## Metrics Engineering

```text
Churn Rate = churned customers / total customers
Retention Rate = retained customers / total customers
Revenue at Risk = sum(revenue where churn = 1)
Average Engagement = average engagement_score
Segment Churn Rate = churned customers by segment / total customers by segment
```

## Tableau Dashboard Preview

![Churn & Retention Dashboard](screenshots/churn_retention_dashboard.png)

## Streamlit Dashboard Recreation

The Streamlit app includes:

- dashboard filters
- KPI cards
- churn trend
- segment churn rate
- churn by tenure
- engagement vs churn
- revenue exposure
- churn reasons
- additional retention views
- customer detail table
- Insight, Action, Recommendation, and Decision section

Run locally:

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Product Insights

Low-engagement customers create the highest churn risk and should be monitored earlier using engagement, session, feature usage, tenure, and churn reason patterns.

## Insight, Action, Recommendation, Decision

### Insight
Low-engagement customers show the strongest churn risk and create measurable revenue exposure.

### Action
Identify low-engagement customers early using session activity, feature usage, tenure behavior, and churn reasons.

### Recommendation
Launch targeted retention campaigns for low-engagement and high-revenue-risk customers.

### Decision
Prioritize retention investment on low-engagement, high-value customers before increasing acquisition spend.

## Business Impact

This dashboard helps leadership reduce churn risk, protect revenue, improve retention targeting, and make better customer lifecycle decisions.

## Future Improvements

- add predictive churn model
- add cohort retention analysis
- add A/B testing layer
- connect live database
- automate refresh pipeline
