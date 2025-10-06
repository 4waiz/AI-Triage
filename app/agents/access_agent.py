from app.schemas import TriageJSON, AccessDecision

# Simple IF/THEN rules for demo. Expand as needed.

def decide_route(triage: TriageJSON) -> AccessDecision:
    red = set([s.lower() for s in triage.red_flags])
    has_red_flag = len(red) > 0

    if triage.urgency_level.lower() == "emergent" or triage.disposition == "ED" or has_red_flag:
        return AccessDecision(recommendation="ED", instructions_en="Proceed to the nearest Emergency Department now.")

    # Default outpatient for urgent/non-urgent in demo
    return AccessDecision(recommendation="Outpatient", instructions_en="We will help you schedule the next available clinic appointment.")
