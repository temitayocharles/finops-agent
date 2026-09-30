from __future__ import annotations

from collections.abc import Iterable

from .models import AnalysisResult, Finding, WorkloadObservation


def _ratio(used: float, requested: float) -> float | None:
    if requested <= 0:
        return None
    return max(0.0, used) / requested


def _confidence(hours: int, cpu_ratio: float | None, memory_ratio: float | None) -> str:
    if hours >= 72 and cpu_ratio is not None and memory_ratio is not None:
        return "HIGH"
    if hours >= 24:
        return "MEDIUM"
    return "LOW"


def analyze_workloads(workloads: Iterable[WorkloadObservation], *, currency: str = "USD", modeled_monthly_infrastructure_cost: float = 0.0, rightsizing_threshold: float = 0.35, investigate_threshold: float = 0.60) -> AnalysisResult:
    findings: list[Finding] = []
    opportunity_total = 0.0
    for w in workloads:
        cpu_ratio = _ratio(w.cpu_avg_cores, w.cpu_requested_cores)
        mem_ratio = _ratio(w.memory_avg_gib, w.memory_requested_gib)
        ratios = [r for r in (cpu_ratio, mem_ratio) if r is not None]
        confidence = _confidence(w.observation_hours, cpu_ratio, mem_ratio)
        if not ratios:
            findings.append(Finding(namespace=w.namespace, name=w.name, kind=w.kind, action="INVESTIGATE", confidence="LOW", reason="No request-to-utilization ratio can be calculated from the supplied evidence.", evidence={"observation_hours": w.observation_hours}))
            continue
        peak_ratio = max(ratios)
        estimated_opportunity = 0.0
        if w.monthly_cost is not None and w.monthly_cost > 0:
            estimated_opportunity = max(0.0, w.monthly_cost * (1.0 - min(1.0, peak_ratio)))
        if peak_ratio <= rightsizing_threshold:
            action = "RIGHTSIZE"
            reason = "Observed utilization is materially below requested capacity across the supplied window."
            opportunity_total += estimated_opportunity
            proposed = {"cpu_request_multiplier": round(max(0.5, min(1.0, (cpu_ratio or peak_ratio) * 1.5)), 2), "memory_request_multiplier": round(max(0.5, min(1.0, (mem_ratio or peak_ratio) * 1.5)), 2)}
        elif peak_ratio <= investigate_threshold:
            action = "INVESTIGATE"
            reason = "Utilization is below requested capacity, but the evidence does not justify an automatic rightsizing recommendation."
            proposed = None
        else:
            action = "KEEP"
            reason = "Observed utilization is reasonably aligned with requested capacity."
            proposed = None
        findings.append(Finding(namespace=w.namespace, name=w.name, kind=w.kind, action=action, confidence=confidence, reason=reason, estimated_monthly_opportunity=round(estimated_opportunity, 2), proposed_change=proposed, evidence={"observation_hours": w.observation_hours, "cpu_requested_cores": w.cpu_requested_cores, "cpu_avg_cores": w.cpu_avg_cores, "memory_requested_gib": w.memory_requested_gib, "memory_avg_gib": w.memory_avg_gib}))
    return AnalysisResult(currency=currency, modeled_monthly_infrastructure_cost=max(0.0, modeled_monthly_infrastructure_cost), modeled_monthly_optimization_opportunity=max(0.0, opportunity_total), realized_monthly_savings=None, findings=tuple(findings))
