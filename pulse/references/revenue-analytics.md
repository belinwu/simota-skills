# Pulse Revenue Analytics Reference

Revenue metrics, MRR tracking, LTV calculation, and churn analysis implementation.

## Revenue Metrics Framework

```markdown
## Revenue Dashboard

**Purpose:** Comprehensive revenue tracking and analysis
**Audience:** Finance, Product, Executive team
**Refresh:** Daily (MRR), Monthly (LTV)

### Key Revenue Metrics

| Metric | Definition | Formula |
|--------|------------|---------|
| **MRR** | Monthly Recurring Revenue | Sum of all active subscription values |
| **ARR** | Annual Recurring Revenue | MRR x 12 |
| **ARPU** | Average Revenue Per User | MRR / Active paying users |
| **LTV** | Customer Lifetime Value | ARPU x Average customer lifespan |
| **CAC** | Customer Acquisition Cost | Marketing spend / New customers |
| **LTV:CAC** | Return on acquisition | LTV / CAC (target: > 3:1) |

### MRR Movements

| Movement Type | Definition |
|---------------|------------|
| **New MRR** | Revenue from new customers |
| **Expansion MRR** | Upgrades and add-ons |
| **Contraction MRR** | Downgrades |
| **Churned MRR** | Revenue lost from cancellations |
| **Reactivation MRR** | Revenue from returning customers |
| **Net New MRR** | New + Expansion - Contraction - Churned + Reactivation |
```

## MRR Tracking Implementation

```typescript
// lib/revenue/mrr-tracker.ts
interface Subscription {
  id: string;
  userId: string;
  planId: string;
  monthlyValue: number;
  status: 'active' | 'canceled' | 'paused';
  startDate: Date;
  canceledDate?: Date;
  previousPlanId?: string;
  previousValue?: number;
}

interface MRRMovement {
  date: Date;
  newMRR: number;
  expansionMRR: number;
  contractionMRR: number;
  churnedMRR: number;
  reactivationMRR: number;
  netNewMRR: number;
  totalMRR: number;
}

interface MRRBreakdown {
  byPlan: Record<string, number>;
  bySegment: Record<string, number>;
  byCohort: Record<string, number>;
}

class MRRTracker {
  calculateMRRMovements(
    previousSubs: Subscription[],
    currentSubs: Subscription[],
    date: Date
  ): MRRMovement {
    const prevMap = new Map(previousSubs.map(s => [s.userId, s]));
    const currMap = new Map(currentSubs.map(s => [s.userId, s]));

    let newMRR = 0;
    let expansionMRR = 0;
    let contractionMRR = 0;
    let churnedMRR = 0;
    let reactivationMRR = 0;

    // Check current subscriptions
    for (const [userId, curr] of currMap) {
      const prev = prevMap.get(userId);

      if (!prev) {
        // New customer or reactivation
        if (curr.previousPlanId) {
          reactivationMRR += curr.monthlyValue;
        } else {
          newMRR += curr.monthlyValue;
        }
      } else if (curr.monthlyValue > prev.monthlyValue) {
        // Expansion
        expansionMRR += curr.monthlyValue - prev.monthlyValue;
      } else if (curr.monthlyValue < prev.monthlyValue) {
        // Contraction
        contractionMRR += prev.monthlyValue - curr.monthlyValue;
      }
    }

    // Check for churned
    for (const [userId, prev] of prevMap) {
      if (!currMap.has(userId)) {
        churnedMRR += prev.monthlyValue;
      }
    }

    const netNewMRR = newMRR + expansionMRR - contractionMRR - churnedMRR + reactivationMRR;
    const previousTotal = previousSubs
      .filter(s => s.status === 'active')
      .reduce((sum, s) => sum + s.monthlyValue, 0);

    return {
      date,
      newMRR,
      expansionMRR,
      contractionMRR,
      churnedMRR,
      reactivationMRR,
      netNewMRR,
      totalMRR: previousTotal + netNewMRR
    };
  }

  calculateMRRBreakdown(subscriptions: Subscription[]): MRRBreakdown {
    const activeSubscriptions = subscriptions.filter(s => s.status === 'active');

    const byPlan: Record<string, number> = {};
    const bySegment: Record<string, number> = {};
    const byCohort: Record<string, number> = {};

    for (const sub of activeSubscriptions) {
      // By plan
      byPlan[sub.planId] = (byPlan[sub.planId] || 0) + sub.monthlyValue;

      // By cohort (signup month)
      const cohortKey = `${sub.startDate.getFullYear()}-${String(sub.startDate.getMonth() + 1).padStart(2, '0')}`;
      byCohort[cohortKey] = (byCohort[cohortKey] || 0) + sub.monthlyValue;
    }

    return { byPlan, bySegment, byCohort };
  }
}

export const mrrTracker = new MRRTracker();
```

## LTV Calculation

```typescript
// lib/revenue/ltv-calculator.ts
interface CustomerData {
  userId: string;
  cohort: string;  // YYYY-MM format
  firstPurchaseDate: Date;
  lastActivityDate: Date;
  totalRevenue: number;
  subscriptionMonths: number;
  planHistory: Array<{
    planId: string;
    monthlyValue: number;
    startDate: Date;
    endDate?: Date;
  }>;
}

interface CohortLTV {
  cohort: string;
  customersCount: number;
  averageLifespanMonths: number;
  averageMonthlyRevenue: number;
  ltv: number;
  retentionRate: number;
}

class LTVCalculator {
  // Simple historical LTV
  calculateHistoricalLTV(customers: CustomerData[]): number {
    if (customers.length === 0) return 0;

    const totalRevenue = customers.reduce((sum, c) => sum + c.totalRevenue, 0);
    return totalRevenue / customers.length;
  }

  // Cohort-based LTV
  calculateCohortLTV(customers: CustomerData[]): CohortLTV[] {
    const cohorts = new Map<string, CustomerData[]>();

    for (const customer of customers) {
      const cohortCustomers = cohorts.get(customer.cohort) || [];
      cohortCustomers.push(customer);
      cohorts.set(customer.cohort, cohortCustomers);
    }

    const results: CohortLTV[] = [];

    for (const [cohort, cohortCustomers] of cohorts) {
      const avgLifespan = cohortCustomers.reduce(
        (sum, c) => sum + c.subscriptionMonths, 0
      ) / cohortCustomers.length;

      const avgMonthlyRevenue = cohortCustomers.reduce(
        (sum, c) => sum + (c.totalRevenue / Math.max(c.subscriptionMonths, 1)), 0
      ) / cohortCustomers.length;

      const activeCount = cohortCustomers.filter(
        c => c.lastActivityDate > new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)
      ).length;

      results.push({
        cohort,
        customersCount: cohortCustomers.length,
        averageLifespanMonths: Math.round(avgLifespan * 10) / 10,
        averageMonthlyRevenue: Math.round(avgMonthlyRevenue),
        ltv: Math.round(avgLifespan * avgMonthlyRevenue),
        retentionRate: (activeCount / cohortCustomers.length) * 100
      });
    }

    return results.sort((a, b) => b.cohort.localeCompare(a.cohort));
  }

  // Predictive LTV using simple retention model
  calculatePredictiveLTV(
    arpu: number,
    monthlyChurnRate: number,
    discountRate: number = 0.1,  // Annual discount rate
    months: number = 60
  ): number {
    const monthlyDiscount = discountRate / 12;
    let ltv = 0;
    let retentionRate = 1;

    for (let month = 0; month < months; month++) {
      // Discount future revenue
      const discountFactor = Math.pow(1 + monthlyDiscount, -month);
      ltv += arpu * retentionRate * discountFactor;
      retentionRate *= (1 - monthlyChurnRate);
    }

    return Math.round(ltv);
  }

  // LTV by acquisition channel
  calculateLTVByChannel(
    customers: CustomerData[],
    channelMapping: Map<string, string>
  ): Record<string, { ltv: number; customers: number }> {
    const channelData: Record<string, { totalRevenue: number; count: number }> = {};

    for (const customer of customers) {
      const channel = channelMapping.get(customer.userId) || 'unknown';

      if (!channelData[channel]) {
        channelData[channel] = { totalRevenue: 0, count: 0 };
      }

      channelData[channel].totalRevenue += customer.totalRevenue;
      channelData[channel].count += 1;
    }

    const result: Record<string, { ltv: number; customers: number }> = {};

    for (const [channel, data] of Object.entries(channelData)) {
      result[channel] = {
        ltv: Math.round(data.totalRevenue / data.count),
        customers: data.count
      };
    }

    return result;
  }
}

export const ltvCalculator = new LTVCalculator();
```

## Churn Revenue Analysis

```typescript
// lib/revenue/churn-analysis.ts
interface ChurnedCustomer {
  userId: string;
  planId: string;
  monthlyValue: number;
  lifetimeRevenue: number;
  subscriptionMonths: number;
  churnDate: Date;
  churnReason?: string;
  lastActivityDate: Date;
}

interface ChurnAnalysis {
  period: string;
  totalChurnedMRR: number;
  churnedCustomers: number;
  averageLostValue: number;
  churnRate: number;
  byReason: Record<string, { count: number; mrr: number }>;
  byPlan: Record<string, { count: number; mrr: number }>;
  byTenure: Record<string, { count: number; mrr: number }>;
}

class ChurnAnalyzer {
  analyze(
    churnedCustomers: ChurnedCustomer[],
    totalMRR: number,
    totalCustomers: number,
    period: string
  ): ChurnAnalysis {
    const totalChurnedMRR = churnedCustomers.reduce(
      (sum, c) => sum + c.monthlyValue, 0
    );

    // Group by reason
    const byReason: Record<string, { count: number; mrr: number }> = {};
    const byPlan: Record<string, { count: number; mrr: number }> = {};
    const byTenure: Record<string, { count: number; mrr: number }> = {};

    for (const customer of churnedCustomers) {
      // By reason
      const reason = customer.churnReason || 'Unknown';
      if (!byReason[reason]) {
        byReason[reason] = { count: 0, mrr: 0 };
      }
      byReason[reason].count += 1;
      byReason[reason].mrr += customer.monthlyValue;

      // By plan
      if (!byPlan[customer.planId]) {
        byPlan[customer.planId] = { count: 0, mrr: 0 };
      }
      byPlan[customer.planId].count += 1;
      byPlan[customer.planId].mrr += customer.monthlyValue;

      // By tenure bucket
      const tenureBucket = this.getTenureBucket(customer.subscriptionMonths);
      if (!byTenure[tenureBucket]) {
        byTenure[tenureBucket] = { count: 0, mrr: 0 };
      }
      byTenure[tenureBucket].count += 1;
      byTenure[tenureBucket].mrr += customer.monthlyValue;
    }

    return {
      period,
      totalChurnedMRR,
      churnedCustomers: churnedCustomers.length,
      averageLostValue: churnedCustomers.length > 0
        ? totalChurnedMRR / churnedCustomers.length
        : 0,
      churnRate: (churnedCustomers.length / totalCustomers) * 100,
      byReason,
      byPlan,
      byTenure
    };
  }

  private getTenureBucket(months: number): string {
    if (months < 1) return '0-1 month';
    if (months < 3) return '1-3 months';
    if (months < 6) return '3-6 months';
    if (months < 12) return '6-12 months';
    if (months < 24) return '1-2 years';
    return '2+ years';
  }

  // Identify at-risk revenue
  identifyAtRiskRevenue(
    customers: Array<{
      userId: string;
      monthlyValue: number;
      healthScore: number;
      daysSinceLastActivity: number;
    }>,
    healthThreshold: number = 40,
    activityThreshold: number = 14
  ): {
    atRiskMRR: number;
    atRiskCustomers: number;
    customers: Array<{ userId: string; monthlyValue: number; riskLevel: string }>
  } {
    const atRiskCustomers = customers.filter(
      c => c.healthScore < healthThreshold || c.daysSinceLastActivity > activityThreshold
    );

    const result = atRiskCustomers.map(c => ({
      userId: c.userId,
      monthlyValue: c.monthlyValue,
      riskLevel: c.healthScore < 20 ? 'critical'
        : c.healthScore < healthThreshold ? 'high'
        : 'medium'
    }));

    return {
      atRiskMRR: atRiskCustomers.reduce((sum, c) => sum + c.monthlyValue, 0),
      atRiskCustomers: atRiskCustomers.length,
      customers: result
    };
  }
}

export const churnAnalyzer = new ChurnAnalyzer();
```

## Revenue SQL Queries

```sql
-- MRR Movement Analysis (BigQuery)
WITH monthly_mrr AS (
  SELECT
    DATE_TRUNC(subscription_date, MONTH) as month,
    user_id,
    plan_id,
    monthly_value,
    LAG(monthly_value) OVER (PARTITION BY user_id ORDER BY subscription_date) as prev_value,
    LAG(plan_id) OVER (PARTITION BY user_id ORDER BY subscription_date) as prev_plan
  FROM `project.dataset.subscriptions`
  WHERE status = 'active'
)

SELECT
  month,
  -- New MRR
  SUM(CASE WHEN prev_value IS NULL AND prev_plan IS NULL THEN monthly_value ELSE 0 END) as new_mrr,
  -- Expansion MRR
  SUM(CASE WHEN monthly_value > COALESCE(prev_value, 0) AND prev_plan IS NOT NULL
      THEN monthly_value - prev_value ELSE 0 END) as expansion_mrr,
  -- Contraction MRR
  SUM(CASE WHEN monthly_value < prev_value
      THEN prev_value - monthly_value ELSE 0 END) as contraction_mrr,
  -- Total MRR
  SUM(monthly_value) as total_mrr
FROM monthly_mrr
GROUP BY month
ORDER BY month DESC;

-- Cohort Revenue Analysis
WITH user_cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC(first_purchase_date, MONTH) as cohort_month
  FROM `project.dataset.users`
  WHERE first_purchase_date IS NOT NULL
),
monthly_revenue AS (
  SELECT
    user_id,
    DATE_TRUNC(transaction_date, MONTH) as revenue_month,
    SUM(amount) as revenue
  FROM `project.dataset.transactions`
  GROUP BY user_id, revenue_month
)

SELECT
  uc.cohort_month,
  DATE_DIFF(mr.revenue_month, uc.cohort_month, MONTH) as months_since_signup,
  COUNT(DISTINCT uc.user_id) as users,
  SUM(mr.revenue) as total_revenue,
  AVG(mr.revenue) as avg_revenue_per_user
FROM user_cohorts uc
JOIN monthly_revenue mr ON uc.user_id = mr.user_id
WHERE mr.revenue_month >= uc.cohort_month
GROUP BY cohort_month, months_since_signup
ORDER BY cohort_month DESC, months_since_signup;

-- LTV by Acquisition Channel
SELECT
  u.acquisition_channel,
  COUNT(DISTINCT u.user_id) as customers,
  SUM(t.amount) as total_revenue,
  AVG(t.amount) as avg_order_value,
  SUM(t.amount) / COUNT(DISTINCT u.user_id) as ltv,
  AVG(DATE_DIFF(u.last_activity_date, u.signup_date, DAY)) as avg_customer_lifespan_days
FROM `project.dataset.users` u
LEFT JOIN `project.dataset.transactions` t ON u.user_id = t.user_id
GROUP BY acquisition_channel
ORDER BY ltv DESC;
```

## Revenue Tracking Events

```typescript
// Track revenue-related events
interface RevenueEventProperties {
  subscription_started: {
    plan_id: string;
    plan_name: string;
    monthly_value: number;
    billing_cycle: 'monthly' | 'yearly';
    trial_period_days?: number;
    coupon_code?: string;
  };

  subscription_upgraded: {
    previous_plan_id: string;
    new_plan_id: string;
    previous_value: number;
    new_value: number;
    upgrade_reason?: string;
  };

  subscription_downgraded: {
    previous_plan_id: string;
    new_plan_id: string;
    previous_value: number;
    new_value: number;
    downgrade_reason?: string;
  };

  subscription_canceled: {
    plan_id: string;
    monthly_value: number;
    lifetime_value: number;
    subscription_months: number;
    cancellation_reason?: string;
    feedback?: string;
  };

  payment_succeeded: {
    transaction_id: string;
    amount: number;
    currency: string;
    payment_method: string;
    is_recurring: boolean;
  };

  payment_failed: {
    transaction_id: string;
    amount: number;
    failure_reason: string;
    retry_count: number;
  };
}

// Track subscription events
export function trackSubscriptionEvent<K extends keyof RevenueEventProperties>(
  eventName: K,
  properties: RevenueEventProperties[K]
): void {
  trackEvent(eventName, {
    ...properties,
    event_category: 'revenue'
  });
}

// Usage examples
trackSubscriptionEvent('subscription_started', {
  plan_id: 'pro_monthly',
  plan_name: 'Pro Plan',
  monthly_value: 2980,
  billing_cycle: 'monthly'
});

trackSubscriptionEvent('subscription_canceled', {
  plan_id: 'pro_monthly',
  monthly_value: 2980,
  lifetime_value: 35760,
  subscription_months: 12,
  cancellation_reason: 'too_expensive'
});
```
