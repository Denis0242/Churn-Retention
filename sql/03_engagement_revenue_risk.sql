-- Engagement band risk analysis
SELECT
    engagement_band,
    COUNT(DISTINCT customer_id) AS total_customers,
    AVG(churn_flag) AS churn_rate,
    AVG(engagement_score) AS avg_engagement,
    SUM(revenue_at_risk) AS revenue_at_risk
FROM churn_retention_clean
GROUP BY engagement_band
ORDER BY churn_rate DESC;
