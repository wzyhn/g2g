"""Apply review fixes that don't require rewriting explanations.

机械修复 + needs_human_review 降级 + stem 字符修补。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
QPATH = DATA / "questions.json"

q = json.loads(QPATH.read_text(encoding="utf-8"))
choice_by_id = {it["id"]: it for it in q["choice"]}
code_by_id = {it["id"]: it for it in q["code"]}

log = []

# === high · wrong_answer:改答案 + 改 explanation 措辞 ===

# ch08-802eeb4b: Sum(a=8,c=2) -> 13 (B=1) 而非 15 (C=2)
it = choice_by_id["ch08-802eeb4b"]
it["answer"] = 1
it["confidence"] = "high"
it["explanation"] = (
    "<p>调用 <code>Sum(a=8, c=2)</code>:<code>a=8</code>,<code>c=2</code>,"
    "<code>b</code> 未传用默认值 <code>3</code>。<code>sum([8,3,2])</code> = <b>13</b>,选 B。</p>"
    "<p><b>易错点</b>:关键字参数只覆盖指定项,未传的形参仍用 def 时的默认值,不要漏算。</p>"
)
log.append("ch08-802eeb4b: answer C(2)→B(1)")

# ch08-97a21f8e: 输出 11 的是 eval("1"+"1")=C(2),而非 eval("1+1")=D(3)
it = choice_by_id["ch08-97a21f8e"]
it["answer"] = 2
it["confidence"] = "high"
it["explanation"] = (
    "<p><code>eval('1'+'1')</code> 先把两个字符串拼成 <code>'11'</code>,再 <code>eval</code> 求值得 <b>11</b>,选 C。</p>"
    "<p>对照:A 直接打印字符串 <code>'1+1'</code>;B <code>1+1</code> 算术得 <code>2</code>;"
    "D <code>eval('1+1')</code> 求值也得 <code>2</code>。</p>"
    "<p><b>易错点</b>:<code>eval</code> 对字符串当 Python 表达式求值,所以拼接顺序决定结果。</p>"
)
log.append("ch08-97a21f8e: answer D(3)→C(2)")

# === high · fixed_still_buggy:把 fixed 代码里的半角符号换回全角 ===

# 0410 题面要全角「!」
it = code_by_id["0410"]
old = it["fixed"]
it["fixed"] = old.replace("!", "！")
log.append(f"0410: fixed 半角 !→！  ({old.count('!')} 处)")

# 0503 题面要全角「,」(只在 print 字符串字面量内)
it = code_by_id["0503"]
old = it["fixed"]
# 只替换 print 字面量里的逗号,保守:把出现在 print(' ... ') 引号内的 ASCII , 换成 ,
# 实际原 fixed 里的逗号都在 print 字符串内,直接全替换更稳
import re
def fix_str_commas(code: str) -> str:
    def repl(m):
        return m.group(0).replace(",", ",")
    return re.sub(r"'[^']*'|\"[^\"]*\"", repl, code)
it["fixed"] = fix_str_commas(old)
log.append("0503: fixed 字符串内半角 ,→,")

# 0516 题面要全角「:」(input 提示符)
it = code_by_id["0516"]
old = it["fixed"]
def fix_str_colons(code: str) -> str:
    def repl(m):
        return m.group(0).replace(":", "：")
    return re.sub(r"'[^']*'|\"[^\"]*\"", repl, code)
it["fixed"] = fix_str_colons(old)
log.append("0516: fixed 字符串内半角 :→:")

# === high · needs_human_review:ch01-46994d59 DBMS 教材分歧 ===
it = choice_by_id["ch01-46994d59"]
it["confidence"] = "low"
warn = "<p><b>⚠ 教材分歧</b>:DBMS 归类各教材不一,嵩天教材多归「系统软件」(A),部分计算机基础教材归「支撑软件」(B)。请按你们指定教材为准。</p>"
it["explanation"] = warn + (it.get("explanation") or "")
log.append("ch01-46994d59: confidence→low + ⚠ 警示前缀")

# === broken_html:ch05-00993f22 删孤立 </content> ===
it = choice_by_id["ch05-00993f22"]
it["explanation"] = it["explanation"].replace("</content>", "").rstrip()
log.append("ch05-00993f22: 删 </content>")

# === stem 字符修补:神威 / 长破折号 ===
for qid, old_sub, new_sub in [
    ("ch01-9379a3b0", "神威?太湖之光", "神威·太湖之光"),
    ("ch01-fce608d1", "神威?太湖之光", "神威·太湖之光"),
]:
    it = choice_by_id[qid]
    new_stem = it["stem"].replace(old_sub, new_sub) if old_sub in it["stem"] else it["stem"]
    new_opts = [o.replace(old_sub, new_sub) for o in it["options"]]
    it["stem"] = new_stem
    it["options"] = new_opts
    log.append(f"{qid}: 神威? → 神威·")

# ch04-9889cac6: P=–P 长破折号 → P=-P 减号
it = choice_by_id["ch04-9889cac6"]
old_stem = it["stem"]
it["stem"] = old_stem.replace("P=–P", "P=-P")
log.append("ch04-9889cac6: P=–P → P=-P")

# === 所有 needs_human_review:confidence→low + 警示前缀 ===
NHR = [
    "ch04-3383c459", "ch04-40dcf53c", "ch04-7affd290", "ch04-d46328f9",
    "ch05-cb77e79e", "ch07-a001bfe3", "ch07-bc20869a",
    "ch01-9379a3b0", "ch01-fce608d1",
    "ch04-39004ab6", "ch04-61822854", "ch04-9889cac6",
    "ch05-92117f7f",
]
WARN_PREFIX = "<p><b>⚠ 题面有缺失或歧义</b>:此题缩进、特殊字符可能被平台抓取丢失,答案为最常见解读,务必去课本/豆包二次验证。</p>"
for qid in NHR:
    it = choice_by_id[qid]
    if WARN_PREFIX not in it["explanation"]:
        it["explanation"] = WARN_PREFIX + it["explanation"]
    it["confidence"] = "low"
    log.append(f"{qid}: confidence→low + ⚠ 前缀")

# === 编程题 0428 weak_explanation:坦白说扣分点未知 ===
it = code_by_id["0428"]
it["bug"] = (
    "<p>原代码逻辑等价于 <code>i%5==0 and i%2==1</code>,功能上正确。<b>扣 25 分原因不明</b>,"
    "可能是平台测试用例对输入格式(如换行/空格)有特殊要求,或边界 n 处理差异。"
    "fixed 用 <code>i%10==5</code> 等价改写,如仍扣分,建议直接对照测试用例输出。</p>"
)
log.append("0428: bug 文案改诚实表述")

# === 写回 ===
QPATH.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"applied {len(log)} patches:")
for l in log:
    print(f"  · {l}")
print(f"-> {QPATH}")
