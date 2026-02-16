from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Initiative:
    id: str
    title: str
    effort_person_weeks: float
    reach_users: float
    impact_1to5: float
    confidence_0to1: float
    risk_1to5: float
    strategic_fit_1to5: float
    dependency_count: int
    compliance_or_contractual: int
    cost_of_delay_per_week: float | None = None


@dataclass(frozen=True)
class HistoricalOutcome:
    id: str
    title: str
    effort_person_weeks: float
    reach_users: float
    impact_1to5: float
    confidence_0to1: float
    risk_1to5: float
    strategic_fit_1to5: float
    dependency_count: int
    success_0to1: int

