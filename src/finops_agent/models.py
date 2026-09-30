from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class WorkloadObservation:
    namespace: str
    name: str
    kind: str = "Deployment"
    cpu_requested_cores: float = 0.0
    memory_requested_gib: float = 0.0
    cpu_avg_cores: float = 0.0
    memory_avg_gib: float = 0.0
    observation_hours: int = 72
    monthly_cost: float | None = None


@dataclass(frozen=True)
class Finding:
    namespace: str
    name: str
    kind: str
    action: str
    confidence: str
    reason: str
    estimated_monthly_opportunity: float = 0.0
    proposed_change: dict[str, Any] | None = None
    evidence: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AnalysisResult:
    currency: str
    modeled_monthly_infrastructure_cost: float
    modeled_monthly_optimization_opportunity: float
    realized_monthly_savings: float | None
    findings: tuple[Finding, ...]
    policy: str = "recommendation-only"

    def to_dict(self) -> dict[str, Any]:
        return {
            "currency": self.currency,
            "modeled_monthly_infrastructure_cost": round(self.modeled_monthly_infrastructure_cost, 2),
            "modeled_monthly_optimization_opportunity": round(self.modeled_monthly_optimization_opportunity, 2),
            "realized_monthly_savings": self.realized_monthly_savings,
            "policy": self.policy,
            "findings": [f.to_dict() for f in self.findings],
        }
