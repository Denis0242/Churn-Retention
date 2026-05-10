-- Revenue exposure by risk group
SELECT
    segment,
    CASE
        WHEN engagement_score < 33 THEN 'Low Engagement'
        WHEN engagement_score < 66 THEN 'Medium Engagement'
        ELSE 'High Engagement'
    END AS engagement_band,
    COUNT(*) AS customers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN churn = 1 THEN revenue ELSE 0 END), 2) AS revenue_at_risk,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_pct
FROM churn_retention_data
GROUP BY segment, engagement_band
ORDER BY revenue_at_risk DESC;
