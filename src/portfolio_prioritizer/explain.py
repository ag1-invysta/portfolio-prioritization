from __future__ import annotations
import pandas as pd

def explain_row(row: pd.Series) -> str:
    parts = []
    parts.append(f"Final score {row['score_final']:.3f} driven by base {row['score_base_0to1']:.3f}.")
    parts.append(f"RICE={row['score_rice']:.2f}" + ("" if pd.isna(row["score_wsjf"]) else f", WSJF={row['score_wsjf']:.2f}") + ".")
    parts.append(f"Risk multiplier {row['mult_risk']:.2f}, dependency multiplier {row['mult_dependencies']:.2f}.")
    if row.get("compliance_or_contractual", 0) == 1:
        parts.append("Flagged as contractual/compliance work (mandatory bucket).")
    return " ".join(parts)

def add_explanations(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["explanation"] = out.apply(explain_row, axis=1)
    return out

