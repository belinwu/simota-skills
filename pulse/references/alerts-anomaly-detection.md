# Pulse Alerts & Anomaly Detection Reference

Real-time alerting and anomaly detection implementation details.

## Alert Definition Template

```markdown
## Alert: [Alert Name]

**Metric:** [Metric being monitored]
**Type:** [Threshold | Anomaly | Trend]
**Severity:** [Critical | Warning | Info]
**Owner:** [Team or person to notify]

### Threshold Configuration

| Condition | Threshold | Time Window | Action |
|-----------|-----------|-------------|--------|
| Below minimum | [value] | [minutes] | [Alert/Page] |
| Above maximum | [value] | [minutes] | [Alert/Page] |
| Rate of change | [%/hour] | [minutes] | [Alert] |

### Notification Channels

| Severity | Primary | Secondary | Escalation |
|----------|---------|-----------|------------|
| Critical | PagerDuty | Slack #alerts | Manager |
| Warning | Slack #alerts | Email | - |
| Info | Slack #metrics | - | - |

### Runbook

1. **Acknowledge** - Confirm alert is valid (not false positive)
2. **Investigate** - Check related metrics and recent deployments
3. **Mitigate** - Apply temporary fix if needed
4. **Resolve** - Address root cause
5. **Document** - Add post-mortem if significant
```

## Alert Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Threshold** | Static upper/lower bounds | Revenue, error rate |
| **Anomaly** | Statistical deviation from baseline | DAU, conversion rate |
| **Trend** | Significant directional change | Session duration, NPS |
| **Missing Data** | Expected events not received | Critical tracking gaps |
| **SLA** | Service level violations | API latency, uptime |

## Anomaly Detection Implementation

```typescript
// lib/alerts/anomaly-detection.ts
interface MetricDataPoint {
  timestamp: Date;
  value: number;
}

interface AnomalyConfig {
  metric: string;
  lookbackDays: number;
  sensitivityLevel: 'low' | 'medium' | 'high';
  minDataPoints: number;
}

interface AnomalyResult {
  isAnomaly: boolean;
  currentValue: number;
  expectedValue: number;
  deviation: number;
  zscore: number;
  confidence: number;
}

// Calculate mean and standard deviation
function calculateStats(values: number[]): { mean: number; stdDev: number } {
  const n = values.length;
  const mean = values.reduce((sum, v) => sum + v, 0) / n;
  const variance = values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / n;
  return { mean, stdDev: Math.sqrt(variance) };
}

// Z-score based anomaly detection
export function detectAnomaly(
  historicalData: MetricDataPoint[],
  currentValue: number,
  config: AnomalyConfig
): AnomalyResult {
  const values = historicalData.map(d => d.value);

  if (values.length < config.minDataPoints) {
    return {
      isAnomaly: false,
      currentValue,
      expectedValue: currentValue,
      deviation: 0,
      zscore: 0,
      confidence: 0
    };
  }

  const { mean, stdDev } = calculateStats(values);
  const zscore = stdDev > 0 ? (currentValue - mean) / stdDev : 0;

  // Sensitivity thresholds
  const thresholds = {
    low: 3.0,
    medium: 2.5,
    high: 2.0
  };

  const threshold = thresholds[config.sensitivityLevel];
  const isAnomaly = Math.abs(zscore) > threshold;
  const confidence = Math.min(1, Math.abs(zscore) / 4);

  return {
    isAnomaly,
    currentValue,
    expectedValue: mean,
    deviation: ((currentValue - mean) / mean) * 100,
    zscore,
    confidence
  };
}

// Moving average anomaly detection (for trend analysis)
export function detectTrendAnomaly(
  data: MetricDataPoint[],
  windowSize: number = 7
): { isTrendChange: boolean; direction: 'up' | 'down' | 'stable'; magnitude: number } {
  if (data.length < windowSize * 2) {
    return { isTrendChange: false, direction: 'stable', magnitude: 0 };
  }

  const recentWindow = data.slice(-windowSize);
  const previousWindow = data.slice(-windowSize * 2, -windowSize);

  const recentAvg = recentWindow.reduce((s, d) => s + d.value, 0) / windowSize;
  const previousAvg = previousWindow.reduce((s, d) => s + d.value, 0) / windowSize;

  const changePercent = ((recentAvg - previousAvg) / previousAvg) * 100;
  const significantChange = Math.abs(changePercent) > 20;

  return {
    isTrendChange: significantChange,
    direction: changePercent > 0 ? 'up' : changePercent < 0 ? 'down' : 'stable',
    magnitude: changePercent
  };
}
```

## Alert Rule Engine

```typescript
// lib/alerts/alert-engine.ts
type AlertSeverity = 'critical' | 'warning' | 'info';
type AlertStatus = 'firing' | 'resolved' | 'acknowledged';

interface AlertRule {
  id: string;
  name: string;
  metric: string;
  condition: AlertCondition;
  severity: AlertSeverity;
  channels: NotificationChannel[];
  cooldownMinutes: number;
  enabled: boolean;
}

type AlertCondition =
  | { type: 'threshold'; operator: '>' | '<' | '>=' | '<='; value: number }
  | { type: 'anomaly'; sensitivity: 'low' | 'medium' | 'high' }
  | { type: 'missing_data'; maxGapMinutes: number }
  | { type: 'rate_of_change'; percentPerHour: number };

interface NotificationChannel {
  type: 'slack' | 'pagerduty' | 'email' | 'webhook';
  config: Record<string, string>;
}

interface Alert {
  id: string;
  ruleId: string;
  ruleName: string;
  status: AlertStatus;
  severity: AlertSeverity;
  metric: string;
  currentValue: number;
  threshold?: number;
  message: string;
  firedAt: Date;
  resolvedAt?: Date;
  acknowledgedBy?: string;
}

class AlertEngine {
  private rules: Map<string, AlertRule> = new Map();
  private activeAlerts: Map<string, Alert> = new Map();
  private cooldowns: Map<string, Date> = new Map();

  addRule(rule: AlertRule): void {
    this.rules.set(rule.id, rule);
  }

  async evaluateMetric(
    metricName: string,
    currentValue: number,
    historicalData?: MetricDataPoint[]
  ): Promise<Alert[]> {
    const newAlerts: Alert[] = [];

    for (const rule of this.rules.values()) {
      if (!rule.enabled || rule.metric !== metricName) continue;
      if (this.isInCooldown(rule.id)) continue;

      const triggered = this.evaluateCondition(
        rule.condition,
        currentValue,
        historicalData
      );

      if (triggered) {
        const alert = this.createAlert(rule, currentValue);
        newAlerts.push(alert);
        this.activeAlerts.set(alert.id, alert);
        this.setCooldown(rule.id, rule.cooldownMinutes);
        await this.sendNotifications(alert, rule.channels);
      }
    }

    return newAlerts;
  }

  private evaluateCondition(
    condition: AlertCondition,
    value: number,
    historical?: MetricDataPoint[]
  ): boolean {
    switch (condition.type) {
      case 'threshold':
        return this.evaluateThreshold(condition, value);
      case 'anomaly':
        if (!historical) return false;
        const result = detectAnomaly(historical, value, {
          metric: '',
          lookbackDays: 14,
          sensitivityLevel: condition.sensitivity,
          minDataPoints: 7
        });
        return result.isAnomaly;
      case 'rate_of_change':
        // Implement rate of change logic
        return false;
      default:
        return false;
    }
  }

  private evaluateThreshold(
    condition: { type: 'threshold'; operator: '>' | '<' | '>=' | '<='; value: number },
    value: number
  ): boolean {
    switch (condition.operator) {
      case '>': return value > condition.value;
      case '<': return value < condition.value;
      case '>=': return value >= condition.value;
      case '<=': return value <= condition.value;
    }
  }

  private createAlert(rule: AlertRule, value: number): Alert {
    return {
      id: `alert_${Date.now()}_${rule.id}`,
      ruleId: rule.id,
      ruleName: rule.name,
      status: 'firing',
      severity: rule.severity,
      metric: rule.metric,
      currentValue: value,
      message: `${rule.name}: ${rule.metric} = ${value}`,
      firedAt: new Date()
    };
  }

  private isInCooldown(ruleId: string): boolean {
    const cooldownEnd = this.cooldowns.get(ruleId);
    return cooldownEnd ? new Date() < cooldownEnd : false;
  }

  private setCooldown(ruleId: string, minutes: number): void {
    const cooldownEnd = new Date(Date.now() + minutes * 60 * 1000);
    this.cooldowns.set(ruleId, cooldownEnd);
  }

  private async sendNotifications(
    alert: Alert,
    channels: NotificationChannel[]
  ): Promise<void> {
    for (const channel of channels) {
      await this.sendToChannel(alert, channel);
    }
  }

  private async sendToChannel(
    alert: Alert,
    channel: NotificationChannel
  ): Promise<void> {
    switch (channel.type) {
      case 'slack':
        await this.sendSlackNotification(alert, channel.config);
        break;
      case 'pagerduty':
        await this.sendPagerDutyNotification(alert, channel.config);
        break;
      case 'email':
        await this.sendEmailNotification(alert, channel.config);
        break;
      case 'webhook':
        await this.sendWebhookNotification(alert, channel.config);
        break;
    }
  }

  private async sendSlackNotification(
    alert: Alert,
    config: Record<string, string>
  ): Promise<void> {
    const color = {
      critical: '#FF0000',
      warning: '#FFA500',
      info: '#0000FF'
    }[alert.severity];

    await fetch(config.webhookUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        attachments: [{
          color,
          title: `[${alert.severity.toUpperCase()}] ${alert.ruleName}`,
          text: alert.message,
          fields: [
            { title: 'Metric', value: alert.metric, short: true },
            { title: 'Value', value: String(alert.currentValue), short: true }
          ],
          ts: Math.floor(alert.firedAt.getTime() / 1000)
        }]
      })
    });
  }

  private async sendPagerDutyNotification(
    alert: Alert,
    config: Record<string, string>
  ): Promise<void> {
    await fetch('https://events.pagerduty.com/v2/enqueue', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        routing_key: config.routingKey,
        event_action: 'trigger',
        dedup_key: alert.ruleId,
        payload: {
          summary: alert.message,
          severity: alert.severity,
          source: 'pulse-alerts',
          custom_details: {
            metric: alert.metric,
            value: alert.currentValue
          }
        }
      })
    });
  }

  private async sendEmailNotification(
    alert: Alert,
    config: Record<string, string>
  ): Promise<void> {
    // Implement email notification via SendGrid, SES, etc.
    console.log(`Email alert to ${config.recipients}: ${alert.message}`);
  }

  private async sendWebhookNotification(
    alert: Alert,
    config: Record<string, string>
  ): Promise<void> {
    await fetch(config.url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(alert)
    });
  }
}

export const alertEngine = new AlertEngine();
```

## Common Alert Configurations

```typescript
// Example alert rules for typical metrics
const commonAlertRules: AlertRule[] = [
  {
    id: 'error_rate_critical',
    name: 'High Error Rate',
    metric: 'error_rate',
    condition: { type: 'threshold', operator: '>', value: 5 },
    severity: 'critical',
    channels: [
      { type: 'pagerduty', config: { routingKey: 'xxx' } },
      { type: 'slack', config: { webhookUrl: 'xxx', channel: '#alerts' } }
    ],
    cooldownMinutes: 15,
    enabled: true
  },
  {
    id: 'dau_anomaly',
    name: 'DAU Anomaly Detection',
    metric: 'daily_active_users',
    condition: { type: 'anomaly', sensitivity: 'medium' },
    severity: 'warning',
    channels: [
      { type: 'slack', config: { webhookUrl: 'xxx', channel: '#metrics' } }
    ],
    cooldownMinutes: 60,
    enabled: true
  },
  {
    id: 'conversion_drop',
    name: 'Conversion Rate Drop',
    metric: 'conversion_rate',
    condition: { type: 'threshold', operator: '<', value: 2.0 },
    severity: 'warning',
    channels: [
      { type: 'slack', config: { webhookUrl: 'xxx', channel: '#growth' } }
    ],
    cooldownMinutes: 30,
    enabled: true
  },
  {
    id: 'revenue_spike',
    name: 'Revenue Anomaly',
    metric: 'daily_revenue',
    condition: { type: 'anomaly', sensitivity: 'high' },
    severity: 'info',
    channels: [
      { type: 'slack', config: { webhookUrl: 'xxx', channel: '#revenue' } }
    ],
    cooldownMinutes: 120,
    enabled: true
  }
];
```
