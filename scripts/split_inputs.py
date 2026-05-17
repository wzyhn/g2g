"""Split data/questions.json into per-chapter input slices for agents.

Output:
  data/parts/in/choice-{ch}.json  e.g. choice-ch01.json
  data/parts/in/code-all.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "parts" / "in"
OUT.mkdir(parents=True, exist_ok=True)

q = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))

by_ch = {}
for item in q["choice"]:
    by_ch.setdefault(item["ch"], []).append({
        "id": item["id"],
        "stem": item["stem"],
        "options": item["options"],
    })

for ch, items in by_ch.items():
    (OUT / f"choice-{ch}.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  choice-{ch}.json  {len(items)}")

code_items = [
    {
        "id": it["id"],
        "ch": it["ch"],
        "title": it["title"],
        "score": it["score"],
        "problem": it["problem"],
        "submitted": it["submitted"],
    }
    for it in q["code"]
]
(OUT / "code-all.json").write_text(
    json.dumps(code_items, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"  code-all.json  {len(code_items)}")
