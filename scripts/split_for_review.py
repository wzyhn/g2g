"""Prepare review inputs:
  data/parts/review_in/choice-chXX.json  脱敏题面 (id + stem + options)
  data/parts/review_in/answers.json      原答案(供 review agent 在独立解题后对比)
  data/parts/review_in/code-all.json     编程题完整数据(含 score / submitted)

输出区分两个目录:
  review_in/  脱敏题面 (给 review agent 独立解题)
  review_in/answers.json   原答案与解析 (review agent 解完题后才查阅)

为了避免锚定,要求 agent 必须先独立答完再读 answers.json。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "parts" / "review_in"
OUT.mkdir(parents=True, exist_ok=True)

q = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))

by_ch = {}
for it in q["choice"]:
    by_ch.setdefault(it["ch"], []).append({
        "id": it["id"],
        "stem": it["stem"],
        "options": it["options"],
    })

for ch, items in sorted(by_ch.items()):
    (OUT / f"choice-{ch}.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"  review_in/choice-{ch}.json  {len(items)}")

answers = {
    "choice": {
        it["id"]: {
            "answer": it["answer"],
            "confidence": it["confidence"],
            "topic": it["topic"],
            "explanation": it["explanation"],
        }
        for it in q["choice"]
    },
    "code": {
        it["id"]: {
            "bug": it["bug"],
            "fixed": it["fixed"],
            "topic": it["topic"],
        }
        for it in q["code"]
    },
}
(OUT / "answers.json").write_text(
    json.dumps(answers, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"  review_in/answers.json  ({len(answers['choice'])} choice + {len(answers['code'])} code)")

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
print(f"  review_in/code-all.json  {len(code_items)}")
