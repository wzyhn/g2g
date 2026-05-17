"""Prepare a single input file for the rewrite agent: 8 weak-explanation items."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
q = json.loads((DATA / "questions.json").read_text(encoding="utf-8"))
choice = {it["id"]: it for it in q["choice"]}

WEAK_NOTES = {
    "ch01-0b0a026c": "解析里「冯诺依曼才是计算机之父」是事实错误。冯诺依曼通常称「现代计算机之父」或「计算机体系结构之父」,「计算机之父」一般指巴贝奇。改:图灵=计算机科学之父,巴贝奇=计算机之父。",
    "ch01-3a0be675": "易错点「显示器层级太低」表述含混。改为:显示器属于输出设备的具体型号,不能与运算器/控制器/存储器等大类并列。",
    "ch01-c5ab4be1": "易错点里说「严格说软硬件相互依存」与题目正解略矛盾,易让学生迷糊。直接强调「软件运行必须依赖硬件,硬件设计也参考软件需求,但本题侧重前者」。",
    "ch02-4dc53643": "解析里把「存储空间」归入算力相关不严谨,存储与算力是不同维度,改写时明确划分:算力=硬件运算资源,数据=原始素材,算法=学习/决策方法。",
    "ch04-7855f2fc": "讲解写「可能是 2.9999...」语气模糊。CPython 下 sqrt(3)*sqrt(3) 确定不严格等于 3,直接说「浮点运算精度问题,结果不严格等于 3」更准确。",
    "ch04-dd87f2f2": "讲解承认 A 描述本身没错却选 B,逻辑链「最正确」交代不清晰。改写:A 的 eval 用法没错但只是举例,B 描述了 Python 动态类型的本质特征,是「关于函数描述」最完整准确的。C 错(可多个 return),D 错(return 非必须)。",
    "ch05-658178b5": "早期融合缺点选 A 合理,但 D 项「计算量较高」也部分成立。补充说明:早期融合的本质问题是「特征拼接后噪声扩散到所有模态」,故 A 是最核心缺点;D 计算量问题不显著,因为早期融合反而维度低于后期独立处理。",
    "ch07-35997d71": "题目 C 选项说「从键盘获取一个整数」不严谨,input 实际返回字符串。补充说明:input 返回 str,需配合 int() 才能转换,但相比其它三个错误项(集合/元组/列表都不对),C 仍是最佳答案。",
}

out = []
for qid, note in WEAK_NOTES.items():
    it = choice[qid]
    out.append({
        "id": qid,
        "ch": it["ch"],
        "stem": it["stem"],
        "options": it["options"],
        "answer": it["answer"],
        "old_explanation": it["explanation"],
        "review_note": note,
    })

target = DATA / "parts" / "rewrite_in.json"
target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"-> {target}  ({len(out)} items)")
