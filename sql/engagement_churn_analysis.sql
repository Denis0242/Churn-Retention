-- Engagement vs churn analysis
SELECT
    CASE
        WHEN engagement_score < 33 THEN 'Low Engagement'
        WHEN engagement_score < 66 THEN 'Medium Engagement'
        ELSE 'High Engagement'
    END AS engagement_band,
    COUNT(*) AS customers,
    ROUND(AVG(sessions_last_30d), 2) AS avg_sessions_last_30d,
    ROUND(AVG(feature_usage_score), 2) AS avg_feature_usage_score,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_pct
FROM churn_retention_data
GROUP BY engagement_band
ORDER BY churn_rate_pct DESC;
