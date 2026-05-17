"""Merge agent outputs (data/parts/out/*.json) back into data/questions.json.

Usage:
    python scripts/merge_answers.py
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_DIR = DATA / "parts" / "out"

questions_path = DATA / "questions.json"
q = json.loads(questions_path.read_text(encoding="utf-8"))

choice_map = {}
code_map = {}
problems = []

for f in sorted(OUT_DIR.glob("choice-*.json")):
    try:
        items = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        problems.append(f"{f.name}: {e}")
        continue
    for it in items:
        if "id" in it:
            choice_map[it["id"]] = it
    print(f"  loaded {f.name}: {len(items)} items")

code_file = OUT_DIR / "code-all.json"
if code_file.exists():
    try:
        items = json.loads(code_file.read_text(encoding="utf-8"))
        for it in items:
            if "id" in it:
                code_map[it["id"]] = it
        print(f"  loaded {code_file.name}: {len(items)} items")
    except Exception as e:
        problems.append(f"{code_file.name}: {e}")

# merge choice
filled_c, missing_c, conf_counter = 0, [], Counter()
for item in q["choice"]:
    src = choice_map.get(item["id"])
    if not src:
        missing_c.append(item["id"])
        continue
    a = src.get("answer")
    if isinstance(a, int) and 0 <= a <= 3:
        item["answer"] = a
    item["confidence"] = src.get("confidence", "low")
    item["topic"] = src.get("topic", "")
    item["explanation"] = src.get("explanation", "")
    filled_c += 1
    conf_counter[item["confidence"]] += 1

# merge code
filled_p, missing_p = 0, []
for item in q["code"]:
    src = code_map.get(item["id"])
    if not src:
        missing_p.append(item["id"])
        continue
    item["bug"] = src.get("bug", "")
    item["fixed"] = src.get("fixed", "")
    topic = src.get("topic", [])
    if isinstance(topic, str):
        topic = [topic]
    item["topic"] = topic
    filled_p += 1

questions_path.write_text(
    json.dumps(q, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print()
print(f"选择题: filled {filled_c}/{len(q['choice'])}")
print(f"  confidence -> {dict(conf_counter)}")
if missing_c:
    print(f"  MISSING ({len(missing_c)}): {missing_c[:10]}{'...' if len(missing_c)>10 else ''}")
print(f"编程题: filled {filled_p}/{len(q['code'])}")
if missing_p:
    print(f"  MISSING: {missing_p}")
if problems:
    print("\nWARNINGS:")
    for p in problems:
        print(f"  - {p}")
print(f"\n-> {questions_path}")
