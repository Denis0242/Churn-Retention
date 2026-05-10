-- Core churn and retention KPIs
SELECT
    COUNT(*) AS total_customers,
    SUM(churn) AS churned_customers,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_pct,
    ROUND((1 - AVG(churn)) * 100, 2) AS retention_rate_pct,
    ROUND(SUM(CASE WHEN churn = 1 THEN revenue ELSE 0 END), 2) AS revenue_at_risk,
    ROUND(AVG(engagement_score), 2) AS avg_engagement_score
FROM churn_retention_data;
