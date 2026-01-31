# Pulse Data Quality Monitoring Reference

Data quality framework and monitoring implementation.

## Data Quality Framework

```markdown
## Data Quality Dashboard

**Purpose:** Monitor tracking data reliability and completeness
**Refresh:** Hourly
**Owner:** Analytics team

### Quality Dimensions

| Dimension | Definition | Target | Alert Threshold |
|-----------|------------|--------|-----------------|
| **Completeness** | % of expected events received | 99% | < 95% |
| **Timeliness** | Data delay from event to availability | < 5 min | > 15 min |
| **Validity** | % of events passing schema validation | 99.5% | < 98% |
| **Uniqueness** | % of distinct events (no duplicates) | 99.9% | < 99% |
| **Consistency** | Cross-platform data agreement | 95% | < 90% |

### Event Coverage Matrix

| Event | Expected Volume/Day | Actual | Coverage % | Status |
|-------|---------------------|--------|------------|--------|
| page_viewed | 100,000 | 98,500 | 98.5% | OK |
| user_signed_up | 500 | 495 | 99.0% | OK |
| checkout_completed | 1,000 | 950 | 95.0% | Warning |
| feature_used | 50,000 | 48,000 | 96.0% | OK |
```

## Schema Validation

```typescript
// lib/data-quality/schema-validator.ts
import { z } from 'zod';

// Base event schema
const BaseEventSchema = z.object({
  event_name: z.string().min(1),
  timestamp: z.string().datetime(),
  anonymous_id: z.string().uuid(),
  user_id: z.string().optional(),
  context: z.object({
    page_url: z.string().url(),
    page_title: z.string(),
    user_agent: z.string(),
    locale: z.string(),
    timezone: z.string()
  })
});

// Event-specific schemas
const EventSchemas = {
  page_viewed: BaseEventSchema.extend({
    properties: z.object({
      page_path: z.string(),
      page_title: z.string(),
      referrer: z.string().optional()
    })
  }),

  user_signed_up: BaseEventSchema.extend({
    properties: z.object({
      signup_method: z.enum(['email', 'google', 'apple', 'github']),
      plan_type: z.enum(['free', 'pro', 'enterprise']),
      referral_source: z.string().optional()
    })
  }),

  checkout_completed: BaseEventSchema.extend({
    properties: z.object({
      order_id: z.string(),
      total_amount: z.number().positive(),
      currency: z.enum(['JPY', 'USD', 'EUR']),
      item_count: z.number().int().positive(),
      payment_method: z.string(),
      coupon_code: z.string().optional()
    })
  }),

  feature_used: BaseEventSchema.extend({
    properties: z.object({
      feature_name: z.string(),
      feature_version: z.string().optional(),
      duration_seconds: z.number().optional(),
      success: z.boolean()
    })
  })
};

interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

interface ValidationError {
  field: string;
  message: string;
  received: unknown;
}

interface ValidationWarning {
  field: string;
  message: string;
}

export function validateEvent(
  eventName: string,
  eventData: unknown
): ValidationResult {
  const schema = EventSchemas[eventName as keyof typeof EventSchemas];

  if (!schema) {
    return {
      isValid: false,
      errors: [{ field: 'event_name', message: `Unknown event: ${eventName}`, received: eventName }],
      warnings: []
    };
  }

  const result = schema.safeParse(eventData);

  if (result.success) {
    return { isValid: true, errors: [], warnings: [] };
  }

  const errors: ValidationError[] = result.error.issues.map(issue => ({
    field: issue.path.join('.'),
    message: issue.message,
    received: issue.code === 'invalid_type' ? (issue as any).received : undefined
  }));

  return { isValid: false, errors, warnings: [] };
}

// Batch validation with summary
export function validateEventBatch(
  events: Array<{ event_name: string; data: unknown }>
): {
  totalEvents: number;
  validEvents: number;
  invalidEvents: number;
  validationRate: number;
  errorsByType: Record<string, number>;
} {
  let validCount = 0;
  const errorsByType: Record<string, number> = {};

  for (const event of events) {
    const result = validateEvent(event.event_name, event.data);
    if (result.isValid) {
      validCount++;
    } else {
      for (const error of result.errors) {
        const key = `${event.event_name}.${error.field}`;
        errorsByType[key] = (errorsByType[key] || 0) + 1;
      }
    }
  }

  return {
    totalEvents: events.length,
    validEvents: validCount,
    invalidEvents: events.length - validCount,
    validationRate: (validCount / events.length) * 100,
    errorsByType
  };
}
```

## Data Freshness Monitor

```typescript
// lib/data-quality/freshness-monitor.ts
interface FreshnessConfig {
  eventName: string;
  expectedIntervalMinutes: number;
  maxDelayMinutes: number;
}

interface FreshnessStatus {
  eventName: string;
  lastSeenAt: Date | null;
  minutesSinceLastEvent: number;
  status: 'healthy' | 'stale' | 'missing';
  expectedInterval: number;
}

class FreshnessMonitor {
  private lastEventTimes: Map<string, Date> = new Map();
  private configs: FreshnessConfig[] = [];

  configure(configs: FreshnessConfig[]): void {
    this.configs = configs;
  }

  recordEvent(eventName: string): void {
    this.lastEventTimes.set(eventName, new Date());
  }

  checkFreshness(): FreshnessStatus[] {
    const now = new Date();

    return this.configs.map(config => {
      const lastSeen = this.lastEventTimes.get(config.eventName);
      const minutesSince = lastSeen
        ? (now.getTime() - lastSeen.getTime()) / (1000 * 60)
        : Infinity;

      let status: 'healthy' | 'stale' | 'missing';
      if (!lastSeen) {
        status = 'missing';
      } else if (minutesSince > config.maxDelayMinutes) {
        status = 'stale';
      } else {
        status = 'healthy';
      }

      return {
        eventName: config.eventName,
        lastSeenAt: lastSeen || null,
        minutesSinceLastEvent: Math.round(minutesSince),
        status,
        expectedInterval: config.expectedIntervalMinutes
      };
    });
  }

  getStaleEvents(): FreshnessStatus[] {
    return this.checkFreshness().filter(s => s.status !== 'healthy');
  }
}

// Example configuration
const freshnessConfigs: FreshnessConfig[] = [
  { eventName: 'page_viewed', expectedIntervalMinutes: 1, maxDelayMinutes: 5 },
  { eventName: 'user_signed_up', expectedIntervalMinutes: 60, maxDelayMinutes: 180 },
  { eventName: 'checkout_completed', expectedIntervalMinutes: 30, maxDelayMinutes: 120 },
  { eventName: 'session_started', expectedIntervalMinutes: 1, maxDelayMinutes: 5 }
];

export const freshnessMonitor = new FreshnessMonitor();
freshnessMonitor.configure(freshnessConfigs);
```

## Event Volume Tracking

```typescript
// lib/data-quality/volume-tracker.ts
interface VolumeBaseline {
  eventName: string;
  hourlyBaseline: number[];  // 24 hours
  dailyBaseline: number;
  weeklyPattern: number[];   // 7 days (0 = Sunday)
  stdDeviation: number;
}

interface VolumeAnomaly {
  eventName: string;
  currentVolume: number;
  expectedVolume: number;
  deviationPercent: number;
  isAnomaly: boolean;
  direction: 'high' | 'low' | 'normal';
}

class VolumeTracker {
  private baselines: Map<string, VolumeBaseline> = new Map();
  private currentHourCounts: Map<string, number> = new Map();

  setBaseline(baseline: VolumeBaseline): void {
    this.baselines.set(baseline.eventName, baseline);
  }

  incrementCount(eventName: string): void {
    const current = this.currentHourCounts.get(eventName) || 0;
    this.currentHourCounts.set(eventName, current + 1);
  }

  checkVolume(eventName: string): VolumeAnomaly | null {
    const baseline = this.baselines.get(eventName);
    if (!baseline) return null;

    const currentVolume = this.currentHourCounts.get(eventName) || 0;
    const hour = new Date().getHours();
    const dayOfWeek = new Date().getDay();

    // Adjust expected volume by hour and day of week
    const hourlyFactor = baseline.hourlyBaseline[hour] /
      (baseline.hourlyBaseline.reduce((a, b) => a + b, 0) / 24);
    const dailyFactor = baseline.weeklyPattern[dayOfWeek] /
      (baseline.weeklyPattern.reduce((a, b) => a + b, 0) / 7);

    const expectedVolume = (baseline.dailyBaseline / 24) * hourlyFactor * dailyFactor;
    const deviation = ((currentVolume - expectedVolume) / expectedVolume) * 100;

    // Use 2 standard deviations as threshold
    const threshold = (baseline.stdDeviation / expectedVolume) * 100 * 2;
    const isAnomaly = Math.abs(deviation) > threshold;

    return {
      eventName,
      currentVolume,
      expectedVolume: Math.round(expectedVolume),
      deviationPercent: Math.round(deviation),
      isAnomaly,
      direction: deviation > threshold ? 'high' : deviation < -threshold ? 'low' : 'normal'
    };
  }

  getAnomalies(): VolumeAnomaly[] {
    const anomalies: VolumeAnomaly[] = [];

    for (const eventName of this.baselines.keys()) {
      const result = this.checkVolume(eventName);
      if (result?.isAnomaly) {
        anomalies.push(result);
      }
    }

    return anomalies;
  }

  resetHourlyCounts(): void {
    this.currentHourCounts.clear();
  }
}

export const volumeTracker = new VolumeTracker();
```

## Data Quality Dashboard SQL

```sql
-- BigQuery: Data Quality Summary
WITH event_stats AS (
  SELECT
    event_name,
    DATE(event_timestamp) as event_date,
    COUNT(*) as event_count,
    COUNT(DISTINCT user_id) as unique_users,
    COUNTIF(user_id IS NULL) as anonymous_events,
    AVG(TIMESTAMP_DIFF(ingestion_timestamp, event_timestamp, SECOND)) as avg_latency_seconds
  FROM `project.dataset.events`
  WHERE DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY event_name, event_date
),

validation_stats AS (
  SELECT
    event_name,
    DATE(event_timestamp) as event_date,
    COUNTIF(validation_status = 'valid') as valid_events,
    COUNTIF(validation_status = 'invalid') as invalid_events
  FROM `project.dataset.event_validation_log`
  WHERE DATE(event_timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
  GROUP BY event_name, event_date
)

SELECT
  e.event_name,
  e.event_date,
  e.event_count,
  e.unique_users,
  ROUND(e.anonymous_events / e.event_count * 100, 2) as anonymous_rate_pct,
  ROUND(e.avg_latency_seconds, 2) as avg_latency_sec,
  ROUND(v.valid_events / (v.valid_events + v.invalid_events) * 100, 2) as validation_rate_pct,
  -- Compare to previous week
  LAG(e.event_count, 7) OVER (PARTITION BY e.event_name ORDER BY e.event_date) as prev_week_count,
  ROUND((e.event_count - LAG(e.event_count, 7) OVER (PARTITION BY e.event_name ORDER BY e.event_date))
    / LAG(e.event_count, 7) OVER (PARTITION BY e.event_name ORDER BY e.event_date) * 100, 2) as wow_change_pct
FROM event_stats e
LEFT JOIN validation_stats v ON e.event_name = v.event_name AND e.event_date = v.event_date
ORDER BY e.event_date DESC, e.event_name;
```
