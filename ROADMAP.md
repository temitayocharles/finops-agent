# FinOps Agent Roadmap

## Where it stands today

FinOps Agent analyzes Kubernetes workload evidence and produces explainable,
approval-gated cost recommendations. It runs as a CLI (`finops-agent analyze`),
an HTTP API (`/healthz`, `/v1/analyze`), and scheduled in-cluster via the
n8n workflow that has run weekly since August 2026. What it does not have yet
is the breadth of detectors, the historical memory, and the test coverage a
tool like this needs before I'd call it done.

## Planned work

### 1. Test coverage (6-8h)
Only `test_analysis.py` exists today. Add focused tests for the API layer
(`api.py`), the CLI (`cli.py`), input loading and output writing (`io.py`),
the data models (`models.py`), and input validation (`validation.py`).
Goal: every public function covered, CI running the suite on each push.

### 2. More detectors (6h)
Current analysis covers the core over-provisioning patterns. Add:
- Idle namespaces (no running workloads, still holding quota)
- Orphaned PersistentVolumeClaims and unattached load balancers
- HPA right-sizing suggestions from observed utilization bands
- Node bin-packing waste (pods spread thin across too many nodes)

Each detector ships with its evidence query, confidence scoring, and a
worked example in `examples/`.

### 3. Trend persistence and diff reports (5h)
Today each analysis is a point in time. Store results in SQLite, add a
`finops-agent trends` command and a `/v1/trends` endpoint, and generate
week-over-week diff reports so modeled opportunity can be compared against
verified savings after changes land.

### 4. Cost model extensions (4h)
- Spot / preemptible pricing support in the cost model
- Multi-currency reporting
- Bare-metal amortization profiles beyond the current defaults

### 5. Webhook delivery hardening (4h)
Retries with backoff, payload signing, and ready-made templates for Slack
and PagerDuty. Delivery ledger so failed notifications are visible, not lost.

### 6. CI policy checks (3h)
Expand the CI-style policy gate: configurable thresholds (e.g. "fail the
pipeline if projected monthly waste exceeds $X"), machine-readable output
for pipeline parsing.

### 7. Operator docs (3h)
A real operator runbook: install, RBAC review checklist, telemetry wiring,
interpreting confidence levels, and a troubleshooting section. Plus two more
worked examples from real cluster shapes.

---

Total: comfortably over 20 hours of work I plan to do anyway. Items ship in
the order above; test coverage first because everything else builds on it.
