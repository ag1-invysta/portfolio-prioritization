from __future__ import annotations
import itertools
import pandas as pd
from .scoring import score_portfolio

def run_scenarios(
    df: pd.DataFrame,
    scenarios: list[dict],
) -> pd.DataFrame:
    rows = []
    for i, s in enumerate(scenarios, start=1):
        scored = score_portfolio(df, **s)
        top_ids = scored.sort_values("score_final", ascending=False)["id"].tolist()
        for rank, _id in enumerate(top_ids, start=1):
            rows.append({"scenario": f"S{i}", "id": _id, "rank": rank})
    return pd.DataFrame(rows)

def rank_stability(ranks_df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    # stability = fraction of scenarios where item appears in top_n
    grp = ranks_df.groupby("id")["rank"]
    stability = grp.apply(lambda s: (s <= top_n).mean()).rename("stability_top_n")
    avg_rank = grp.mean().rename("avg_rank")
    flips = grp.std().rename("rank_std")
    return pd.concat([stability, avg_rank, flips], axis=1).sort_values(
        ["stability_top_n", "avg_rank"], ascending=[False, True]
    )

def default_scenarios() -> list[dict]:
    # weight sweeps; you can add more later
    return [
        {"w_rice": 0.55, "w_wsjf": 0.25, "w_strategic_fit": 0.20},
        {"w_rice": 0.70, "w_wsjf": 0.10, "w_strategic_fit": 0.20},
        {"w_rice": 0.40, "w_wsjf": 0.40, "w_strategic_fit": 0.20},
        {"w_rice": 0.45, "w_wsjf": 0.15, "w_strategic_fit": 0.40},
    ]

