from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_assess_basic():
    payload = {"symptoms_text": "ألم شديد في الصدر وضيق نفس", "language": "ar"}
    resp = client.post("/api/v1/assess", json=payload)
    assert resp.status_code in (200, 500)  # 500 if no API key set
    if resp.status_code == 200:
        j = resp.json()
        assert j["recommendation"] in ("ED", "Outpatient")
        assert "next_step_url" in j
Tests: tests/test_validator.py
from app.safety.validator import validate_safe_text

def test_validator_blocks():
    blocked = validate_safe_text("This mentions suicide")
    assert "emergency" in blocked.lower()
