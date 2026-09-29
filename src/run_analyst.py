import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from retrieval import certified_fields, retrieve_medsurg_los
from freshness import parse_freshness, enforce_sla
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    allowed = certified_fields(ROOT / "catalog" / "certified_fields.json")
    enc = pd.read_csv(DATA / "encounter.csv")
    dept = pd.read_csv(DATA / "department.csv")
    fresh = enforce_sla(parse_freshness(DATA / "freshness_ok.txt")["age_hours"], 4)
    stale = enforce_sla(parse_freshness(DATA / "freshness_stale.txt")["age_hours"], 4)
    ans = retrieve_medsurg_los(enc, dept, allowed) if fresh["ok"] else {"refused": True, "reason": fresh["message"]}
    refuse = {"refused": True, "reason": stale["message"]}
    summary = {"question": "How many open encounter LOS hours are in MedSurg right now?",
               "retrieval": ans, "stale_refusal": refuse, "no_api_keys": True}
    pd.DataFrame([{"answer_hours": ans.get("answer_hours"), "stale_refusal": refuse["reason"]}]).to_csv(
        OUT / "analyst_result.csv", index=False
    )
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
