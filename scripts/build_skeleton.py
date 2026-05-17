"""Build data/questions.json skeleton from existing choice.json + programming.json.

Output: data/questions.json with empty answer/explanation fields, ready for
AI batch-fill.

ID 设计:cbk_id 在 ASP.NET 抓取里同章会冲突,改用 stem 规范化后的 sha1[:8]。
"""
import hashlib
import json
import re
from pathlib import Path


def stem_id(ch: str, stem: str) -> str:
    norm = re.sub(r"\s+", " ", stem).strip()
    h = hashlib.sha1(norm.encode("utf-8")).hexdigest()[:8]
    return f"ch{ch}-{h}"

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT.parent
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

CHAPTER_NAMES = {
    "01": "Python 概述与计算思维",
    "02": "Python 基本语法元素",
    "03": "基本数据类型",
    "04": "程序的控制结构",
    "05": "函数与代码复用",
    "06": "组合数据类型",
    "07": "文件与数据格式化",
    "08": "程序设计方法学",
    "09": "Python 计算生态",
    "10": "Python 标准库",
}
SKIPPED_CHOICE = {"04"}
SKIPPED_CODE = {"05"}

choice_src = json.loads((SRC / "choice.json").read_text(encoding="utf-8"))
prog_src = json.loads((SRC / "programming.json").read_text(encoding="utf-8"))

choice_chapters = []
all_choice = []
for ch in sorted(choice_src):
    seen = set()
    chapter_items = []
    for q in choice_src[ch]:
        qid = stem_id(ch, q["stem"])
        if qid in seen:
            continue
        seen.add(qid)
        chapter_items.append({
            "id": qid,
            "ch": f"ch{ch}",
            "stem": q["stem"],
            "options": [o["text"] for o in sorted(q["options"], key=lambda x: int(x["value"]))],
            "answer": None,
            "confidence": "low",
            "topic": "",
            "explanation": "",
        })
    chapter_items.sort(key=lambda x: x["id"])
    choice_chapters.append({
        "id": f"ch{ch}",
        "name": CHAPTER_NAMES.get(ch, f"第 {ch} 章"),
        "count": len(chapter_items),
        "skipped": ch in SKIPPED_CHOICE,
    })
    all_choice.extend(chapter_items)

prog_by_ch = {}
for p in prog_src:
    prog_by_ch.setdefault(p["chapter"], []).append(p)

code_chapters = []
all_code = []
for ch in sorted(prog_by_ch):
    items = sorted(prog_by_ch[ch], key=lambda x: x.get("pro_num", ""))
    code_chapters.append({
        "id": f"ch{ch}",
        "name": CHAPTER_NAMES.get(ch, f"第 {ch} 章"),
        "count": len(items),
        "skipped": ch in SKIPPED_CODE,
    })
    for p in items:
        try:
            score = int(p.get("score") or 0)
        except (TypeError, ValueError):
            score = 0
        all_code.append({
            "id": p["pro_num"],
            "ch": f"ch{ch}",
            "title": p.get("pro_name", ""),
            "score": score,
            "problem": p.get("problem", ""),
            "submitted": p.get("my_code", ""),
            "bug": "",
            "fixed": "",
            "topic": [],
        })

out = {
    "meta": {
        "choiceChapters": choice_chapters,
        "codeChapters": code_chapters,
    },
    "choice": all_choice,
    "code": all_code,
}

(DATA / "questions.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print(f"choice chapters: {len(choice_chapters)} | choice questions: {len(all_choice)}")
for c in choice_chapters:
    flag = " [SKIPPED]" if c["skipped"] else ""
    print(f"  {c['id']}  {c['count']:>3}  {c['name']}{flag}")
print(f"code chapters: {len(code_chapters)} | code questions: {len(all_code)}")
for c in code_chapters:
    flag = " [SKIPPED]" if c["skipped"] else ""
    print(f"  {c['id']}  {c['count']:>3}  {c['name']}{flag}")
print(f"-> {DATA / 'questions.json'}")
