# Collaboration & Handoff Templates

## Bolt Integration

### Performance Optimization Flow

When Growth identifies performance issues affecting SEO:

1. **Growth identifies** - Core Web Vitals failing or slow page speed
2. **Create proposal** - Document performance bottlenecks
3. **Hand off to Bolt** - `/Bolt optimize performance`
4. **Bolt implements** - Applies performance optimizations

### Growth → Bolt Performance Request

```markdown
## Growth → Bolt Performance Request

**Issue:** [Core Web Vitals failing | Slow page load | Poor mobile performance]

**Current Metrics:**
- LCP: [X.Xs] (target: < 2.5s)
- INP: [Xms] (target: < 200ms)
- CLS: [X.XX] (target: < 0.1)
- PageSpeed Score: [X/100]

**Identified Bottlenecks:**
1. [Large unoptimized images]
2. [Render-blocking JavaScript]
3. [No caching headers]

**Affected Pages:**
- [/page-url] - [specific issue]

**Impact on Growth:**
- SEO ranking affected by Core Web Vitals
- High bounce rate due to slow load

**Requested Optimizations:**
- [ ] Image optimization (WebP, srcset)
- [ ] Code splitting and lazy loading
- [ ] Font optimization
- [ ] Caching strategy

Suggested command: `/Bolt optimize performance`
```

### Growth → Bolt LCP Optimization

```markdown
## Growth → Bolt LCP Optimization

**Current LCP:** [X.Xs]
**Target LCP:** < 2.5s
**LCP Element:** [Hero image | Heading | Video]

**Proposed Fixes:**
1. Preload LCP element
2. Optimize image format/size
3. Implement SSR/SSG for critical content

Suggested command: `/Bolt fix LCP`
```

---

## Canvas Integration

### Conversion Funnel Diagram Request

```
/Canvas create conversion funnel diagram:
- Stages: [Awareness, Interest, Decision, Action]
- Drop-off rates at each stage
- Key metrics per stage
- Optimization opportunities
```

### User Flow Diagram Request

```
/Canvas create user flow diagram for [feature]:
- Entry points
- Decision points
- Conversion paths
- Exit points
- Friction points to optimize
```

### A/B Test Design Diagram Request

```
/Canvas create A/B test diagram:
- Control vs Variant
- Hypothesis
- Primary/secondary metrics
- Sample size requirements
- Test duration
```

### Canvas Output Examples

**Conversion Funnel (Mermaid):**
```mermaid
flowchart TD
    subgraph Awareness
        A[Landing Page Visit]
        A1[100% - 10,000 users]
    end

    subgraph Interest
        B[Scroll to Features]
        B1[60% - 6,000 users]
    end

    subgraph Decision
        C[View Pricing]
        C1[30% - 3,000 users]
    end

    subgraph Action
        D[Click Signup]
        D1[10% - 1,000 users]
        E[Complete Signup]
        E1[5% - 500 users]
    end

    A --> B
    B --> C
    C --> D
    D --> E

    style A fill:#e8f5e9
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#ffebee
    style E fill:#ffebee
```

**A/B Test Design (Mermaid):**
```mermaid
flowchart LR
    subgraph Traffic
        A[Visitors]
    end

    subgraph Split
        B{Random 50/50}
    end

    subgraph Control
        C[Original CTA]
        C1["'Sign Up'"]
        C2[Conversion: 3.2%]
    end

    subgraph Variant
        D[New CTA]
        D1["'Start Free Trial'"]
        D2[Conversion: ?%]
    end

    subgraph Analysis
        E[Statistical Significance]
        F[Winner Declaration]
    end

    A --> B
    B --> C
    B --> D
    C --> E
    D --> E
    E --> F
```

**User Journey (Mermaid):**
```mermaid
journey
    title User Signup Journey
    section Discovery
      Google Search: 5: User
      Click Result: 4: User
      Land on Page: 5: User
    section Evaluation
      Read Hero: 4: User
      Scroll Features: 3: User
      Check Pricing: 3: User
    section Conversion
      Click CTA: 2: User
      Fill Form: 2: User
      Submit: 3: User
    section Activation
      Confirm Email: 4: User
      First Action: 5: User
```

---

## Handoff Templates

### GROWTH_TO_EXPERIMENT_HANDOFF

```markdown
## EXPERIMENT_HANDOFF (from Growth)

### CRO Hypothesis
- **Page:** [URL/component]
- **Current conversion:** [X%]
- **Hypothesis:** [Changing X will improve Y because Z]
- **Proposed variants:** [List of variants]

### Measurement
- **Primary metric:** [Conversion rate of specific action]
- **Secondary metrics:** [Bounce rate, time on page, etc.]

Suggested command: `/Experiment design test for [page]`
```

### GROWTH_TO_BOLT_HANDOFF

```markdown
## BOLT_HANDOFF (from Growth)

### Performance Issues Found
- **Page:** [URL]
- **LCP:** [X ms] (target: < 2500ms)
- **CLS:** [X] (target: < 0.1)
- **INP:** [X ms] (target: < 200ms)

### Priority Fixes
1. [Largest Contentful Paint issue]
2. [Layout shift cause]
3. [Interaction delay cause]

Suggested command: `/Bolt optimize performance for [page]`
```
