from typing import List

from .llm_agent import LLMAgent


def plan(goal: str, llm: LLMAgent) -> List[str]:
    """Use an LLM to break a goal into minimal subtasks."""
    prompt = (
        "Break down the following goal into 3-7 minimal subtasks as a numbered list."\
        f"\nGoal: {goal}\nSubtasks:"
    )
    response = llm.ask(prompt, mode="planner")
    tasks: List[str] = []
    for line in response.splitlines():
        line = line.strip(" -")
        if not line:
            continue
        if line[0].isdigit() and "." in line:
            line = line.split(".", 1)[1].strip()
        tasks.append(line)
    return tasks[:7]
