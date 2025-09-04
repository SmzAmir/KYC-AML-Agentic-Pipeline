import json, sys
sys.path.insert(0, "src")
from kyc_agent_factory.orchestrator import Orchestrator

if __name__ == "__main__":
    orch = Orchestrator()
    cid = orch.create_case("Alice Example", [{"type":"passport","number":"X123"}])
    print(json.dumps(orch.run_case(cid), indent=2))
