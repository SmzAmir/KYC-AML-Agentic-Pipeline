import sys
sys.path.insert(0, "src")
from kyc_agent_factory.orchestrator import Orchestrator

def test_end_to_end_pipeline():
    orch = Orchestrator()
    cid = orch.create_case("Alice Example", [{"type":"passport","number":"X123"}])
    out = orch.run_case(cid)
    assert out["case_id"] == cid
    assert out["risk"]["band"] in ("LOW", "MEDIUM", "HIGH")
    c = orch.get_case(cid)
    assert c["status"] == "processed"
    audit = orch.get_audit(cid)
    assert len(audit["events"]) >= 4
