from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .analysis import analyze_workloads
from .models import WorkloadObservation
from .validation import validate_payload


def analyze_payload(payload: dict[str, Any]) -> dict[str, Any]:
    validate_payload(payload)
    workloads = tuple(WorkloadObservation(**item) for item in payload.get("workloads", []))
    result = analyze_workloads(workloads, currency=str(payload.get("currency", "USD")).upper(), modeled_monthly_infrastructure_cost=float(payload.get("modeled_monthly_infrastructure_cost", 0.0)), rightsizing_threshold=float(payload.get("rightsizing_threshold", 0.35)), investigate_threshold=float(payload.get("investigate_threshold", 0.60)))
    return result.to_dict()


def analyze_file(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Input must be a JSON object")
    return analyze_payload(payload)
