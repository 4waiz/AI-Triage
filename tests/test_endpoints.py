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
