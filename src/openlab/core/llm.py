import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OPENLAB_MODEL", "gemma4:31b-cloud")


def ask_agent(role: str, context: str) -> str:
    """Ask the local Gemma model to perform one agent's task."""
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are one specialist in OpenLab AI, a scientific "
                        "data investigation team. Be precise, distinguish "
                        "evidence from assumptions, and never invent statistics. "
                        + role
                    ),
                },
                {"role": "user", "content": context},
            ],
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()
    return response.json()["message"]["content"]
