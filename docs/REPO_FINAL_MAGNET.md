# REPO_FINAL_MAGNET.md
## Recruiter‑Magnet Repo Formula vFinal
### Designed For: Data Analyst (Healthcare & Tech) with Product Analytics Skills

---

# PURPOSE

Every repository should feel like a:

> Real-world analytics decision-support system

—not just a dashboard project.

The goal of every repository is to demonstrate:

- Product Analytics Thinking
- Business Thinking
- KPI Monitoring
- Funnel & Retention Analysis
- Dashboard Storytelling
- Decision Support
- Healthcare & Tech Analytics
- Executive-Level Insights
- Technical Polish (SQL + Tableau + Python + Streamlit)

---

# FINAL REPO MAGNET STRUCTURE

## 1. Executive Summary

### Purpose
Recruiter hook.

### Permanent Rule
Executive Summary must always sound:

```text
Business + Product + Outcome focused
```

### Include
- Business problem
- Product or operational context
- KPIs analyzed
- Decision supported
- Expected business outcome

### Standard Structure

```text
This project analyzes [business problem] to help [stakeholder/team] improve [business or product outcome].

The dashboard evaluates [KPIs] to identify [problem/opportunity].

Insights from this analysis support decisions around [decision].

Expected impact includes [business outcome].

Built using Tableau, SQL, Python, and Streamlit.
```

---

## 2. Business Problem

Every repo must answer:

```text
What happened?
Why does it matter?
Who is affected?
What decision should leadership make?
```

Examples:

### Experimentation
```text
Which experiment variant should ship?
```

### Funnel / Journey
```text
Where are users dropping off?
```

### Churn
```text
Which customers are likely to churn?
```

### Claims / Healthcare
```text
What drives cost or operational risk?
```

---

## 3. KPI Goals

Always use a KPI table.

```markdown
| KPI | Business Purpose |
|---|---|
| Conversion Rate | Measures user action completion |
| Retention Rate | Measures customer stickiness |
| Churn Rate | Measures customer loss risk |
| Revenue Per User | Measures monetization |
| Claim Cost | Measures financial exposure |
| Engagement Rate | Measures product interaction |
```

---

## 4. Dataset Overview

Include:

- Dataset name
- Rows
- Columns
- Date range
- Key fields
- Business meaning

---

## 5. EDA + Cleaning + Feature Engineering Notebook

### Mandatory Folder

```text
notebooks/
└── eda_cleaning_feature_engineering.ipynb
```

### Required Notebook Order

```text
1. Load Data
2. Dataset Overview
3. Missing Values
4. Duplicates
5. Datatype Cleaning
6. Column Cleaning
7. Text Cleaning
8. Outlier Detection
9. Range Validation
10. KPI Validation
11. Feature Engineering
12. Business Logic Validation
13. Summary Statistics
14. Final Clean Dataset Export
15. Insight Summary
```

### Feature Engineering Examples

```text
risk_flag
churn_flag
retention_rate
conversion_rate
dropoff_rate
revenue_per_user
cost_band
risk_category
decision_signal
```

---

## 6. SQL Transformations

### Rule
Every repo must include:

```text
3–4 representative SQL queries
```

The queries should:

```text
Match dashboard visuals
Stay recruiter-readable
Remain business-focused
Avoid unnecessary complexity
```

### Representative SQL Examples

#### 1. KPI Summary Query

```sql
SELECT
    experiment_name,
    experiment_group,
    AVG(conversion_rate) AS conversion_rate,
    AVG(confidence_level) AS confidence,
    AVG(lift_percentage) AS lift
FROM experimentation
GROUP BY 1,2;
```

Purpose:

```text
Shows experiment performance by variant.
```

#### 2. Trend Analysis Query

```sql
SELECT
    event_date,
    AVG(conversion_rate) AS conversion_rate,
    AVG(revenue_per_user) AS revenue_per_user
FROM experimentation
GROUP BY 1
ORDER BY 1;
```

Purpose:

```text
Tracks KPI trends over time.
```

#### 3. Segment Performance Query

```sql
SELECT
    customer_segment,
    AVG(retention_rate) AS retention_rate,
    AVG(revenue_per_user) AS revenue_per_user
FROM experimentation
GROUP BY 1;
```

Purpose:

```text
Shows which customer segment performs best.
```

#### 4. Decision Signal Query

```sql
SELECT
    decision_signal,
    COUNT(*) AS total_experiments
FROM experimentation
GROUP BY 1;
```

Purpose:

```text
Supports executive decision-making.
```

---

## 7. Metrics Engineering

Define KPI formulas clearly.

```text
Conversion Rate = Converted Users / Total Users
Retention Rate = Retained Users / Total Users
Churn Rate = 1 - Retention Rate
Revenue Per User = Revenue / Users
Lift = Variant - Control
Risk Score = Weighted Risk Components
```

---

## 8. Analytics Workflow

```text
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
Dashboard Build
        ↓
Insights
        ↓
Decision Support
        ↓
Business Impact
```

---

## 9. Dashboard Preview

### Required Screenshots

```text
screenshots/
├── dashboard_preview.png
├── kpi_overview.png
├── trend_or_funnel.png
└── segment_or_risk_view.png
```

### Standard

Include:

1. Main Dashboard Screenshot
2. KPI Overview Screenshot
3. Trend / Funnel Screenshot
4. Segment / Risk Screenshot

Purpose:

```text
Show recruiters dashboard depth
without opening Tableau.
```

---

## 10. Streamlit App Recreation

### Rule
Streamlit must closely recreate Tableau dashboard.

Must match:

```text
Same colors
Same layout
Same KPI cards
Same chart order
Same business story
Same executive summary
```

### Folder

```text
app/
└── streamlit_app.py
```

---

## 11. Executive Decision Summary

Every Streamlit app must include:

```text
Insight | Action | Recommendation | Decision
```

### Style

```text
Insight → Light Blue
Action → Light Yellow
Recommendation → Light Green
Decision → Light Red/Pink
```

---

## 12. Product Insights

Use business language.

Bad:

```text
Conversion increased.
```

Better:

```text
Variant B improved conversion while maintaining healthy retention, making it a stronger candidate for rollout.
```

---

## 13. Insight → Action → Recommendation → Decision

Required format:

```markdown
### Insight
What happened?

### Action
What should the business monitor?

### Recommendation
What should leadership implement?

### Decision
Ship / Improve / Monitor / Review
```

---

## 14. Decision Framework

Example:

```text
Ship        = Strong KPI improvement + acceptable risk
Promising   = Positive signal but needs more evidence
Review      = Mixed performance or elevated risk
Do Not Ship = Weak performance or harmful outcome
```

---

## 15. Business Impact

### Permanent Rule
Business impact must be:

```text
Measurable
Business-oriented
Outcome-focused
```

Bad:

```text
Improves decision-making.
```

Better:

```text
Could improve conversion by 5–10%, reduce churn by 3–7%, lower claim cost exposure, or improve retention outcomes.
```

Examples:

- Reduced churn risk by X%
- Increased retention by X%
- Reduced claim cost exposure by X%
- Improved conversion by X%
- Increased revenue per user by X%

---

## 16. Repo Architecture

```text
project-name/
├── data/
├── sql/
├── notebooks/
│   └── eda_cleaning_feature_engineering.ipynb
├── dashboard/
├── screenshots/
│   ├── dashboard_preview.png
│   ├── kpi_overview.png
│   ├── trend_or_funnel.png
│   └── segment_or_risk_view.png
├── app/
│   └── streamlit_app.py
├── docs/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 17. Automation Awareness

Keep lightweight.

Examples:

```text
Scheduled SQL jobs
Python scripts
Prefect pipelines
Automated dashboard refresh
```

---

## 18. Future Improvements

Include realistic improvements.

Examples:

```text
Add predictive model
Add cohort analysis
Add statistical testing
Add live database connection
```

---

# FINAL REPO MAGNET STANDARD

Every repo should include:

```text
README.md
EDA notebook (.ipynb)
3–4 representative SQL queries
Main dashboard screenshot
2–3 supporting dashboard screenshots
Matching Streamlit recreation
Executive decision summary
Measurable business impact
Future improvements
```

Every repo should communicate:

> I can clean data, analyze KPIs, write SQL, build dashboards, recreate analytics in Streamlit, explain insights, recommend actions, and support business decisions.

