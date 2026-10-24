import json
from openlab.core.llm import ask_agent


def run_analyst(question: str, analysis: dict) -> str:
    return ask_agent(
        "You are the Analysis Engineer. Interpret only the supplied "
        "computed results. Explain relevant patterns and effect sizes. "
        "Distinguish correlation from causation. If the question cannot "
        "be answered by the supplied results, say what additional analysis "
        "is needed. Never invent statistics.",
        json.dumps({
            "research_question": question,
            "computed_results": analysis,
        }, indent=2),
    )
