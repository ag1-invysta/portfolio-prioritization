from __future__ import annotations
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

FEATURES = [
    "effort_person_weeks", "reach_users", "impact_1to5", "confidence_0to1",
    "risk_1to5", "strategic_fit_1to5", "dependency_count"
]

def train_success_model(history_df: pd.DataFrame) -> Pipeline:
    missing = [c for c in FEATURES + ["success_0to1"] if c not in history_df.columns]
    if missing:
        raise ValueError(f"History missing columns: {missing}")

    X = history_df[FEATURES].copy()
    y = history_df["success_0to1"].astype(int)

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced"))
    ])
    model.fit(X, y)
    return model

def predict_success(model: Pipeline, initiatives_df: pd.DataFrame) -> pd.Series:
    X = initiatives_df[FEATURES].copy()
    proba = model.predict_proba(X)[:, 1]
    return pd.Series(proba, index=initiatives_df.index, name="p_success")

