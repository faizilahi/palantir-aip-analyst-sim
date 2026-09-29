from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "images"
OUT.mkdir(parents=True, exist_ok=True)
p = ROOT / "data" / "corpus" / "department_spend.csv"
if p.exists():
    df = pd.read_csv(p)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(df["total_cost"], labels=df["department"], autopct="%1.0f%%")
    ax.set_title("AIP sim context: spend mix")
    fig.savefig(OUT / "spend_pie.png", dpi=120)
    plt.close(fig)
