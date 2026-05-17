"""修复 questions.json 数据完整性:转义 ASCII <letter>,统一换行。

修复:
1. stem / option / explanation 里所有出现的 <letter… 形式的 ASCII 字面量
   (会被浏览器当 HTML 标签吞掉),改成 &lt;…&gt;
2. \n 不需要改(white-space:pre-wrap 在 CSS 端处理)
"""
import json
import re
from pathlib import Path

QPATH = Path(__file__).resolve().parent.parent / "data" / "questions.json"
q = json.loads(QPATH.read_text(encoding="utf-8"))

# 匹配:<letter 但不在 < 后跟 / 或已是合法 HTML 标签(p/code/b/br/span/div 等)
# 简化:< 后跟字母,且不属于我们白名单的标签开头 → 转义
ALLOWED_TAGS = ("p", "code", "b", "br", "span", "div", "a", "i", "u", "em", "strong",
                "ul", "ol", "li", "pre", "small", "sub", "sup", "h1", "h2", "h3", "blockquote")
def escape_bad_lt(text: str) -> str:
    """把不属于白名单 HTML 起止标签的 < 替换成 &lt;。"""
    if not text or "<" not in text:
        return text
    def repl(m):
        rest = m.group(1)
        # </tag... 形式
        if rest.startswith("/"):
            tag = re.match(r"/([a-zA-Z]+)", rest)
            if tag and tag.group(1).lower() in ALLOWED_TAGS:
                return m.group(0)
            return "&lt;" + rest
        # <tag... 形式
        tag = re.match(r"([a-zA-Z]+)", rest)
        if tag and tag.group(1).lower() in ALLOWED_TAGS:
            return m.group(0)
        return "&lt;" + rest
    return re.sub(r"<(.*?)(?=[<\s\"']|$)", repl, text, count=0)

# 更稳的实现:逐字符扫描
def escape_unknown_tags(text: str) -> str:
    if not text or "<" not in text:
        return text
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c != "<":
            out.append(c)
            i += 1
            continue
        # try parse: < + optional / + alpha+ + (>|space|/)
        m = re.match(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)([\s/>])", text[i:])
        if m and m.group(2).lower() in ALLOWED_TAGS:
            out.append("<")
            i += 1
            continue
        # not a known tag start — escape
        out.append("&lt;")
        i += 1
    return "".join(out)

choice_fixed = 0
for it in q["choice"]:
    for field in ("stem", "explanation"):
        new = escape_unknown_tags(it.get(field, ""))
        if new != it.get(field, ""):
            it[field] = new
            choice_fixed += 1
    new_opts = []
    opt_changed = False
    for o in it.get("options", []):
        new = escape_unknown_tags(o)
        if new != o:
            opt_changed = True
        new_opts.append(new)
    if opt_changed:
        it["options"] = new_opts
        choice_fixed += 1

code_fixed = 0
for it in q["code"]:
    for field in ("problem", "bug"):
        new = escape_unknown_tags(it.get(field, ""))
        if new != it.get(field, ""):
            it[field] = new
            code_fixed += 1
    # fixed/submitted 是代码字段,不渲染为 HTML,不动

QPATH.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"choice fields fixed: {choice_fixed}")
print(f"code fields fixed: {code_fixed}")
print(f"-> {QPATH}")
