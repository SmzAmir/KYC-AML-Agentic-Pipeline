from src.pipeline import healthcheck, example_task

def test_health():
    assert healthcheck()["status"] == "ok"

def test_example_task():
    out = example_task({"a": 1, "b": 2.5, "c": "ignore"})
    assert out["numeric_total"] == 3.5
    assert set(out["input_keys"]) == {"a", "b", "c"}
