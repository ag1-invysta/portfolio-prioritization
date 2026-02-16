import pandas as pd
from portfolio_prioritizer.sensitivity import default_scenarios, run_scenarios, rank_stability

def test_sensitivity_outputs_ranks_and_stability():
    df = pd.DataFrame([
        {"id":"A","title":"A","effort_person_weeks":10,"reach_users":1000,"impact_1to5":4,
         "confidence_0to1":0.7,"risk_1to5":2,"strategic_fit_1to5":5,"dependency_count":2,
         "compliance_or_contractual":0,"cost_of_delay_per_week":50000},
        {"id":"B","title":"B","effort_person_weeks":6,"reach_users":500,"impact_1to5":3,
         "confidence_0to1":0.9,"risk_1to5":3,"strategic_fit_1to5":3,"dependency_count":1,
         "compliance_or_contractual":0,"cost_of_delay_per_week":20000},
        {"id":"C","title":"C","effort_person_weeks":8,"reach_users":2000,"impact_1to5":4.5,
         "confidence_0to1":0.6,"risk_1to5":4,"strategic_fit_1to5":4,"dependency_count":5,
         "compliance_or_contractual":1,"cost_of_delay_per_week":60000},
    ])
    ranks = run_scenarios(df, default_scenarios())
    assert {"scenario", "id", "rank"}.issubset(ranks.columns)
    stab = rank_stability(ranks, top_n=2)
    assert "stability_top_n" in stab.columns
    assert stab["stability_top_n"].between(0, 1).all()

