"""Aggregate review/*.json into a single review-report.md for human triage."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REV = DATA / "parts" / "review"

q = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
choice_by_id = {it["id"]: it for it in q["choice"]}
code_by_id = {it["id"]: it for it in q["code"]}

all_flags = []
for f in sorted(REV.glob("*.json")):
    try:
        items = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ERROR {f.name}: {e}")
        continue
    for it in items:
        it["_source"] = f.stem
        all_flags.append(it)

severity_rank = {"high": 0, "medium": 1, "low": 2}
issue_rank = {
    "wrong_answer": 0, "fixed_still_buggy": 0, "wrong_diagnosis": 0,
    "broken_html": 1,
    "needs_human_review": 2,
    "weak_explanation": 3, "wrong_topic": 4,
}
all_flags.sort(key=lambda x: (
    severity_rank.get(x.get("severity"), 9),
    issue_rank.get(x.get("issue"), 9),
    x.get("id", ""),
))

LETTER = ["A", "B", "C", "D"]

lines = ["# 题库交叉复核报告\n"]
lines.append(f"共 {len(all_flags)} 个异议条目 / 414 题(选择题 373 + 编程题 41)\n")
sev_counter = Counter(x.get("severity") for x in all_flags)
issue_counter = Counter(x.get("issue") for x in all_flags)
src_counter = Counter(x.get("_source") for x in all_flags)
lines.append(f"严重度: high {sev_counter.get('high',0)} · medium {sev_counter.get('medium',0)} · low {sev_counter.get('low',0)}")
lines.append(f"类型: " + " · ".join(f"{k} {v}" for k,v in issue_counter.most_common()))
lines.append(f"来源: " + " · ".join(f"{k} {v}" for k,v in sorted(src_counter.items())))
lines.append("")

for group_sev in ("high", "medium", "low"):
    group = [x for x in all_flags if x.get("severity") == group_sev]
    if not group:
        continue
    lines.append(f"\n## 严重度: {group_sev}  ({len(group)} 条)\n")
    for it in group:
        qid = it.get("id", "?")
        issue = it.get("issue", "?")
        note = it.get("note", "")
        if qid in choice_by_id:
            src = choice_by_id[qid]
            stem = src["stem"].replace("\n", " ")[:90]
            opts = src["options"]
            oa = it.get("original_answer")
            ma = it.get("my_answer")
            oa_str = f"{LETTER[oa]}={opts[oa][:30]}" if isinstance(oa, int) and 0 <= oa < 4 else "?"
            ma_str = f"{LETTER[ma]}={opts[ma][:30]}" if isinstance(ma, int) and 0 <= ma < 4 else "?"
            lines.append(f"### [{issue}] {qid}")
            lines.append(f"**题面**: {stem}")
            for i, o in enumerate(opts):
                lines.append(f"- ({LETTER[i]}) {o[:80]}")
            lines.append(f"**原答案**: {oa_str}")
            if isinstance(ma, int):
                lines.append(f"**复核答案**: {ma_str}")
            lines.append(f"**理由**: {note}")
            lines.append("")
        elif qid in code_by_id:
            src = code_by_id[qid]
            lines.append(f"### [{issue}] {qid} {src.get('title','')}")
            lines.append(f"**得分**: {src.get('score','?')}  |  **章**: {src.get('ch','?')}")
            lines.append(f"**理由**: {note}")
            lines.append("")
        else:
            lines.append(f"### [{issue}] {qid} (题目未找到)")
            lines.append(f"**理由**: {note}")
            lines.append("")

out_path = ROOT / "review-report.md"
out_path.write_text("\n".join(lines), encoding="utf-8")
print(f"-> {out_path}")
print(f"total flags: {len(all_flags)}")
print(f"by severity: {dict(sev_counter)}")
print(f"by issue: {dict(issue_counter)}")
