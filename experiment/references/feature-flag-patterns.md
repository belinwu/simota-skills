# Feature Flag Patterns

## Flag Types

| Type | Lifecycle | Example |
|------|-----------|---------|
| Release | Short (days-weeks) | New checkout flow |
| Experiment | Medium (weeks) | A/B test variant |
| Ops | Permanent | Kill switch, rate limit |
| Permission | Permanent | Premium features |

## LaunchDarkly Integration

```typescript
import { init } from 'launchdarkly-js-client-sdk';

const client = init('client-key', { key: userId });

const showNewCheckout = client.variation('new-checkout', false);
```

## Custom Feature Flag

```typescript
interface FeatureFlag {
  key: string;
  enabled: boolean;
  variants?: Record<string, unknown>;
  targeting?: { percentage: number; segments?: string[] };
}
```

## Cleanup Checklist
- [ ] Remove flag evaluation code
- [ ] Remove losing variant code
- [ ] Archive flag in management system
- [ ] Update documentation

---

## Platform Comparison Matrix

| Feature | Statsig | Eppo | GrowthBook | LaunchDarkly |
|---------|---------|------|------------|--------------|
| **Statistical engine** | Sequential testing, CUPED built-in | Frequentist + Bayesian, CUPED | Frequentist (Bayesian optional) | Basic frequentist |
| **Feature flags** | Full (targeting, rollout, kill switch) | Limited (experiment-focused) | Full | Industry-leading |
| **Warehouse-native** | Yes (Snowflake, BigQuery, Redshift) | Yes (primary focus) | Yes | No (event streaming only) |
| **Metrics catalog** | Yes | Yes | Yes | No |
| **Auto-rollback** | Yes | No | No | Yes (via monitoring) |
| **Open source** | No | No | Yes (self-host) | No |
| **Pricing model** | Per event or flat | Per experiment | Free OSS / paid cloud | Per seat |
| **Best for** | Growth teams with high experiment velocity | Data warehouse-centric orgs | Cost-sensitive teams, OSS preference | Enterprise feature management |

### Selection Guide

| Your situation | Recommended platform |
|---------------|---------------------|
| High-velocity experimentation, integrated analytics | **Statsig** |
| All metrics live in data warehouse (Snowflake/BigQuery) | **Eppo** |
| Budget-constrained, want full control | **GrowthBook** (self-hosted) |
| Need mature enterprise FF + SSO + audit logs | **LaunchDarkly** |
| Small team, just need simple feature toggles | Custom implementation (see below) |

---

## Warehouse-Native Integration Pattern

Warehouse-native experimentation analyses experiment results directly in your data warehouse, giving you full control and auditability.

```
┌─────────────┐    exposure events    ┌──────────────────┐
│  Feature    │ ──────────────────▶  │   Data Warehouse  │
│  Flag SDK   │                      │ (Snowflake/BigQuery│
└─────────────┘                      │  /Redshift/etc.)   │
                                     └──────────┬────────┘
                                                │
                                         SQL analysis
                                                │
                                     ┌──────────▼────────┐
                                     │  Experiment Report │
                                     │  (dbt / Jupyter)   │
                                     └───────────────────┘
```

**Exposure table schema:**

```sql
CREATE TABLE experiment_exposures (
  exposure_id       STRING NOT NULL,
  experiment_name   STRING NOT NULL,
  variant           STRING NOT NULL,  -- 'control' | 'treatment'
  user_id           STRING NOT NULL,
  exposed_at        TIMESTAMP NOT NULL,
  session_id        STRING,
  device_type       STRING,
  PRIMARY KEY (experiment_name, user_id)  -- one exposure per user per experiment
);
```

**Analysis query (BigQuery example):**

```sql
WITH exposure AS (
  SELECT
    user_id,
    variant,
    DATE(exposed_at) AS exposure_date
  FROM experiment_exposures
  WHERE experiment_name = 'checkout_redesign'
    AND exposed_at BETWEEN '2024-01-01' AND '2024-01-15'
),
conversions AS (
  SELECT DISTINCT user_id
  FROM order_events
  WHERE event_type = 'purchase'
    AND created_at BETWEEN '2024-01-01' AND '2024-01-22'
)
SELECT
  e.variant,
  COUNT(DISTINCT e.user_id)                         AS users,
  COUNT(DISTINCT c.user_id)                         AS conversions,
  ROUND(COUNT(DISTINCT c.user_id) * 100.0
        / COUNT(DISTINCT e.user_id), 2)             AS conversion_rate_pct
FROM exposure e
LEFT JOIN conversions c USING (user_id)
GROUP BY e.variant
ORDER BY e.variant;
```

---

## Basic Feature Flag Setup

```typescript
// lib/featureFlags.ts
interface FeatureFlag {
  name: string;
  variants: string[];
  allocation: number[];  // Percentage for each variant
  enabled: boolean;
}

const flags: Record<string, FeatureFlag> = {
  'new_checkout_flow': {
    name: 'new_checkout_flow',
    variants: ['control', 'treatment'],
    allocation: [50, 50],
    enabled: true
  }
};

export function getVariant(
  flagName: string,
  userId: string
): string {
  const flag = flags[flagName];
  if (!flag || !flag.enabled) {
    return 'control';
  }

  // Deterministic assignment based on user ID
  const hash = hashUserId(userId, flagName);
  const bucket = hash % 100;

  let cumulative = 0;
  for (let i = 0; i < flag.variants.length; i++) {
    cumulative += flag.allocation[i];
    if (bucket < cumulative) {
      return flag.variants[i];
    }
  }

  return 'control';
}

function hashUserId(userId: string, salt: string): number {
  const str = `${userId}:${salt}`;
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}
```

## React Integration

```tsx
// components/ExperimentProvider.tsx
import { createContext, useContext, ReactNode } from 'react';
import { getVariant } from '@/lib/featureFlags';
import { useUser } from '@/hooks/useUser';
import { trackEvent } from '@/lib/analytics';

interface ExperimentContextValue {
  getExperimentVariant: (experimentName: string) => string;
  trackExposure: (experimentName: string) => void;
}

const ExperimentContext = createContext<ExperimentContextValue | null>(null);

export function ExperimentProvider({ children }: { children: ReactNode }) {
  const { user } = useUser();

  const getExperimentVariant = (experimentName: string): string => {
    return getVariant(experimentName, user?.id || 'anonymous');
  };

  const trackExposure = (experimentName: string): void => {
    const variant = getExperimentVariant(experimentName);
    trackEvent('experiment_exposure', {
      experiment_name: experimentName,
      variant: variant,
      user_id: user?.id
    });
  };

  return (
    <ExperimentContext.Provider value={{ getExperimentVariant, trackExposure }}>
      {children}
    </ExperimentContext.Provider>
  );
}

export function useExperiment(experimentName: string) {
  const context = useContext(ExperimentContext);
  if (!context) {
    throw new Error('useExperiment must be used within ExperimentProvider');
  }

  const variant = context.getExperimentVariant(experimentName);

  // Track exposure on first render
  useEffect(() => {
    context.trackExposure(experimentName);
  }, [experimentName]);

  return {
    variant,
    isControl: variant === 'control',
    isTreatment: variant === 'treatment'
  };
}
```

## Usage Example

```tsx
function CheckoutPage() {
  const { variant, isTreatment } = useExperiment('new_checkout_flow');

  return (
    <div>
      {isTreatment ? (
        <NewCheckoutFlow />
      ) : (
        <CurrentCheckoutFlow />
      )}
    </div>
  );
}
```
