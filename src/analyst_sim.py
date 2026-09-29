"""
Palantir AIP Analyst teaching simulation — keyword retrieval + rule templates.
NO OpenAI / Anthropic / Foundry AIP keys required. NOT production AIP.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from retriever import KeywordCorpusRetriever

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus"


def answer(query: str, retriever: KeywordCorpusRetriever) -> str:
    hits = retriever.search(query)
    q = query.lower()
    if "department" in q or "spend" in q or "cost" in q:
        for h in hits:
            if "department" in h["name"]:
                df = h["df"]
                top = df.sort_values("total_cost", ascending=False).iloc[0]
                return (
                    f"Template analyst response: highest department spend is {top['department']} "
                    f"at ${top['total_cost']:,.2f} (synthetic corpus `{h['name']}`)."
                )
    if "high risk" in q or "risk" in q:
        for h in hits:
            if "high_risk" in h["name"]:
                df = h["df"]
                row = df.iloc[0]
                return (
                    f"Template analyst response: top high-risk patient {row.get('patient_id')} "
                    f"has spend ${row.get('total_cost_usd', row.get('total_cost', 0)):,.2f}."
                )
    snippet = hits[0]["text"][:400].replace("\n", " ")
    return f"Template analyst response (retrieved `{hits[0]['name']}`): {snippet}..."


def main() -> None:
    retriever = KeywordCorpusRetriever(CORPUS)
    questions = [
        "Which department has the highest spend?",
        "Show high risk patient costs",
    ]
    for q in questions:
        print(f"Q: {q}")
        print(f"A: {answer(q, retriever)}\n")


if __name__ == "__main__":
    main()
