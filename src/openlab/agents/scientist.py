import json
from openlab.core.llm import ask_agent


def run_scientist(audit: dict, question: str) -> str:
    return ask_agent(
        "You are the Research Scientist. Propose a concise analysis plan "
        "that answers the research question using available columns. "
        "Mention relevant limitations and avoid causal claims from "
        "observational data. Do not invent columns or results.",
        json.dumps({
            "research_question": question,
            "dataset_audit": audit,
        }, indent=2),
    )
