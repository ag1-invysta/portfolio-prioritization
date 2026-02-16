import pandas as pd
from portfolio_prioritizer.scoring import score_portfolio, validate_initiatives

def test_validate_initiatives_rejects_bad_confidence():
    df = pd.DataFrame([{
        "id": "X", "title": "Bad", "effort_person_weeks": 1,
        "reach_users": 10, "impact_1to5": 3, "confidence_0to1": 1.5,
        "risk_1to5": 2, "strategic_fit_1to5": 3,
        "dependency_count": 0, "compliance_or_contractual": 0
    }])
    try:
        validate_initiatives(df)
        assert False, "Expected ValueError"
    except ValueError as e:
        assert "confidence_0to1" in str(e)

def test_score_portfolio_outputs_expected_columns():
    df = pd.DataFrame([{
        "id": "A", "title": "A", "effort_person_weeks": 10,
        "reach_users": 1000, "impact_1to5": 4, "confidence_0to1": 0.7,
        "risk_1to5": 3, "strategic_fit_1to5": 5,
        "dependency_count": 2, "compliance_or_contractual": 0,
        "cost_of_delay_per_week": 20000
    }])
    out = score_portfolio(df)
    for col in [
        "score_rice", "score_wsjf", "score_base_0to1",
        "mult_risk", "mult_dependencies", "score_final",
        "bucket", "rank_within_bucket", "rank_overall"
    ]:
        assert col in out.columns

