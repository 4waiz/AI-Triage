from langchain_openai import ChatOpenAI
from app.config import settings

# Single place to change model/params

def get_llm():
    """
    Initializes and returns the language model client (e.g., ChatOpenAI).
    
    Reads configuration like model ID and API key from the settings.
    """
    return ChatOpenAI(
        model=settings.MODEL_ID,
        temperature=0.2,
        api_key=settings.OPENAI_API_KEY,
    )