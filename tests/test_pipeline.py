import json
from pathlib import Path
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
cfg = json.loads(Path("config.json").read_text())

def test_metrics_schema():
    m = client.get("/metrics").json()
    for k in ["student_id", "accuracy", "training_rows", "model_version", "git_sha"]:
        assert k in m
    assert m["student_id"] == cfg["student_id"]
    assert m["accuracy"] > 0.5
    assert m["training_rows"] >= 100

def test_predict():
    rec = {f: 0.0 for f in cfg["features"]}
    r = client.post("/predict", json={"records": [rec]})
    assert r.status_code == 200
    assert len(r.json()["predictions"]) == 1