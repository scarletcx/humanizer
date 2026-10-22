# Humanizer

[![tests](https://github.com/scarletcx/humanizer/actions/workflows/tests.yml/badge.svg)](https://github.com/scarletcx/humanizer/actions/workflows/tests.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

把 AI 味很重的文字改写得像真人写的，同时不改变它表达的事实。

> 本仓库是 [blader/humanizer](https://github.com/blader/humanizer) 的 fork/打包版，原作为 Siqi Chen 所有。35 条模式和技能行为保持不变；本 fork 主要更新跨 agent 安装路径和仓库结构。

[English](README.md)

## 它做什么

Humanizer 基于 Wikipedia 的 ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)（由 WikiProject AI Cleanup 维护）整理了 35 条 AI 写作模式，包括：

- 内容层：夸大重要性、堆名字、空洞的 `-ing` 分析、销售腔、模糊来源、模板化的“挑战与展望”；
- 语言层：AI 高频词、回避 *is/are*、“不是 X 而是 Y”、强行三件套、同义词轮换、虚假的“从 X 到 Y”、被动语态和缺失主语；
- 风格层：破折号、过多加粗、加粗列表标签、标题 Title Case、emoji、弯引号、过多连字符、假装深刻、预告下一段、重复标题、写旧版本、强行金句、假坦诚开头、回答没人提的反对、拒绝假选项；
- Chatbot 层：客服腔、知识截止免责声明、猜测、过度赞同、填充词、堆叠限定词、空洞的正能量结尾。

它不会编造事实。姓名、数字、日期、引用或其他事实性细节必须来自原文或用户；缺失时应该询问或删掉，而不是补一个看起来合理的说法。

## 安装

技能位于 `skills/humanizer/`。下面的命令使用 `scarletcx` 账号；如果 fork 了项目，请替换成自己的账号。

### Skills CLI

```bash
npx skills add scarletcx/humanizer --global
```

去掉 `--global` 只安装到当前项目。可以用 `--agent <name>` 或 `--agent '*'` 选择 agent。

### 手动安装（大多数 agent）

```bash
git clone https://github.com/scarletcx/humanizer.git
cd humanizer
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/humanizer" ~/.agents/skills/humanizer
```

`~/.agents/skills/` 会被 Command Code、Codex、Gemini CLI、Cursor、GitHub Copilot 读取。

Claude Code 使用自己的目录：

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/humanizer" ~/.claude/skills/humanizer
```

项目内安装：

```bash
mkdir -p .agents/skills
cp -R /path/to/humanizer/skills/humanizer .agents/skills/humanizer
```

GitHub Copilot CLI：

```bash
gh skill install scarletcx/humanizer humanizer
gh skill preview scarletcx/humanizer humanizer
```

### Claude Code 插件

```text
/plugin marketplace add scarletcx/humanizer
/plugin install humanizer@humanizer
```

插件命令是 `/humanizer:humanizer`。

### Claude Desktop

下载仓库 ZIP，把 `skills/humanizer/` 作为 skill 上传。

## 使用

直接调用：

```text
/humanizer

[粘贴你的文字]
```

或者自然语言：

```text
请把这段文字 humanize：[你的文字]
```

改写文件：

```text
把 docs/launch-post.md 里的正文 humanize，代码和数据不要动。
```

### 匹配你的声音

如果想让改写更像你，附上一段自己的写作样本：

```text
/humanizer

这是我的写作样本，请匹配这个声音：
[粘贴 2-3 段自己的文字]

现在 humanize 这段：
[粘贴 AI 文字]
```

Humanizer 会跟随样本的节奏、用词、标点和刻意保留的怪癖；样本优先于默认风格规则。

## 仓库结构

```text
humanizer/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── NOTICE.md
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/humanizer/
│   ├── SKILL.md
│   ├── README.md              # 完整 35 条模式表和 before/after
│   ├── AGENTS.md              # 贡献者维护指南
│   ├── LICENSE
│   ├── agents/openai.yaml     # 可选 Codex UI 元数据
│   └── scripts/validate-package.py
├── tests/test_validate_package.py
└── .github/workflows/tests.yml
```

完整的 35 条模式、完整示例和版本历史见
[`skills/humanizer/README.md`](skills/humanizer/README.md)。

## 开发与校验

```bash
python3 skills/humanizer/scripts/validate-package.py
python3 -m unittest discover -s tests -v
```

校验器检查必需文件、frontmatter、版本一致性、35 条模式编号、插件路径和本地 Markdown 链接，只使用 Python 标准库。

## 许可与出处

- **原技能**：[blader/humanizer](https://github.com/blader/humanizer)，作者 Siqi Chen，MIT。
- **模式来源**：Wikipedia ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)，由 WikiProject AI Cleanup 维护；Wikipedia 文本采用 CC BY-SA，详见 [NOTICE.md](NOTICE.md)。
- **本 fork**：打包、校验器、测试和文档采用 MIT；35 条模式和技能行为保持不变。

详见 [LICENSE](LICENSE) 和 [NOTICE.md](NOTICE.md)。
