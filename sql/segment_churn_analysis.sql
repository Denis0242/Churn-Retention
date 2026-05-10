-- Churn rate by business dimensions
SELECT
    segment,
    plan_type,
    region,
    device,
    acquisition_channel,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn = 1 THEN revenue ELSE 0 END), 2) AS revenue_at_risk
FROM churn_retention_data
GROUP BY segment, plan_type, region, device, acquisition_channel
ORDER BY churn_rate_pct DESC;
