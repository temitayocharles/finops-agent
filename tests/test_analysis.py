from finops_agent.analysis import analyze_workloads
from finops_agent.models import WorkloadObservation
from finops_agent.io import analyze_payload


def test_rightsize_when_utilization_is_low():
    result = analyze_workloads([WorkloadObservation(namespace="payments", name="api", cpu_requested_cores=2.0, memory_requested_gib=4.0, cpu_avg_cores=0.3, memory_avg_gib=0.8, observation_hours=72, monthly_cost=200.0)], currency="USD", modeled_monthly_infrastructure_cost=1000.0)
    assert result.findings[0].action == "RIGHTSIZE"
    assert result.findings[0].confidence == "HIGH"
    assert result.modeled_monthly_optimization_opportunity > 0
    assert result.realized_monthly_savings is None


def test_keep_when_utilization_is_aligned():
    result = analyze_workloads([WorkloadObservation(namespace="platform", name="worker", cpu_requested_cores=1.0, memory_requested_gib=2.0, cpu_avg_cores=0.75, memory_avg_gib=1.4, observation_hours=72, monthly_cost=100.0)])
    assert result.findings[0].action == "KEEP"
    assert result.modeled_monthly_optimization_opportunity == 0


def test_missing_requests_is_investigate():
    result = analyze_workloads([WorkloadObservation(namespace="default", name="job")])
    assert result.findings[0].action == "INVESTIGATE"


def test_payload_validation_rejects_negative_usage():
    try:
        analyze_payload({"workloads": [{"namespace": "default", "name": "bad", "cpu_avg_cores": -1}]})
    except ValueError as exc:
        assert "cannot be negative" in str(exc)
    else:
        raise AssertionError("negative utilization should be rejected")
