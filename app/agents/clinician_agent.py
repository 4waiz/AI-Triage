from typing import Any
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from app.schemas import TriageJSON
from app.utils.langchain_setup import get_llm

SYSTEM_PROMPT = """
You are ClinicianAgent, an Arabic-friendly triage assistant.
Follow the Grounded ReAct style: think step-by-step, cite red flags, and output ONLY the JSON per the schema.
Keep medical claims conservative and defer to ED when life-threatening risk exists.
If input is Arabic, reason in Arabic internally but keep fields in Arabic where appropriate.
"""

# You can paste the Research Team's master prompt into prompts/grounded_react_prompt.txt and load it here if needed.

async def run_clinician_agent(symptoms_text: str, language: str) -> TriageJSON:
    parser = PydanticOutputParser(pydantic_object=TriageJSON)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT + "\\nSchema: {format_instructions}"),
        ("human", "Language: {language}\nSymptoms: {symptoms}")
    ]).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | get_llm() | parser
    result: TriageJSON = await chain.ainvoke({
        "language": language,
        "symptoms": symptoms_text
    })
    return result
