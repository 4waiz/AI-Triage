from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import AssessRequest, AssessResponse
from app.agents.clinician_agent import run_clinician_agent
from app.agents.access_agent import decide_route
from app.safety.validator import validate_safe_text
from app.config import settings

app = FastAPI(title="RightCare AI Triage API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static web chat
app.mount("/static", StaticFiles(directory="app/web"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("app/web/index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/api/v1/assess", response_model=AssessResponse)
async def assess(req: AssessRequest):
    try:
        triage = await run_clinician_agent(req.symptoms_text, req.language)
        decision = decide_route(triage)

        # Localize final user text (Arabic-first)
        if req.language.lower().startswith("ar"):
            if decision.recommendation == "ED":
                user_text = "توجّه فورًا إلى قسم الطوارئ."
            else:
                user_text = "احجز موعدًا مع العيادات الخارجية." \
                            + ("\n" + (triage.instructions_ar or ""))
        else:
            user_text = "Go to the Emergency Department." if decision.recommendation == "ED" \
                        else "Book an outpatient appointment." \
                             + ("\n" + (decision.instructions_en or ""))

        safe_text = validate_safe_text(user_text)

        return AssessResponse(
            recommendation=decision.recommendation,
            severity=triage.urgency_level,
            red_flags=triage.red_flags,
            specialty=triage.required_specialty,
            reasoning=triage.reasoning,
            instructions=safe_text,
            next_step_url=settings.SCHEDULING_URL if decision.recommendation == "Outpatient" else f"{settings.APP_BASE_URL}/static/ed-directions.html",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
