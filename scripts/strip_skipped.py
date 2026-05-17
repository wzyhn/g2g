"""清除题库里"老师未讲"相关表述 + meta.skipped 全设 false。"""
import json
import re
from pathlib import Path

QPATH = Path(__file__).resolve().parent.parent / "data" / "questions.json"
q = json.loads(QPATH.read_text(encoding="utf-8"))

# 1. meta:所有 skipped=false
n_meta = 0
for c in q["meta"]["choiceChapters"]:
    if c.get("skipped"):
        c["skipped"] = False
        n_meta += 1
for c in q["meta"]["codeChapters"]:
    if c.get("skipped"):
        c["skipped"] = False
        n_meta += 1

# 2. 删除 explanation 里的"本章老师未讲"段
n_exp = 0
NOTE_PAT = re.compile(r"\s*<p>\s*<b>注意</b>\s*[:：]\s*本章老师未讲[^<]*</p>\s*", re.IGNORECASE)
WARN_PAT = re.compile(r"<p><b>⚠ 题面有缺失或歧义</b>[^<]*</p>")
# 我们保留 "题面有缺失" 警示(确实是平台抓取问题),只去"老师未讲"
for it in q["choice"]:
    old = it.get("explanation", "")
    new = NOTE_PAT.sub("", old).strip()
    if new != old:
        it["explanation"] = new
        n_exp += 1

# 3. 删除 ch01-46994d59 教材分歧前缀里如有"老师未讲"也清(它当前是教材分歧,不应该有)
# 但保留教材分歧本身

# 4. ch04 confidence 之前因"未讲"被人工 medium 的题,如果 explanation 没有任何警示了,
#    并且原来是 medium,提升回 high(因为现在不再标"未讲")
n_conf = 0
for it in q["choice"]:
    if it.get("confidence") == "medium" and not WARN_PAT.search(it.get("explanation", "")) \
       and "缺失" not in it.get("explanation", "") and "歧义" not in it.get("explanation", ""):
        it["confidence"] = "high"
        n_conf += 1

QPATH.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"meta.skipped cleared: {n_meta}")
print(f"explanation 老师未讲段移除: {n_exp}")
print(f"confidence medium→high: {n_conf}")
print(f"-> {QPATH}")
