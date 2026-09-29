from datetime import datetime
from pathlib import Path

def parse_freshness(path: Path) -> dict:
    vals = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        k, v = line.split("=", 1)
        vals[k] = datetime.fromisoformat(v.replace("Z", ""))
    age = (vals["now"] - vals["as_of"]).total_seconds() / 3600
    return {"age_hours": age, "as_of": vals["as_of"].isoformat(), "now": vals["now"].isoformat()}

def enforce_sla(age_hours: float, sla: float) -> dict:
    if age_hours > sla:
        return {"ok": False, "message": "REFUSE: certified encounter data is stale"}
    return {"ok": True, "message": "fresh"}
