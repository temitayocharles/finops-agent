from __future__ import annotations

from typing import Any


def validate_payload(payload: dict[str, Any]) -> None:
    rightsizing = float(payload.get("rightsizing_threshold", 0.35))
    investigate = float(payload.get("investigate_threshold", 0.60))
    if not 0 <= rightsizing <= investigate <= 1:
        raise ValueError("Thresholds must satisfy 0 <= rightsizing <= investigate <= 1")
    currency = str(payload.get("currency", "USD")).strip().upper()
    if len(currency) != 3 or not currency.isalpha():
        raise ValueError("currency must be a three-letter code")
    workloads = payload.get("workloads", [])
    if not isinstance(workloads, list):
        raise TypeError("workloads must be a JSON array")
    for index, item in enumerate(workloads):
        if not isinstance(item, dict):
            raise TypeError(f"workloads[{index}] must be an object")
        for field in ("namespace", "name"):
            if not str(item.get(field, "")).strip():
                raise ValueError(f"workloads[{index}].{field} is required")
        for field in ("cpu_requested_cores", "memory_requested_gib", "cpu_avg_cores", "memory_avg_gib"):
            if float(item.get(field, 0.0)) < 0:
                raise ValueError(f"workloads[{index}].{field} cannot be negative")
