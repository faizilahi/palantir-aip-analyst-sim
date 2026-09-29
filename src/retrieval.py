import json
from pathlib import Path
import pandas as pd

def certified_fields(catalog: Path) -> set:
    data = json.loads(catalog.read_text(encoding="utf-8"))
    return {(c["object"], c["field"]) for c in data["certified"] if c["certified"]}

def retrieve_medsurg_los(enc: pd.DataFrame, dept: pd.DataFrame, allowed: set) -> dict:
    need = {("Encounter", "length_of_stay_hours"), ("Encounter", "status"), ("Department", "department_name")}
    if not need.issubset(allowed):
        return {"refused": True, "reason": "uncertified fields requested"}
    m = enc.merge(dept, on="department_id")
    m = m[(m["status"] == "OPEN") & (m["department_name"] == "MedSurg")]
    return {"refused": False, "answer_hours": int(m["length_of_stay_hours"].sum()), "row_count": int(len(m))}
