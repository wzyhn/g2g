# G2G · 挂2过

> 从挂到过 · Python 期末冲刺刷题站
>
> 零后端、单文件、移动端优先 · 414 题带 AI 讲解、错题本、模拟测试、收藏

📦 **仓库**:<https://github.com/wzyhn/g2g>
🔗 **在线访问**:<https://wzyhn.github.io/g2g/>(GitHub Pages,需到 repo Settings → Pages 启用)

## 为什么叫 G2G

「挂」→ **2** → 「过」 —— 从挂科到过线,中间隔着一个数字 2。
拼音 *guà 2 guò*,首尾 G 开头,所以简称 **G2G**(也是 *Good to Go* 的双关)。

一个班的同学考前一周的共同记忆。

## 截图

> 截图占位,部署后请把首页 / 做题 / 错题本 / 模拟测试 4 张图放进 `docs/`。
> 命名:`docs/home.png`、`docs/quiz.png`、`docs/mistakes.png`、`docs/mock.png`

| 首页 | 做题 | 错题本 | 模拟测试 |
|---|---|---|---|
| ![home](docs/home.png) | ![quiz](docs/quiz.png) | ![mistakes](docs/mistakes.png) | ![mock](docs/mock.png) |

## 功能

**核心**
- 📚 **按章刷题** · 选择题 10 章 + 编程题 6 章,点章节弹底部选题面板
- 🎛 **选题面板** · 题数 / 顺序(顺序、随机、错题优先、未做优先)/ 跳过已掌握
- ❌ **错题本** · 错过自动入,顽疾标记(错 ≥3 次),按章筛选,一键「✓ 掌握」瘦身
- ⭐ **收藏** · 答题页右上一键 ★,首页快捷入口

**冲刺**
- ⏱ **模拟测试** · 抽 30 题 60 分钟倒计时,完成后看错误率与章节分布,一键加进错题本
- 🔍 **搜索** · 关键词全文搜 stem / options / 题面
- 🤖 **AI 讲解 4 模板** · 通用 / 举反例 / 对比类似题 / 5 句话说清,一键复制粘贴去豆包/Kimi

**杂项**
- 🌙 **夜间模式** · 跟随系统主题
- 💾 **导入导出** · 错题本与收藏 JSON 备份,换设备能续
- 📱 **移动端优先** · 微信内置浏览器、Chrome、Safari、360 全部测过
- 🔒 **零追踪 / 零后端 / 不收数据** · localStorage 存进度
- 🚫 **noindex** · 题库私有,搜索引擎不收录

## 技术栈

- 纯原生 HTML / CSS / JS,**零构建**、**零依赖**、**零框架**
- 单 HTML(`index.html`) ~70 KB · 题库 JSON ~300 KB · logo 资源 ~88 KB
- LocalStorage 持久化,fetch 加载 questions.json
- 浏览器要求:Chrome 86+ / Safari 14+ / 微信 X5 内核(已加 fallback)

## 部署

只需 3 步:

```bash
# 1. 打包必要文件(共 ~340 KB)
tar czf g2g.tar.gz index.html data/questions.json assets/

# 2. 解压到静态服务器目录,或直接拖到 Cloudflare Pages / Vercel / Netlify

# 3. 配 nginx gzip(可选,JSON 大小从 300KB 降到 50KB)
#   gzip on; gzip_types application/json;
```

完整说明见 [`实施说明.md`](实施说明.md)。

## 自定义

修改 HTML 顶部 `CONFIG`:

```js
const CONFIG = {
  title:    "G2G 挂2过",
  subtitle: "从挂到过",
  examAt:         "2026-05-19T09:00:00+08:00",
  projectStartAt: "2026-05-18T02:00:00+08:00",
  aiModel:        "Claude 4.7 Opus",
  aiVendor:       "Anthropic",
  github:         "https://github.com/wzyhn/g2g",
};
```

## 题库来源

- 414 道题(选择题 373 + 编程题 41)从学校 e2e 教学平台抓取
- 答案与讲解由 Claude 4.7 Opus 批量生成,经多轮交叉复核与人工 patch
- 整体置信度:high 360+ · medium 6 · low 7
- low 标记的题在题面或选项有平台抓取损失,展示时带 ⚠ 警示

## 仓库结构

```
g2g/
├── index.html              SPA 单文件
├── data/
│   └── questions.json      题库
├── assets/                 favicon + logo
├── scripts/                构建/审核脚本(不需要上线)
├── docs/                   截图(可选)
├── README.md               本文件
└── 实施说明.md              部署详细说明
```

## 致谢

- 题库素材来自学校 e2e 教学平台,版权归原作者所有,仅供同班学习
- 界面与功能设计由 [Claude 4.7 Opus](https://claude.com) 生成

## 免责声明

本站为本班同学间的内部学习工具,仅作个人学习交流,不得外传,不得用于任何商业目的。
答案与讲解均由 AI 生成,可能存在错误。使用者应自行判断准确性。
本站不对因使用本工具产生的任何后果承担责任。

## 建立 GitHub 仓库

```bash
# 在 g2g/ 目录下
git init
git add index.html README.md 实施说明.md data/questions.json assets/ .gitignore
git commit -m "init: G2G v1.0"
git branch -M main

# GitHub New repo → 名字填 g2g → Public → 不勾 Add README → Create
git remote add origin https://github.com/wzyhn/g2g.git
git push -u origin main

# 把 README/CONFIG 里的 wzyhn 全局替换成你的 GH 用户名后,再 commit 一次
```

## License

MIT

