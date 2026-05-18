-- KPI Summary: churn, retention, revenue exposure, and engagement
SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    AVG(churn_flag) AS churn_rate,
    1 - AVG(churn_flag) AS retention_rate,
    SUM(revenue_at_risk) AS revenue_at_risk,
    AVG(engagement_score) AS avg_engagement
FROM churn_retention_clean;
