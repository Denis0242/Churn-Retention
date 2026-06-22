# Churn & Retention Dashboard

![Dashboard Preview](screenshots/dashboard_preview.png)

# Executive Summary

This project analyzes customer churn and retention behavior to help business, product, and customer success teams identify high-risk customers, improve engagement, reduce preventable churn, and protect recurring revenue.

Using Tableau, SQL, Python, and Streamlit, the analysis evaluates customer behavior across engagement patterns, tenure, churn reasons, revenue exposure, and customer segments to uncover where retention efforts should be prioritized.

The dashboard enables stakeholders to answer key business questions:

* Which customer segments have the highest churn risk?
* Which engagement behaviors indicate future churn?
* Which tenure bands require intervention?
* Which churn reasons deserve immediate attention?
* Which customers create the largest revenue exposure?

The analysis identified:

* $228,489 in observed revenue exposure
* Opportunities capable of supporting an estimated 5–10% churn reduction
* Retention improvements of 3–7% through targeted engagement initiatives

Built using Tableau, SQL, Python, and Streamlit for business intelligence, KPI reporting, and decision-support analytics.

---

# Business Problem

Customer churn creates revenue leakage, reduces customer lifetime value, and weakens long-term business growth.

Business leaders require visibility into:

* High-risk customer segments
* Churn warning signals
* Customer engagement patterns
* Revenue exposure from churn
* Customer lifecycle risk
* Retention opportunities

Without proactive churn monitoring, organizations risk losing valuable customers, increasing acquisition costs, and reducing long-term profitability.

---

# Decision Support Use Case

This dashboard helps business leaders, product teams, and customer success managers monitor retention performance, identify churn drivers, prioritize intervention efforts, and support data-driven decisions designed to improve customer satisfaction, retention, and lifetime value.

---

# KPIs

| KPI             |    Value | Business Purpose                      |
| --------------- | -------: | ------------------------------------- |
| Total Customers |    1,200 | Measures customer base size           |
| Churn Rate      |   73.50% | Measures customer loss risk           |
| Retention Rate  |   26.50% | Measures customer stickiness          |
| Revenue at Risk | $228,489 | Measures financial exposure           |
| Avg Engagement  |    26.25 | Measures customer interaction quality |

---

# Dashboard Overview

The dashboard consists of several analytical views designed to support retention decision-making:

* Executive KPI Scorecards
* Churn Trend Analysis
* Engagement vs Churn Analysis
* Churn by Tenure Analysis
* Revenue Exposure Monitoring
* Churn Reason Analysis
* Customer Risk Prioritization

These views provide a centralized retention analytics solution for leadership reporting and operational decision-making.

---

# Dashboard Screenshots

## Dashboard Preview

![Dashboard Preview](screenshots/dashboard_preview.png)

## KPI Cards

![KPI Cards](screenshots/kpi_cards.png)

## Churn Trend

![Churn Trend](screenshots/churn_trend.png)

## Engagement vs Churn

![Engagement vs Churn](screenshots/engagement_vs_churn.png)

## Churn by Tenure

![Churn by Tenure](screenshots/churn_by_tenure.png)

## Churn Reasons

![Churn Reasons](screenshots/churn_reasons.png)

---

# Key Insights

### Insight 1

Customers with low engagement scores demonstrate significantly higher churn rates than highly engaged customers.

### Insight 2

Specific customer segments contribute disproportionately to overall revenue exposure.

### Insight 3

Early-tenure customers show elevated churn risk, highlighting onboarding improvement opportunities.

### Insight 4

A small number of churn reasons account for the majority of customer loss and require targeted intervention.

---

# Data Dictionary

| Field            | Description                   |
| ---------------- | ----------------------------- |
| customer_id      | Unique customer identifier    |
| segment          | Customer segment              |
| plan_type        | Subscription plan             |
| region           | Geographic region             |
| engagement_score | Customer engagement metric    |
| tenure_days      | Customer lifecycle duration   |
| churn_flag       | Churn indicator               |
| revenue_at_risk  | Revenue exposed to churn      |
| risk_score       | Customer retention risk score |
| risk_category    | Risk classification           |

---

# EDA + Feature Engineering

The project includes a structured 15-step exploratory data analysis and feature engineering workflow.

### EDA Workflow

1. Load Data
2. Dataset Overview
3. Missing Values Analysis
4. Duplicate Validation
5. Datatype Cleaning
6. Column Name Standardization
7. Text Cleaning
8. Outlier Detection
9. Range Validation
10. KPI Validation
11. Feature Engineering
12. Business Logic Validation
13. Summary Statistics
14. Final Dataset Export
15. Insight Summary

### Feature Engineering

Engineered features include:

* churn_flag
* retained_flag
* engagement_band
* tenure_band
* revenue_at_risk
* ltv_at_risk
* risk_score
* risk_category

These metrics improve customer risk monitoring and retention prioritization.

---

# Representative SQL Queries

### KPI Summary

```sql
SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    AVG(churn_flag) AS churn_rate,
    1 - AVG(churn_flag) AS retention_rate,
    SUM(revenue_at_risk) AS revenue_at_risk,
    AVG(engagement_score) AS avg_engagement
FROM churn_retention_clean;
```

### Segment Churn Analysis

```sql
SELECT
    segment,
    COUNT(DISTINCT customer_id) AS customers,
    AVG(churn_flag) AS churn_rate,
    SUM(revenue_at_risk) AS revenue_at_risk
FROM churn_retention_clean
GROUP BY segment
ORDER BY churn_rate DESC;
```

---

# Analytics Workflow

Business Problem

↓

EDA + Cleaning

↓

Feature Engineering

↓

SQL Transformations

↓

Metrics Engineering

↓

Dashboard Development (Tableau)

↓

Streamlit Application

↓

Business Insights

↓

Recommendations

↓

Executive Decision

---

# Business Impact

This dashboard enables stakeholders to:

* Identify opportunities capable of reducing churn by an estimated 5–10%
* Improve customer retention by an estimated 3–7%
* Protect $228,489+ in observed revenue exposure
* Improve customer success prioritization
* Reduce inefficient acquisition spending
* Strengthen KPI-driven decision-making

---

# Recommendations

Implement targeted retention initiatives focused on low-engagement and high-value customers before churn risk escalates in order to reduce revenue leakage and improve customer lifetime value.

---

# Executive Decision Summary

### Insight

Low-engagement customers and selected customer segments show the highest churn exposure and represent meaningful revenue risk.

### Action

Increase monitoring of engagement behavior, tenure patterns, and churn drivers while strengthening intervention timing.

### Recommendation

Deploy proactive retention campaigns for high-risk customer groups before churn risk escalates.

### Decision

Prioritize retention investment before acquisition spending to improve customer lifetime value and reduce revenue leakage.

---

# Tools Used

* SQL
* Tableau
* Python
* Pandas
* Streamlit
* GitHub

---

# Repository Structure

```text
churn-retention-dashboard/
├── app/
├── data/
├── notebooks/
├── screenshots/
├── sql/
├── README.md
└── requirements.txt
```

---

# How to Run the Project

```bash
git clone https://github.com/Denis0242/Churn-Retention

pip install -r requirements.txt

streamlit run app/streamlit_app.py
```

---

# Future Improvements

* Add churn prediction models
* Add retention cohort analysis
* Add customer-level churn scoring
* Add A/B testing readouts
* Connect to Snowflake or Redshift
* Build executive alerting capabilities
* Add experimentation reporting

---

# Disclaimer

* Dataset is synthetic and created for portfolio purposes.
* No real customer information is included.
* Project developed for educational and demonstration purposes.
* Business impact estimates are illustrative and intended to demonstrate analytical decision-making.

