-- Churn & Retention Analysis Queries

-- 1. KPI Summary
SELECT
    COUNT(DISTINCT customer_id) AS total_customers,
    AVG(churn) * 100 AS churn_rate,
    (1 - AVG(churn)) * 100 AS retention_rate,
    SUM(CASE WHEN churn = 1 THEN revenue ELSE 0 END) AS revenue_at_risk,
    AVG(engagement_score) AS avg_engagement
FROM churn_retention;

-- 2. Churn Trend by Month
SELECT
    DATE_TRUNC('month', COALESCE(churn_date, last_active_date, signup_date)) AS month,
    AVG(churn) * 100 AS churn_rate
FROM churn_retention
GROUP BY 1
ORDER BY 1;

-- 3. Segment Churn Rate
SELECT
    segment,
    COUNT(DISTINCT customer_id) AS customers,
    AVG(churn) * 100 AS churn_rate
FROM churn_retention
GROUP BY segment
ORDER BY churn_rate DESC;

-- 4. Churn by Tenure Band
SELECT
    tenure_band,
    COUNT(DISTINCT customer_id) AS customers,
    AVG(churn) * 100 AS churn_rate
FROM churn_retention
GROUP BY tenure_band
ORDER BY churn_rate DESC;

-- 5. Engagement vs Churn
SELECT
    engagement_band,
    COUNT(DISTINCT customer_id) AS customers,
    AVG(churn) * 100 AS churn_rate
FROM churn_retention
GROUP BY engagement_band
ORDER BY churn_rate DESC;

-- 6. Revenue Exposure
SELECT
    segment,
    SUM(revenue_at_risk) AS revenue_at_risk
FROM churn_retention
GROUP BY segment
ORDER BY revenue_at_risk DESC;

-- 7. Churn Reasons
SELECT
    churn_reason,
    COUNT(*) AS churned_customers
FROM churn_retention
WHERE churn = 1
GROUP BY churn_reason
ORDER BY churned_customers DESC;

-- 8. Customer Detail Table
SELECT
    customer_id,
    segment,
    region,
    plan_type,
    device,
    acquisition_channel,
    engagement_band,
    tenure_band,
    engagement_score,
    revenue,
    revenue_at_risk,
    churn,
    churn_reason
FROM churn_retention
ORDER BY revenue_at_risk DESC, engagement_score ASC;
