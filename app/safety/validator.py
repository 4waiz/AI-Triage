import re

BANNED_PATTERNS = [
    r"suicide|self-harm|kill yourself|انتحار|قتل نفسك",
    r"exact dosing instructions|mg/kg|overdose|جرعة" ,
    r"violent threat|تهديد",
]

SAFE_FALLBACK_AR = (
    "عذرًا، لا أستطيع عرض هذا النص. إذا كانت لديك حالة طارئة، اتصل بخدمات الطوارئ أو توجّه إلى أقرب قسم طوارئ فورًا."
)
SAFE_FALLBACK_EN = (
    "Sorry, I can’t show that content. If this is an emergency, call local emergency services or go to the nearest ED now."
)

def validate_safe_text(text: str) -> str:
    lower = text.lower()
    for pattern in BANNED_PATTERNS:
        if re.search(pattern, lower):
            # crude language detection
            return SAFE_FALLBACK_AR if any(c in text for c in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي") else SAFE_FALLBACK_EN
    return text
