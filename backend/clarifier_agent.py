from typing import List

from .llm_agent import LLMAgent


def clarify(subtasks: List[str], known_facts: List[str], llm: LLMAgent) -> List[str]:
    prompt = (
        "Given the subtasks and known facts, what clarifying questions should be asked?"\
        f"\nSubtasks: {subtasks}\nFacts: {known_facts}"
    )
    response = llm.ask(prompt, mode="clarifier")
    questions = []
    for line in response.splitlines():
        q = line.strip(" -")
        if not q:
            continue
        if not q.endswith("?"):
            q += "?"
        questions.append(q)
    return questions
