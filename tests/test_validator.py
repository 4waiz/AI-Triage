from app.safety.validator import validate_safe_text

def test_validator_blocks():
    blocked = validate_safe_text("This mentions suicide")
    assert "emergency" in blocked.lower()
