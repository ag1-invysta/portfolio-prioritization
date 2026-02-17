# Portfolio Prioritization Tool (AI + Sensitivity)

This tool demonstrates how AI can augment portfolio decision-making through transparent modeling, explicit assumptions, and stress-tested tradeoffs—rather than replacing judgment with opaque automation.

A portfolio prioritization system designed for **program, product, and portfolio-level decision-making**.  It produces transparent, auditable rankings while explicitly separating **value estimation**, **risk policy**, and **organizational constraints**.

This tool is intentionally conservative in its use of AI:  AI is applied only where it is defensible—**learning from historical outcomes** and **stress-testing assumptions**—not for opaque “AI decides” automation.

---

## What this tool does

- Ranks initiatives using a **base value score** derived from multiple lenses:
  - Product value (RICE)
  - Economic urgency (WSJF-like)
  - Strategic alignment
- Applies **explicit policy adjustments** for delivery risk and dependencies
- Separates **mandatory (compliance / contractual)** work from discretionary prioritization
- Optionally trains an **interpretable AI model** on historical outcomes
- Runs **sensitivity analysis** to show ranking stability under different assumptions
- Produces **deterministic explanations** suitable for executive and governance review

---

## Key design principles

- **Explainability first** – every score is traceable to a formula
- **Separation of concerns**
  - Value estimation ≠ risk tolerance ≠ delivery feasibility
- **Relative, not absolute** scoring
  - Rankings are meaningful within a portfolio, not as universal truth
- **Policy knobs, not magic constants**

---

## Repository structure


---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

## Baseline prioritization

portfolio --initiatives data/sample_initiatives.csv --out ranked.csv
portfolio --initiatives data/sample_initiatives.csv \
  --history data/sample_history.csv \
  --run-sensitivity \
  --out ranked_ai.csv

Outputs
- ranked.csv / ranked_ai.csv: Scores, ranks, and explanations per initiative
- rank_stability.csv: Ranking robustness across multiple scenarios

## How weights and risk are applied 

This section clarifies **exactly how weighting and risk adjustments work**, and why they are intentionally separated.

---

### Weighting: what is weighted and when

Weights are applied to **normalized value components**, not to raw values and not directly to the final score.

The calculation flow is:

1. **Compute raw value components**
   - RICE
   - WSJF (if provided)
   - Strategic Fit

2. **Normalize each component across the portfolio**
   - Converts each component to a 0–1 scale
   - Prevents large-scale metrics (e.g., cost of delay) from dominating

3. **Apply weights to the normalized values**
   - This produces the **BaseScore**

4. **Apply risk and dependency multipliers**
   - This produces the **FinalScore**

---

### Base score formula

```math
BaseScore_i =
w_R · Norm(RICE_i)
+ w_W · Norm(WSJF_i)
+ w_S · Norm(StrategicFit_i)

Where:

- w_R, w_W, w_S are portfolio-level weights: what is valued (today)
- Weights sum to 1.0
- BaseScore ∈ [0, 1]
- Scores are relative within the portfolio

Weights represent value preference, e.g.:
- “How much do we care about customer impact vs. economics vs. strategy?”

They do not represent risk tolerance.

### Risk measurement: how confident are we to realizing its value
Step 1: Risk is rated on a 1–5 ordinal scale
- 1 = very low risk
- 5 = very high risk

We want:
 - Risk 1 → no penalty
 - Higher risk → progressively larger penalty

The penalty should be:
- Linear
- Predictable
- Easy to explain

Step 2: shift scale, such that 1 has no penalty
- (Risk - 1) does this

Step 3: apply a per-level penalty
- (arbitrary/tunable) chose 8% per risk level
- e.g, risk 5: (risk -1) x .08 = .32

Step 4: convert penalty to multiplier
- Risk Multiplier = 1 - Penalty
- e.g., risk 5: 1 - .32 = .68 . In this case, this initiative's confidence of realizing value is reduced by ~32%
## Final score formula
- FinalScore(i) = BaseScore(i) × RiskMultiplier(i) × DependencyMultiplier(i)
- Risk and dependencies are applied after value is estimated so that:
- Value judgment and delivery feasibility remain separate
- Risk does not get double-counted
- Sensitivity analysis remains meaningful
