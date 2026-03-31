# Adaptive Experimentation

## MAB vs A/B Test Selection Framework

Use this table to decide between classical A/B testing and Multi-Armed Bandit (MAB) approaches.

| Criterion | Traditional A/B Test | Multi-Armed Bandit (MAB) |
|-----------|---------------------|--------------------------|
| **Primary goal** | Causal inference, learning | Regret minimization, earning |
| **Reward signal** | Delayed OK (days to weeks) | Immediate required (same session) |
| **Number of variants** | 2-4 | 2-10+ |
| **Traffic allocation** | Fixed (e.g., 50/50) | Dynamic (shifts to winner over time) |
| **Statistical validity** | Strong (frequentist guarantee) | Weaker (no fixed hypothesis) |
| **Experiment duration** | Fixed (pre-calculated) | Flexible (can run indefinitely) |
| **Novelty effect** | Handled with proper duration | Risk of premature convergence |
| **Use cases** | UI redesign, pricing, onboarding | Recommendation, ad selection, content ranking |
| **Interpretability** | High (clear winner/loser) | Lower (probabilistic allocation) |

**Rule of thumb:** Use A/B test when learning matters most; use MAB when earning matters most.

---

## Thompson Sampling Implementation

Thompson Sampling is the recommended MAB algorithm due to its simplicity and strong empirical performance.

**Core concept:** Maintain a Beta distribution for each arm's estimated reward probability. At each step, sample from each arm's distribution and select the arm with the highest sample.

```typescript
// Full implementation is in statistical-methods.md → Thompson Sampling section

// Usage example:
const sampler = new ThompsonSampler(['control', 'checkout_v2', 'checkout_v3']);

// For each user request:
const arm = sampler.selectArm();  // Dynamically selects based on posteriors

// After observing outcome:
sampler.update(arm, reward);  // reward: 1 for conversion, 0 for no conversion

// Monitor progress:
const stats = sampler.getStats();
// [{ name: 'control', estimatedRate: 0.05, uncertainty: 0.002 },
//  { name: 'checkout_v2', estimatedRate: 0.065, uncertainty: 0.001 },
//  ...]
```

**When to stop Thompson Sampling:**

```typescript
interface ConvergenceCheck {
  winner: string | null;    // null if not converged
  confidence: number;       // P(this arm is truly best)
  allocationShare: number;  // Current traffic share going to leading arm
}

function checkConvergence(
  stats: Array<{ name: string; estimatedRate: number; uncertainty: number }>,
  confidenceThreshold = 0.95
): ConvergenceCheck {
  // Monte Carlo: sample 10,000 times, check if one arm consistently wins
  const nSamples = 10_000;
  const winCounts: Record<string, number> = {};

  for (let i = 0; i < nSamples; i++) {
    let bestArm = stats[0].name;
    let bestSample = -Infinity;
    for (const arm of stats) {
      // Sample from arm's posterior (approximate with normal)
      const sample = arm.estimatedRate + arm.uncertainty * gaussianRandom();
      if (sample > bestSample) { bestSample = sample; bestArm = arm.name; }
    }
    winCounts[bestArm] = (winCounts[bestArm] ?? 0) + 1;
  }

  const topArm = Object.entries(winCounts)
    .sort((a, b) => b[1] - a[1])[0];
  const confidence = topArm[1] / nSamples;

  return {
    winner: confidence >= confidenceThreshold ? topArm[0] : null,
    confidence,
    allocationShare: 0 // calculated separately from current allocation
  };
}

function gaussianRandom(): number {
  const u1 = Math.random(), u2 = Math.random();
  return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
}
```

---

## Automatic Stopping Rules

### mSPRT (mixture Sequential Probability Ratio Test)

mSPRT provides valid inference at any stopping time — you can peek continuously without inflating Type I error.

**Key property:** The p-value from mSPRT is valid at any sample size, not just the pre-planned target.

```typescript
interface MSPRTState {
  logLikelihoodRatio: number;
  n: number;
  controlSuccesses: number;
  treatmentSuccesses: number;
}

function updateMSPRT(
  state: MSPRTState,
  controlEvent: 0 | 1,
  treatmentEvent: 0 | 1,
  nullEffect = 0,        // H₀: no effect
  mixingVariance = 0.01  // prior variance on effect size
): MSPRTState & { shouldStop: boolean; pValue: number } {
  const newState: MSPRTState = {
    logLikelihoodRatio: state.logLikelihoodRatio,
    n: state.n + 1,
    controlSuccesses: state.controlSuccesses + controlEvent,
    treatmentSuccesses: state.treatmentSuccesses + treatmentEvent
  };

  // Compute log-likelihood ratio update (simplified for proportions)
  const p0 = (newState.controlSuccesses + 1) / (newState.n + 2);
  const p1 = (newState.treatmentSuccesses + 1) / (newState.n + 2);
  const observedEffect = p1 - p0 - nullEffect;

  // mSPRT statistic: cumulative product of likelihood ratios
  const llrUpdate = observedEffect * observedEffect / (2 * mixingVariance);
  newState.logLikelihoodRatio += llrUpdate;

  // Convert to p-value: p = 1/e^(logLikelihoodRatio)
  const pValue = Math.exp(-newState.logLikelihoodRatio);

  return {
    ...newState,
    shouldStop: pValue < 0.05,
    pValue
  };
}
```

### Always Valid P-values (Confidence Sequences)

A simpler alternative: use confidence sequences that maintain validity at all sample sizes.

```typescript
function alwaysValidPValue(
  control: { conversions: number; total: number },
  treatment: { conversions: number; total: number },
  rho = 0.5  // mixing parameter (0 < rho < 1, smaller = more conservative)
): { pValue: number; isSignificant: boolean } {
  const n = control.total + treatment.total;
  const p1 = control.conversions / control.total;
  const p2 = treatment.conversions / treatment.total;
  const diff = p2 - p1;

  // Boundary that valid p-values must stay below
  const boundary = Math.sqrt((2 * Math.log(1 / rho) + Math.log(n + 1)) / n);
  const zStat = Math.abs(diff) / boundary;

  // Convert to p-value (approximate)
  const pValue = 2 * (1 - normalCDF(zStat));

  return {
    pValue: Math.min(1, pValue),
    isSignificant: Math.abs(diff) > boundary
  };
}

function normalCDF(x: number): number {
  return 0.5 * (1 + erf(x / Math.sqrt(2)));
}

function erf(x: number): number {
  const t = 1 / (1 + 0.3275911 * Math.abs(x));
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t
    - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return x >= 0 ? y : -y;
}
```

---

## Contextual Bandit Overview

Contextual bandits extend MAB by conditioning the arm selection on user context features. This allows personalization: different variants may win for different user segments.

**When to use contextual bandits:**
- Heterogeneous treatment effects are expected (e.g., a feature helps mobile users but hurts desktop)
- User features are available at decision time (device, location, past behavior)
- You have enough traffic to learn per-segment policies (rule of thumb: 10x more traffic than standard A/B)

**Architecture pattern:**

```
User Request
    │
    ▼
Feature Extraction     ← user_id, device, geo, past_behavior
    │
    ▼
Contextual Policy      ← LinUCB, EpsilonGreedy, Neural Bandit
    │
    ▼
Arm Selection          ← variant_A | variant_B | variant_C
    │
    ▼
Reward Observation     ← click, purchase, engagement
    │
    ▼
Policy Update          ← online learning
```

**Simplified LinUCB-inspired approach (TypeScript):**

```typescript
interface ContextualArm {
  name: string;
  // A: covariance matrix (d×d), b: reward vector (d×1)
  A: number[][];
  b: number[];
}

class SimpleContextualBandit {
  private arms: ContextualArm[];
  private alpha: number; // exploration parameter

  constructor(armNames: string[], featureDim: number, alpha = 1.0) {
    this.alpha = alpha;
    this.arms = armNames.map(name => ({
      name,
      A: identityMatrix(featureDim),
      b: new Array(featureDim).fill(0)
    }));
  }

  selectArm(features: number[]): string {
    let bestArm = this.arms[0].name;
    let bestScore = -Infinity;

    for (const arm of this.arms) {
      // UCB score = θᵀx + α * sqrt(xᵀA⁻¹x)
      const theta = solveLinearSystem(arm.A, arm.b);
      const meanReward = dotProduct(theta, features);
      const uncertainty = this.alpha * Math.sqrt(
        dotProduct(features, solveLinearSystem(arm.A, features))
      );
      const score = meanReward + uncertainty;

      if (score > bestScore) { bestScore = score; bestArm = arm.name; }
    }

    return bestArm;
  }

  update(armName: string, features: number[], reward: number): void {
    const arm = this.arms.find(a => a.name === armName);
    if (!arm) return;
    // A += xxᵀ, b += r*x
    for (let i = 0; i < features.length; i++) {
      for (let j = 0; j < features.length; j++) {
        arm.A[i][j] += features[i] * features[j];
      }
      arm.b[i] += reward * features[i];
    }
  }
}

// Placeholder helpers (use a proper linear algebra library in production)
function identityMatrix(n: number): number[][] {
  return Array.from({ length: n }, (_, i) =>
    Array.from({ length: n }, (_, j) => i === j ? 1 : 0)
  );
}

function dotProduct(a: number[], b: number[]): number {
  return a.reduce((sum, v, i) => sum + v * b[i], 0);
}

function solveLinearSystem(A: number[][], b: number[]): number[] {
  // NOTE: Use a real linear algebra library (e.g., mathjs) in production
  // This is a placeholder for the concept
  return b.map((_, i) => b[i] / A[i][i]);
}
```

**Important caveats for contextual bandits:**
- Reward delay creates off-policy evaluation challenges
- Feature selection significantly impacts policy quality
- Evaluation requires offline counterfactual estimation (IPW, DM, DR estimators)
- Consider using proven libraries (Vowpal Wabbit, ML.NET, or cloud ML platforms) over custom implementation
