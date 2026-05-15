# KPI Definitions

## Total Customers
Unique count of customer_id.

## Churn Rate
Churned customers divided by total customers.

```text
Churn Rate = AVG(churn) * 100
```

## Retention Rate
Percentage of customers who did not churn.

```text
Retention Rate = 100 - Churn Rate
```

## Revenue at Risk
Revenue attached to customers who churned.

```text
Revenue at Risk = SUM(revenue where churn = 1)
```

## Average Engagement
Average customer engagement score.

```text
Average Engagement = AVG(engagement_score)
```

## Segment Churn Rate
Average churn rate by segment.

## Churn by Tenure
Average churn rate by tenure band.

## Engagement vs Churn
Average churn rate by engagement band.
