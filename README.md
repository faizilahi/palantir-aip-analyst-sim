# AIP-Style Analyst Over Certified Fields Only

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

Local simulation of an AIP-style analyst answering a hospital ops question using
**only certified ontology fields**. No API keys. No Foundry tenant.

## The question

"How many open encounter LOS hours are in MedSurg right now?"

## The retrieval

Retriever restricts to certified fields listed in `catalog/certified_fields.json`.
Answer from SQL grain: **2,104** hours.

## The refusal when data is stale

If `encounter` freshness exceeds 4 hours, the analyst **refuses** instead of
guessing. Stale fixture triggers: `REFUSE: certified encounter data is stale`.

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_analyst.py
```
