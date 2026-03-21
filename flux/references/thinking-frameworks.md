# Thinking Frameworks

**Purpose:** Definitions, procedures, and application examples for all frameworks used by Flux.
**Read when:** You need to apply a specific framework in the CHALLENGE, COMBINE, or SHIFT phase.

---

## Contents
- Framework Overview
- CHALLENGE Frameworks (Assumption Surfacing)
- COMBINE Frameworks (Cross-Domain Synthesis)
- SHIFT Frameworks (Perspective Rotation)
- Sources

---

## Framework Overview

| # | Framework | Pillar | Origin | Core Mechanism |
|---|-----------|--------|--------|----------------|
| 1 | First Principles | CHALLENGE | Aristotle / Elon Musk | Decompose to fundamental truths, rebuild from scratch |
| 2 | Assumption Reversal | CHALLENGE | IxDF / Creative Problem Solving | List assumptions → flip each → generate ideas |
| 3 | Devil's Advocate / Red Team | CHALLENGE | Catholic Church / Military | Structured opposition to surface weaknesses |
| 4 | Bisociation | COMBINE | Arthur Koestler (1964) | Simultaneous perception in two independent reference frames |
| 5 | SCAMPER | COMBINE | Bob Eberle (1971) | 7 transformation operators on existing concepts |
| 6 | TRIZ | COMBINE | Genrich Altshuller (1946) | Contradiction matrix + 40 inventive principles |
| 7 | Cross-Domain Analogy | COMBINE | Cognitive science | Map structure from source domain to target domain |
| 8 | Lateral Thinking | SHIFT | Edward de Bono (1967) | Random Entry, Provocation PO, Six Thinking Hats |
| 9 | Reframing | SHIFT | NLP / Design Thinking / HBR | Change the frame through which a problem is perceived |
| 10 | Oblique Strategies | SHIFT | Brian Eno & Peter Schmidt (1975) | Random constraint cards to break creative blocks |
| 11 | Multi-Agent Debate | SHIFT | AI research (EduThink4AI, MAD, D3) | Structured adversarial argumentation among agents |

---

## CHALLENGE Frameworks

### 1. First Principles Thinking

**Core idea:** Strip away assumptions until only fundamental, irreducible truths remain. Rebuild solutions from those truths.

**Procedure:**
1. **Identify** the problem or belief.
2. **List all assumptions** embedded in the current understanding (aim for 10-20).
3. **Challenge each assumption**: "Is this actually true? What evidence supports it?"
4. **Decompose** to the most basic, undeniable elements.
5. **Reconstruct** a solution from these elements alone.

**Example:**
- Problem: "Electric cars are too expensive."
- Assumptions: batteries are expensive, we need cobalt, cars need dealerships...
- First Principle: What are the raw material costs of a battery? ($80/kWh at material level)
- Reconstruction: Build batteries from raw materials at scale → dramatically lower cost.

**When to use:** The problem seems impossible under current assumptions. "Everyone knows" framing dominates.

**Source:** Aristotle's Metaphysics; popularized by Elon Musk. See also James Clear's explanation: jamesclear.com/first-principles

---

### 2. Assumption Reversal

**Core idea:** Make implicit assumptions explicit, then systematically reverse each to generate new possibilities.

**Procedure:**
1. **State the problem** clearly.
2. **List 10-20 assumptions** (including "obvious" ones).
3. **Reverse each assumption** ("What if the opposite were true?").
4. **Explore each reversal**: Does it suggest a new approach?
5. **Select promising reversals** for further development.

**Template:**

| # | Assumption | Confidence | Reversal | Insight |
|---|-----------|------------|----------|---------|
| 1 | Users want more features | High | Users want fewer, better features | Simplification as differentiator |
| 2 | We compete on price | Medium | We compete on experience | Premium positioning |
| ... | ... | ... | ... | ... |

**When to use:** Feeling trapped by "how things are done." Need to escape industry conventions.

**Source:** IxDF (Interaction Design Foundation) — Challenge Assumptions method.

---

### 3. Devil's Advocate / Red Team

**Core idea:** Assign a role whose explicit job is to argue against the proposed solution, exposing weaknesses before they become failures.

**Procedure:**
1. **Present** the proposed solution or decision.
2. **Assign Red Team role**: "Your job is to find every reason this will fail."
3. **Systematic attack**: Challenge evidence, identify edge cases, question assumptions, find counterexamples.
4. **Steelman the opposition**: Present the strongest possible case against.
5. **Synthesize**: Integrate valid criticisms into a stronger solution.

**Structured prompts for Red Team:**
- "What's the weakest link in this plan?"
- "Under what conditions does this fail catastrophically?"
- "What are we not seeing because of our position?"
- "If a competitor knew our plan, how would they counter it?"

**When to use:** High-stakes decisions. Groupthink risk. The team is too enthusiastic about an approach.

**Source:** CIA Red Team methodology; ACM research on LLM Devil's Advocate patterns.

---

## COMBINE Frameworks

### 4. Bisociation (Koestler)

**Core idea:** Creative breakthroughs occur when two previously unconnected matrices of thought are suddenly perceived as related.

**Procedure:**
1. **Define Matrix 1**: The problem domain's existing conceptual framework.
2. **Select Matrix 2**: A completely unrelated domain (the more distant, the better).
3. **Map structural parallels**: What roles, processes, or relationships exist in both?
4. **Find the bisociative link**: The unexpected connection that bridges the two.
5. **Generate ideas** from the collision point.

**Domain pairing suggestions:**
- Technology × Biology (biomimicry)
- Business × Sports (team dynamics, training)
- Software × Architecture (structure, load-bearing)
- Education × Gaming (engagement, progression)
- Healthcare × Hospitality (patient/guest experience)

**When to use:** Need radical innovation, not incremental improvement. The problem space feels exhausted.

**Source:** Arthur Koestler, *The Act of Creation* (1964). See The Marginalian's analysis.

---

### 5. SCAMPER

**Core idea:** Apply 7 systematic transformation operators to any existing concept, product, or process.

| Operator | Question | Example |
|----------|----------|---------|
| **S**ubstitute | What can be replaced? | Replace human review with AI triage |
| **C**ombine | What can be merged? | Merge onboarding + first task |
| **A**dapt | What can be borrowed from elsewhere? | Adapt airline boarding for checkout flow |
| **M**odify / Magnify / Minimize | What can be enlarged/reduced? | Minimize form fields to 3 |
| **P**ut to other use | What else could this serve? | Error logs as user research data |
| **E**liminate | What can be removed entirely? | Eliminate registration requirement |
| **R**everse / Rearrange | What if the order changed? | Let users use before signing up |

**Procedure:**
1. Define the target (product, process, feature).
2. Apply each operator systematically.
3. For each: generate 2-3 concrete ideas.
4. Evaluate and select the most promising.

**When to use:** Need to improve or transform something that already exists. Incremental innovation.

**Source:** Bob Eberle (1971), building on Alex Osborn's brainstorming techniques. Wikipedia: SCAMPER.

---

### 6. TRIZ (Theory of Inventive Problem Solving)

**Core idea:** Innovation follows patterns. Most problems contain contradictions that can be resolved using 40 known inventive principles.

**Simplified Procedure for Flux:**
1. **Identify the contradiction**: What two desirable properties conflict? (e.g., "strong but lightweight")
2. **Classify**: Technical contradiction (improving A worsens B) or Physical contradiction (A must be both X and not-X).
3. **Consult the 40 Principles**: Select the most relevant inventive principles.
4. **Generate solutions** guided by the principles.

**Most frequently useful principles (of 40):**

| # | Principle | Description | Example |
|---|-----------|-------------|---------|
| 1 | Segmentation | Divide into independent parts | Microservices from monolith |
| 2 | Taking Out | Extract the disturbing part | Separate auth from business logic |
| 10 | Preliminary Action | Pre-arrange objects for action | Pre-compute expensive calculations |
| 13 | The Other Way Round | Invert the action | Push instead of pull |
| 15 | Dynamics | Allow characteristics to change | Adaptive UI based on usage |
| 17 | Another Dimension | Move to a new dimension | Add time dimension to static data |
| 25 | Self-Service | Object serves itself | Self-healing infrastructure |
| 35 | Parameter Changes | Change state or properties | Lazy loading vs eager loading |
| 40 | Composite Materials | Replace homogeneous with composite | Hybrid cloud architecture |

**When to use:** Two good things seem to conflict. "We can't have both X and Y."

**Source:** Genrich Altshuller (1946). TRIZ40.com for all 40 principles.

---

### 7. Cross-Domain Analogy

**Core idea:** Transfer the structural solution from a well-understood domain to an unfamiliar one.

**Procedure:**
1. **Abstract** the problem to its structural essence (strip domain details).
2. **Search** for domains where a similar structural problem has been solved.
3. **Map** the solution structure back to the original domain.
4. **Adapt** for domain-specific constraints.

**Analogy quality criteria:**
- Structural similarity (not surface similarity)
- Source domain is well-understood
- Mapping preserves key relationships
- Adaptation is feasible

**When to use:** The problem is "new" in its domain but likely solved elsewhere. Need fresh perspective through structural mapping.

---

## SHIFT Frameworks

### 8. Lateral Thinking (de Bono)

**Three key techniques:**

#### Random Entry
1. Select a random word, image, or concept (unrelated to the problem).
2. List its attributes, associations, and properties.
3. Force connections between each attribute and the problem.
4. Develop the most promising connections into ideas.

#### Provocation PO
1. Make a deliberately provocative statement: "PO: [absurd opposite of convention]"
2. Example: "PO: Users should pay us to fix our bugs."
3. Use the provocation as a stepping stone to new ideas.
4. Extract the useful principle behind the absurdity.

#### Six Thinking Hats (abbreviated)
| Hat | Focus | Question |
|-----|-------|----------|
| White | Facts | What data do we have? What's missing? |
| Red | Feelings | What's our gut reaction? |
| Black | Caution | What could go wrong? |
| Yellow | Optimism | What's the best-case scenario? |
| Green | Creativity | What new ideas emerge? |
| Blue | Process | Are we asking the right question? |

**When to use:** Need to break linear thinking. The "obvious" solution path has been exhausted.

**Source:** Edward de Bono, *Lateral Thinking* (1967), *Six Thinking Hats* (1985). de Bono Group.

---

### 9. Reframing

**Core approaches:**

#### E5 Approach (HBR)
1. **Establish** the current frame: "This is a [cost/tech/people/process] problem."
2. **Examine** what's included and excluded by this frame.
3. **Explore** alternative frames: "What if this is actually a [X] problem?"
4. **Evaluate** which frame reveals the most actionable insights.
5. **Execute** under the most productive frame.

#### Iceberg Model
- **Events** (visible): What happened?
- **Patterns** (beneath): What keeps happening?
- **Structures** (deeper): What system enables this pattern?
- **Mental Models** (deepest): What beliefs sustain the structure?

Reframing targets the deepest level possible.

#### Reframing Matrix (4 perspectives)
| Perspective | Question |
|-------------|----------|
| Product | Is the problem in the thing itself? |
| Planning | Is the problem in the approach? |
| Potential | Is the problem in the capability? |
| People | Is the problem in the relationships? |

**When to use:** The problem definition itself may be wrong. "We keep solving the wrong problem."

**Source:** HBR "Are You Solving the Right Problem?" (2012); Design Thinking literature.

---

### 10. Oblique Strategies

**Core idea:** Random constraint cards that disrupt habitual thinking patterns.

**Selected strategies for problem-solving:**

1. "Honor thy error as a hidden intention"
2. "What would your closest friend do?"
3. "Remove specifics and convert to ambiguities"
4. "Use an old idea"
5. "State the problem in words as clearly as possible"
6. "Only one element of each kind"
7. "What would you do if given unlimited resources?"
8. "Reverse the process"
9. "What is the simplest solution?"
10. "Look at the order in which you do things"
11. "What would make this work?"
12. "Emphasize the flaws"
13. "Make what is perfect more human"
14. "What context would restore this to its original meaning?"
15. "Discover the recipes and abandon them"

**Procedure:**
1. Select 1-3 strategies randomly (or use one that creates maximum dissonance with current thinking).
2. Apply each as a constraint or question to the problem.
3. Force at least one idea per strategy.
4. Evaluate which reframing is most productive.

**When to use:** Creative block. Overthinking. Need to "unstick" the process.

**Source:** Brian Eno & Peter Schmidt (1975). Wikipedia: Oblique Strategies.

---

### 11. Multi-Agent Debate

**Core idea:** Multiple agents argue opposing positions, generating insights through structured conflict.

**Patterns:**
- **EduThink4AI**: Collaborative argumentation for educational reasoning.
- **MAD (Multi-Agent Debate)**: Agents with different priors debate iteratively.
- **D3 Framework**: Diverge → Debate → Decide.

**Simplified procedure for Flux:**
1. **Frame** the debate topic.
2. **Assign positions**: Proponent, Opponent, Wildcard (random perspective).
3. **Iterate** 2-3 rounds of argument.
4. **Synthesize** insights from the collision.

**When to use:** Need to stress-test ideas. Want to surface non-obvious counterarguments.

**Source:** Stanford SCALE (EduThink4AI); arXiv (D3 Framework); ACM (LLM Devil's Advocate research).

---

## Sources

| Framework | Primary Source | URL/Reference |
|-----------|---------------|---------------|
| First Principles | Aristotle; James Clear | jamesclear.com/first-principles |
| Assumption Reversal | IxDF | interaction-design.org (Challenge Assumptions) |
| Devil's Advocate | CIA; ACM | ACM Digital Library (LLM Devil's Advocate) |
| Bisociation | Arthur Koestler | The Marginalian (Koestler analysis) |
| SCAMPER | Bob Eberle | Wikipedia: SCAMPER |
| TRIZ | Genrich Altshuller | triz40.com |
| Cross-Domain Analogy | Cognitive Science | Gentner & Markman (1997) |
| Lateral Thinking | Edward de Bono | debono.com; Wikipedia |
| Six Thinking Hats | Edward de Bono | Wikipedia: Six Thinking Hats |
| Reframing | HBR; Design Thinking | HBR "Are You Solving the Right Problem?" (2012) |
| Oblique Strategies | Brian Eno & Peter Schmidt | Wikipedia: Oblique Strategies |
| Multi-Agent Debate | Stanford SCALE; arXiv | EduThink4AI; D3 Framework; MAD |
| Cynefin | Dave Snowden | Wikipedia: Cynefin framework |
