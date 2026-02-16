from __future__ import annotations
import numpy as np
import pandas as pd

REQUIRED_COLS = [
    "id", "title", "effort_person_weeks", "reach_users", "impact_1to5",
    "confidence_0to1", "risk_1to5", "strategic_fit_1to5",
    "dependency_count", "compliance_or_contractual"
]

def validate_initiatives(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if (df["effort_person_weeks"] <= 0).any():
        raise ValueError("effort_person_weeks must be > 0")

    if (~df["confidence_0to1"].between(0, 1)).any():
        raise ValueError("confidence_0to1 must be between 0 and 1")

    if (~df["impact_1to5"].between(1, 5)).any():
        raise ValueError("impact_1to5 must be between 1 and 5")

    if (~df["risk_1to5"].between(1, 5)).any():
        raise ValueError("risk_1to5 must be between 1 and 5")

def risk_multiplier(risk_1to5: pd.Series) -> pd.Series:
    # risk 1 -> 1.00, risk 5 -> 0.68 (tunable)
    return 1.0 - (risk_1to5 - 1.0) * 0.08

def dependency_penalty(dep_count: pd.Series) -> pd.Series:
    return 1.0 - np.minimum(dep_count, 10) * 0.02

def compute_rice(df: pd.DataFrame) -> pd.Series:
    return (df["reach_users"] * df["impact_1to5"] * df["confidence_0to1"]) / df["effort_person_weeks"]

def compute_wsjf(df: pd.DataFrame) -> pd.Series:
    # cost_of_delay_per_week is optional; if absent, return NaN
    if "cost_of_delay_per_week" not in df.columns:
        return pd.Series([np.nan] * len(df), index=df.index)
    return df["cost_of_delay_per_week"] / df["effort_person_weeks"]

def normalize(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    if s.isna().all():
        return s
    mn, mx = np.nanmin(s), np.nanmax(s)
    if np.isclose(mx, mn):
        return pd.Series([0.5] * len(s), index=s.index)
    return (s - mn) / (mx - mn)

def score_portfolio(
    df: pd.DataFrame,
    w_rice: float = 0.55,
    w_wsjf: float = 0.25,
    w_strategic_fit: float = 0.20,
) -> pd.DataFrame:
    validate_initiatives(df)

    rice = compute_rice(df)
    wsjf = compute_wsjf(df)
    fit = df["strategic_fit_1to5"]

    base = (
        w_rice * normalize(rice) +
        w_wsjf * normalize(wsjf) +
        w_strategic_fit * normalize(fit)
    )

    adj = risk_multiplier(df["risk_1to5"]) * dependency_penalty(df["dependency_count"])
    final = base * adj

    out = df.copy()
    out["score_rice"] = rice
    out["score_wsjf"] = wsjf
    out["score_base_0to1"] = base
    out["mult_risk"] = risk_multiplier(df["risk_1to5"])
    out["mult_dependencies"] = dependency_penalty(df["dependency_count"])
    out["score_final"] = final

    # Separate mandatory work
    out["bucket"] = np.where(out["compliance_or_contractual"] == 1, "MANDATORY", "DISCRETIONARY")

    # Rank within bucket then overall
    out = out.sort_values(["bucket", "score_final"], ascending=[True, False])
    out["rank_within_bucket"] = out.groupby("bucket").cumcount() + 1
    out["rank_overall"] = out["score_final"].rank(ascending=False, method="min").astype(int)
    return out

