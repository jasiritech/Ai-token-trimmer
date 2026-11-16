# ✂️ ai-token-trimmer

> **Cut Claude & LLM coding token usage by up to 90%+** using classic Git workflows, ignore rules, and a zero-dependency Python AST mapper.

![Python](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen?style=flat-square)
![Token Savings](https://img.shields.io/badge/token%20savings-~90%25%2B-orange?style=flat-square)
![Workflow](https://img.shields.io/badge/workflow-git%20%2B%20ast-lightgrey?style=flat-square)

---

## 🚨 The Problem

AI coding assistants burn through token limits fast because they:
- Read **entire files** just to find one function
- Scan **logs, build artifacts, lockfiles, and `node_modules/`**
- Re-send **long conversation histories** on every follow-up prompt
- Rewrite **whole files** instead of returning minimal diffs

## 💡 The Solution

`ai-token-trimmer` brings back **classic, zero-cost repo tooling** (`ctags`-style indexing, `grep`, line slicing, and `git diff`) so your local machine does the searching for **0 tokens**, and the AI only sees the exact lines it needs.

| Approach | What the AI Sees | Typical Cost |
| :--- | :--- | :--- |
| ❌ **Default AI Workflow** | Full source files, logs, tests, and folders | ~35,000+ tokens |
| ✅ **With `ai-token-trimmer`** | Compact symbol map + targeted `--slice` + `git diff` | ~1,800–2,500 tokens (**~90–95% saved**) |

---

## ⚙️ How It Works

```text
1. Index locally (0 tokens)  ──▶  python repo_map.py
2. Search locally (0 tokens) ──▶  git grep -n "symbol"
3. Slice target lines only   ──▶  python repo_map.py --slice file.py 50 110
4. Patch via minimal diff    ──▶  git diff
```

---

## 📦 What's Inside

```text
ai-token-trimmer/
├── repo_map.py                 # Zero-dependency Python AST symbol mapper & line slicer
├── templates/
│   ├── .claudeignore           # Blocks logs/, node_modules/, dist/, lockfiles, & media
│   └── CLAUDE.md               # Rules instructing Claude Code to read slices & diffs only
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Copy into your project
Copy [`repo_map.py`](repo_map.py) (and optionally [`templates/.claudeignore`](templates/.claudeignore) and [`templates/CLAUDE.md`](templates/CLAUDE.md)) into your repository root.

### 2. Generate a compact symbol map
Instead of feeding whole files to your AI, generate a map of every class, method, and line range:

```bash
python repo_map.py
```

**Example output:**
```text
argon/agent.py (673 lines)
  class AgentConfig [L48-L65]
  class FindingAnalyzer [L221-L338]
    def analyze() [L231-L292]
  class ArgonAgent [L341-L623]
    def run() [L507-L575]
```

### 3. Slice only the lines you need
Once you know the exact line range, extract just that function:

```bash
python repo_map.py --slice argon/agent.py 507 575
```

### 4. Windows PowerShell Clipboard Shortcut
Send the map or slice straight to your clipboard and paste it into Claude, ChatGPT, or Gemini:

```powershell
python repo_map.py | clip
python repo_map.py --slice argon/agent.py 507 575 | clip
```

---

## 🛠️ Classic Git & CLI Habits That Save Even More Tokens

Pair `repo_map.py` with these built-in commands:

| Tool / Command | Purpose | Token Impact |
| :--- | :--- | :--- |
| `git grep -n "func_name"` | Find exact file & line before prompting | **0 tokens** |
| `git diff` / `git diff --stat` | Share only changed lines for review | **~80–90% smaller** |
| `git log --oneline -n 10` | Compact commit history | **Minimal context** |
| `gh pr diff <id>` | Inspect a Pull Request without web bloat | **Diff only** |
| `gh run view --log-failed` | Grab only the failing CI error lines | **Skips passing logs** |
| `.claudeignore` | Hide `logs/`, `dist/`, `*.lock`, images | **Prevents accidental reads** |

---

## 🧠 Best Practices

1. **Locate before reading** — Always run `repo_map.py` or `git grep` first.
2. **Ask for patches, not rewrites** — Tell the AI to output only the changed lines or a unified diff.
3. **Commit & reset chats** — After finishing one task, `git commit` and open a fresh chat so old context isn't re-sent on every message.
