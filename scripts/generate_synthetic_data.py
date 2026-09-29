from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
# Prefer reading foundry sim data if present; else minimal
foundry = ROOT.parent / "palantir-foundry-ontology-sim" / "data" / "encounter.csv"
if foundry.exists():
    enc = pd.read_csv(foundry)
    dept = pd.read_csv(foundry.parent / "department.csv")
else:
    enc = pd.DataFrame({
        "encounter_id": [f"E{i:04d}" for i in range(100)],
        "length_of_stay_hours": [30] * 100,
        "status": ["OPEN"] * 100,
        "department_id": ["D2"] * 100,
    })
    dept = pd.DataFrame({"department_id": ["D2"], "department_name": ["MedSurg"]})
enc.to_csv(DATA / "encounter.csv", index=False)
dept.to_csv(DATA / "department.csv", index=False)
Path(DATA / "freshness_ok.txt").write_text("as_of=2024-09-01T10:00:00Z\nnow=2024-09-01T11:00:00Z\n", encoding="utf-8")
Path(DATA / "freshness_stale.txt").write_text("as_of=2024-09-01T10:00:00Z\nnow=2024-09-01T16:30:00Z\n", encoding="utf-8")
print("analyst fixtures ready")
