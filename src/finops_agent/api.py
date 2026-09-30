from __future__ import annotations

from typing import Any
from fastapi import FastAPI, HTTPException
from .io import analyze_payload

app = FastAPI(title="FinOps Agent", version="1.0.0")

@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/v1/analyze")
def analyze(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        return analyze_payload(payload)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
