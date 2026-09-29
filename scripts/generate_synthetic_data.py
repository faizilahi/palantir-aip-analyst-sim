"""Build analyst corpus from ontology-style KPI files (synthetic)."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=None, help="Optional foundry-lab derived dir")
    args = parser.parse_args()
    out = Path("data/corpus")
    out.mkdir(parents=True, exist_ok=True)

    sibling = Path(__file__).resolve().parents[2] / "palantir-foundry-ontology-sim" / "data" / "derived"
    src = args.source or sibling
    files = ["patient_cost_summary.csv", "department_spend.csv", "high_risk_top_spenders.csv"]
    if src.exists() and all((src / f).exists() for f in files):
        for f in files:
            shutil.copy(src / f, out / f)
        print(f"Copied corpus from {src}")
    else:
        pd.DataFrame(
            {"department": ["ED", "IP", "OP"], "total_cost": [120000, 98000, 45000]}
        ).to_csv(out / "department_spend.csv", index=False)
        pd.DataFrame(
            {
                "patient_id": ["P00001", "P00002"],
                "risk_tier": ["HIGH", "HIGH"],
                "total_cost_usd": [12000, 9500],
            }
        ).to_csv(out / "high_risk_top_spenders.csv", index=False)
        pd.DataFrame(
            {
                "patient_id": ["P00001", "P00002", "P00003"],
                "encounter_count": [4, 2, 7],
                "total_cost_usd": [15000, 8000, 22000],
            }
        ).to_csv(out / "patient_cost_summary.csv", index=False)
        print("Wrote minimal fallback corpus")


if __name__ == "__main__":
    main()
