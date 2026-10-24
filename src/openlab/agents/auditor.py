import json
from openlab.core.llm import ask_agent


def run_auditor(audit: dict, question: str) -> str:
    return ask_agent(
        "You are the Data Auditor. Explain data-quality risks. "
        "Do not claim that unusual values are errors without evidence. "
        "Do not change the dataset.",
        json.dumps({
            "research_question": question,
            "measured_audit": audit,
        }, indent=2),
    )
