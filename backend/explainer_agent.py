from .llm_agent import LLMAgent


def explain(reasoning: str, llm: LLMAgent) -> str:
    prompt = (
        "Turn the following reasoning steps into a readable explanation:\n" + reasoning
    )
    return llm.ask(prompt, mode="explainer")
