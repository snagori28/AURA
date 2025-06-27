from backend.planner_agent import plan
from backend.memory_agent import MemoryAgent
from backend.clarifier_agent import clarify
from backend.reasoner_agent import reason
from backend.explainer_agent import explain
from backend.feedback_agent import apply_feedback


class FakeLLM:
    def __init__(self, responses):
        self.responses = list(responses)

    def ask(self, prompt, mode="default"):
        return self.responses.pop(0)


class FakeTx:
    def __init__(self, store):
        self.store = store

    def run(self, query, **params):
        self.store.append((query, params))
        return [{"fact": "A", "topic": "B"}]


class FakeSession:
    def __init__(self, store):
        self.store = store

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def write_transaction(self, func):
        tx = FakeTx(self.store)
        func(tx)

    def read_transaction(self, func):
        tx = FakeTx(self.store)
        return func(tx)


class FakeDriver:
    def __init__(self):
        self.store = []

    def session(self):
        return FakeSession(self.store)


def test_planner_agent_returns_subtasks():
    llm = FakeLLM(["1. A\n2. B\n3. C"])
    subtasks = plan("goal", llm)
    assert subtasks == ["A", "B", "C"]


def test_memory_agent_store_and_retrieve():
    driver = FakeDriver()
    agent = MemoryAgent(driver=driver)
    agent.store_fact("f", "t", "s", 1.0)
    facts = agent.retrieve_facts("f")
    assert driver.store
    assert facts == [{"fact": "A", "topic": "B"}]


def test_clarifier_agent():
    llm = FakeLLM(["Question 1?\nQuestion 2?"])
    questions = clarify(["sub"], ["fact"], llm)
    assert questions == ["Question 1?", "Question 2?"]


def test_reasoner_agent():
    llm = FakeLLM(["Decision"])
    assert reason(["s"], [{"fact": "A"}], llm) == "Decision"


def test_explainer_agent():
    llm = FakeLLM(["Explanation"])
    assert explain("Reason", llm) == "Explanation"


def test_feedback_agent():
    facts = [{"fact": "A", "value": "B"}]
    feedback = {0: "reject"}
    assert apply_feedback(facts, feedback) == []
