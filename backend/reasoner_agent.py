from typing import Any, Dict, List

from .llm_agent import LLMAgent


def reason(
    subtasks: List[str],
    facts: List[Dict[str, Any]],
    llm: LLMAgent,
    mode: str = "planning",
) -> str:
    prompt = (
        f"Use mode {mode} to reason over the following subtasks and facts and "
        "return your decision or plan.\n"\
        f"Subtasks: {subtasks}\nFacts: {facts}"
    )
    return llm.ask(prompt, mode="reasoner")
