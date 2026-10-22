# Humanizer

[![tests](https://github.com/scarletcx/humanizer/actions/workflows/tests.yml/badge.svg)](https://github.com/scarletcx/humanizer/actions/workflows/tests.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Rewrite AI-sounding text so it reads like a person wrote it, without changing
what it says.

> This repository is a fork/packaging of
> [blader/humanizer](https://github.com/blader/humanizer), originally by Siqi
> Chen. The 35 patterns and skill behavior are unchanged. This fork updates
> install paths and packaging for cross-agent use.

[中文说明](README.zh-CN.md)

## Why it exists

AI-generated prose has recognizable habits: inflated importance, sales language,
vague sources, stock transitions, formulaic three-item lists, chatbot
pleasantries, and generic positive endings. Humanizer names those patterns and
rewrites the text without changing its facts.

It is not an "AI detector" and it does not add fake details. A name, number,
date, quote, citation, or other factual claim must come from the source or the
writer. If a detail is missing, the skill asks for it or uses a simpler sentence.

## What it does

- Checks text against **35 patterns** adapted from Wikipedia's
  ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
  maintained by WikiProject AI Cleanup.
- Keeps every claim while allowing structure, paragraph order, and sentence
  length to change.
- Matches the writer's voice when a writing sample is provided.
- Keeps technical and reference prose neutral; adds personality only when the
  text calls for it.
- Supports pasted text, file mode (prose only), and embedded mode (return only
  the final text).
- Works with Command Code, Claude Code, Codex, Gemini CLI, Cursor, GitHub
  Copilot, and other Agent Skills-compatible hosts.

## Install

The installable skill lives in `skills/humanizer/`. The commands below use the
`scarletcx` account; replace it with your own account if you fork the project.

### Skills CLI

```bash
npx skills add scarletcx/humanizer --global
```

Leave off `--global` to install only in the current project. Add
`--agent <name>` or `--agent '*'` to choose agents, then reload their skills.

### Manual install

Most Agent Skills hosts read `~/.agents/skills/`:

```bash
git clone https://github.com/scarletcx/humanizer.git
cd humanizer
mkdir -p ~/.agents/skills
ln -s "$(pwd)/skills/humanizer" ~/.agents/skills/humanizer
```

Claude Code reads `~/.claude/skills/` instead:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/humanizer" ~/.claude/skills/humanizer
```

Project-local install:

```bash
mkdir -p .agents/skills
cp -R /path/to/humanizer/skills/humanizer .agents/skills/humanizer
```

GitHub Copilot CLI:

```bash
gh skill install scarletcx/humanizer humanizer
gh skill preview scarletcx/humanizer humanizer
```

### Claude Code plugin

```text
/plugin marketplace add scarletcx/humanizer
/plugin install humanizer@humanizer
```

The plugin command is `/humanizer:humanizer`.

### Claude Desktop

Download this repository as a ZIP and upload `skills/humanizer/` as a skill.

## Use

Call the skill directly:

```text
/humanizer

[paste your text here]
```

Or ask in plain language:

```text
Please humanize this text: [your text]
```

To rewrite a file, give it the path:

```text
Humanize the prose in docs/launch-post.md
```

### Match your voice

If you want the rewrite to sound more like you, include a sample:

```text
/humanizer

Here's a sample of my writing for voice matching:
[paste 2-3 paragraphs of your own writing]

Now humanize this text:
[paste AI text to humanize]
```

Humanizer follows the sample's rhythm, word choice, punctuation, and deliberate
quirks. A writing sample takes priority over the default style rules.

## The 35 patterns

The full before/after table is in
[`skills/humanizer/README.md`](skills/humanizer/README.md). The categories are:

- **Content:** inflated importance, name-dropping, shallow `-ing` analysis, sales
  language, vague sources, formulaic challenges and outlook.
- **Language and grammar:** overused AI words, avoiding *is* and *are*, "not X
  but Y," forced groups of three, synonym cycling, false "from X to Y" ranges,
  passive voice, and missing subjects.
- **Style:** em/en dashes, excessive bold, bold list labels, title case in
  headings, emojis, curly quotes, hyphenated word pairs, fake deeper truths,
  announcing the next point, repeated headings, writing about an old version,
  forced punchlines, formulaic sayings, fake-candid openings, unraised
  objections, and fake alternatives.
- **Chatbot and filler:** UI pleasantries, knowledge-limit disclaimers, guesses,
  overly agreeable tone, filler phrases, stacked qualifiers, and generic
  positive endings.

Humanizer also checks for false positives. Perfect grammar, formal words, one
curly quote, or one em dash does not prove AI authorship; several patterns
together are stronger evidence.

## Repository layout

```text
humanizer/
├── README.md
├── README.zh-CN.md
├── LICENSE
├── NOTICE.md
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── scripts/validate-package.py
├── skills/humanizer/
│   ├── SKILL.md
│   ├── README.md
│   ├── AGENTS.md
│   ├── LICENSE
│   └── agents/openai.yaml
├── tests/test_validate_package.py
└── .github/workflows/tests.yml
```

## Development

```bash
python3 scripts/validate-package.py
python3 -m unittest discover -s tests -v
```

The validator checks the required files, frontmatter, version consistency,
35 pattern headings, plugin paths, and local Markdown links. It uses only the
Python standard library.

## License and attribution

- **Original skill:** [blader/humanizer](https://github.com/blader/humanizer) by
  Siqi Chen, MIT.
- **Pattern source:** Wikipedia's
  ["Signs of AI writing"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
  maintained by WikiProject AI Cleanup. Wikipedia text is available under
  CC BY-SA; see [NOTICE.md](NOTICE.md).
- **This fork:** packaging, validator, tests, and documentation are MIT. The
  35 patterns and skill behavior are unchanged.

See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for details.
