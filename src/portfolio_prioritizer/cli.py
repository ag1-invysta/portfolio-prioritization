from __future__ import annotations
import argparse
import pandas as pd

from .scoring import score_portfolio
from .explain import add_explanations
from .sensitivity import default_scenarios, run_scenarios, rank_stability
from .model import train_success_model, predict_success

def main() -> None:
    p = argparse.ArgumentParser(prog="portfolio")
    p.add_argument("--initiatives", required=True, help="Path to initiatives CSV")
    p.add_argument("--history", help="Optional history CSV to train AI model")
    p.add_argument("--out", default="portfolio_ranked.csv", help="Output CSV path")
    p.add_argument("--run-sensitivity", action="store_true", help="Run default sensitivity scenarios")
    args = p.parse_args()

    initiatives = pd.read_csv(args.initiatives)
    scored = score_portfolio(initiatives)
    scored = add_explanations(scored)

    if args.history:
        hist = pd.read_csv(args.history)
        model = train_success_model(hist)
        scored["p_success"] = predict_success(model, scored)
        # Example AI composite: reward high probability and high base value proxy
        scored["ai_score"] = scored["p_success"] * scored["score_final"]
        scored = scored.sort_values(["bucket", "ai_score"], ascending=[True, False])

    scored.to_csv(args.out, index=False)
    print(f"Wrote ranked portfolio to: {args.out}")

    if args.run_sensitivity:
        scenarios = default_scenarios()
        ranks = run_scenarios(initiatives, scenarios)
        stab = rank_stability(ranks, top_n=10)
        stab.to_csv("rank_stability.csv")
        print("Wrote sensitivity output to: rank_stability.csv")

if __name__ == "__main__":
    main()

