"""Keyword retriever — NO API keys, NO live LLM."""
from __future__ import annotations

from pathlib import Path

import pandas as pd


class KeywordCorpusRetriever:
    def __init__(self, corpus_dir: Path) -> None:
        self.docs: list[dict] = []
        for csv in corpus_dir.glob("*.csv"):
            df = pd.read_csv(csv)
            self.docs.append({"name": csv.stem, "text": df.to_csv(index=False), "df": df})

    def search(self, query: str, top_k: int = 2) -> list[dict]:
        q = query.lower()
        scored = []
        for doc in self.docs:
            text = doc["text"].lower()
            score = sum(text.count(tok) for tok in q.split() if len(tok) > 2)
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        if not self.docs:
            return []
        return [d for s, d in scored[:top_k] if s > 0] or [self.docs[0]]
