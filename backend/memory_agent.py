from __future__ import annotations

from typing import Any, Dict, List, Optional


class MemoryAgent:
    """Neo4j-based fact store."""

    def __init__(
        self,
        uri: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        driver: Any | None = None,
    ) -> None:
        if driver is not None:
            self.driver = driver
        else:  # pragma: no cover - external dependency
            from neo4j import GraphDatabase  # type: ignore

            self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def store_fact(
        self,
        fact: str,
        value: str,
        source: str = "unknown",
        confidence: float = 1.0,
    ) -> None:
        query = (
            "MERGE (f:Fact {text:$fact})\n"
            "MERGE (t:Topic {name:$value})\n"
            "MERGE (f)-[:ABOUT {source:$source, confidence:$confidence}]->(t)"
        )
        with self.driver.session() as session:  # type: ignore
            session.write_transaction(
                lambda tx: tx.run(
                    query,
                    fact=fact,
                    value=value,
                    source=source,
                    confidence=confidence,
                )
            )

    def retrieve_facts(self, subtask: str) -> List[Dict[str, Any]]:
        query = (
            "MATCH (f:Fact)-[:ABOUT]->(t:Topic)\n"
            "WHERE f.text CONTAINS $subtask\n"
            "RETURN f.text AS fact, t.name AS topic"
        )
        with self.driver.session() as session:  # type: ignore
            records = session.read_transaction(
                lambda tx: list(tx.run(query, subtask=subtask))
            )
        return [
            {"fact": r["fact"], "topic": r["topic"]} for r in records  # type: ignore
        ]
