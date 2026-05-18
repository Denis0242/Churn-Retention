-- Segment churn analysis
SELECT
    segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    AVG(churn_flag) AS churn_rate,
    SUM(revenue_at_risk) AS revenue_at_risk
FROM churn_retention_clean
GROUP BY segment
ORDER BY churn_rate DESC;
