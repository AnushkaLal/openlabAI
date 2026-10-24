import json
from openlab.core.llm import ask_agent


def run_reviewer(
    question: str,
    audit: dict,
    analysis: dict,
    interpretation: str,
) -> str:
    return ask_agent(
        "You are an independent scientific Peer Reviewer. Check whether "
        "the interpretation answers the question and is supported by the "
        "provided numerical evidence. Flag unsupported claims, missing-data "
        "bias, correlation-versus-causation errors, and limitations. "
        "Do not invent results. End with a verdict: ACCEPT or NEEDS REVISION. "
        "Your verdict is advisory, not a guarantee of scientific validity.",
        json.dumps({
            "question": question,
            "audit": audit,
            "computed_results": analysis,
            "analyst_interpretation": interpretation,
        }, indent=2),
    )
