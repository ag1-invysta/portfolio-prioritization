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
