-- Tenure band lifecycle churn analysis
WITH tenure_bands AS (
    SELECT
        *,
        CASE
            WHEN tenure_days BETWEEN 0 AND 30 THEN '0–30 Days'
            WHEN tenure_days BETWEEN 31 AND 90 THEN '31–90 Days'
            WHEN tenure_days BETWEEN 91 AND 180 THEN '91–180 Days'
            ELSE '181+ Days'
        END AS tenure_band
    FROM churn_retention_data
)
SELECT
    tenure_band,
    COUNT(*) AS customers,
    SUM(churn) AS churned_customers,
    ROUND(AVG(churn) * 100, 2) AS churn_rate_pct,
    ROUND((1 - AVG(churn)) * 100, 2) AS retention_rate_pct
FROM tenure_bands
GROUP BY tenure_band
ORDER BY churn_rate_pct DESC;
