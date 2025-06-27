from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

from .llm_agent import LLMAgent
from .planner_agent import plan
from .memory_agent import MemoryAgent
from .clarifier_agent import clarify
from .reasoner_agent import reason
from .explainer_agent import explain
from .feedback_agent import apply_feedback
from .logging import log_event

app = FastAPI()

llm = LLMAgent()
memory = MemoryAgent()


class Goal(BaseModel):
    goal: str


class AskRequest(BaseModel):
    question: str


class Facts(BaseModel):
    facts: List[Dict[str, Any]]


@app.post("/plan")
def plan_endpoint(goal: Goal) -> Dict[str, Any]:
    subtasks = plan(goal.goal, llm)
    log_event("plan_generated", str(subtasks))
    return {"subtasks": subtasks}


@app.post("/ask")
def ask_endpoint(req: AskRequest) -> Dict[str, Any]:
    answer = llm.ask(req.question)
    log_event("asked", req.question)
    return {"answer": answer}


@app.post("/explain")
def explain_endpoint(data: Dict[str, Any]) -> Dict[str, Any]:
    reasoning = data.get("reasoning", "")
    explanation = explain(reasoning, llm)
    log_event("explain", reasoning)
    return {"explanation": explanation}


@app.post("/learn")
def learn_endpoint(data: Facts) -> Dict[str, Any]:
    for f in data.facts:
        memory.store_fact(
            f["fact"],
            f["value"],
            f.get("source", "api"),
            f.get("confidence", 1.0),
        )
    log_event("facts_learned", str(len(data.facts)))
    return {"stored": len(data.facts)}


@app.post("/ingest")
def ingest_endpoint(data: Dict[str, Any]) -> Dict[str, Any]:
    subtask = data.get("subtask", "")
    facts = memory.retrieve_facts(subtask)
    log_event("facts_retrieved", subtask)
    return {"facts": facts}


@app.post("/feedback")
def feedback_endpoint(data: Dict[str, Any]) -> Dict[str, Any]:
    facts = data.get("facts", [])
    feedback = data.get("feedback", {})
    processed = apply_feedback(facts, feedback)
    for f in processed:
        memory.store_fact(
            f["fact"],
            f["value"],
            f.get("source", "feedback"),
            f.get("confidence", 1.0),
        )
    log_event("feedback_processed", str(len(processed)))
    return {"accepted": len(processed)}
