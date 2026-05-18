-- Churn reason analysis
SELECT
    churn_reason,
    COUNT(*) AS churned_customers,
    SUM(revenue_at_risk) AS revenue_at_risk
FROM churn_retention_clean
WHERE churn_flag = 1
GROUP BY churn_reason
ORDER BY churned_customers DESC;
