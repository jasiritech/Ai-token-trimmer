# ✂️ ai-token-trimmer

> **Trim unnecessary context sent to LLMs** using classic Git workflows, ignore rules, and a zero-dependency Python AST mapper.

![Python](https://img.shields.io/badge/python-3.9%2B-blue?style=flat-square)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Scope](https://img.shields.io/badge/parser-python%20ast-lightgrey?style=flat-square)

---

## 🚨 The Problem

When working with web chats (copy-paste) or unguided prompts, LLMs consume extra tokens when they:
- Receive **entire files** just to locate one function
- Scan **logs, build artifacts, lockfiles, and `node_modules/`**
- Re-send large uncached context or rewrite **whole files** instead of returning minimal diffs

## 💡 The Solution

`ai-token-trimmer` pairs **classic local tooling** (`ctags`-style indexing, `git grep`, line slicing, and `git diff`) so your machine does the searching locally (spending **0 LLM tokens**), and you only share the relevant symbol map and target slices.

> **Note on savings:** End-to-end task savings vary by task and tool — biggest when using **web chat (copy-paste)**, and more modest in **agentic CLIs** like Claude Code that already use `grep`/`glob` and prompt caching.

---

## 📊 Reproducible Map-Size Measurement

Measured on a 21-file Python codebase (`argon/*.py` + `tests/*.py`, using the `~4 chars/token` heuristic):
- **Full source files:** `140,784` chars (~35,196 tokens)
- **`python repo_map.py` output:** `7,523` chars (~1,881 tokens)
- **Initial index reduction:** **94.7% smaller** than pasting every `.py` file

*Ratio is approximate; exact token counts depend on the tokenizer.*

You can measure the exact ratio on your own Python repo (Windows, macOS, or Linux) with:

```bash
python repo_map.py --stats
```

---

## ⚙️ How It Works

```text
1. Index locally (0 LLM tokens)  ──▶  python repo_map.py
2. Search callers & imports      ──▶  git grep -n "symbol"
3. Slice target lines only       ──▶  python repo_map.py --slice file.py 50 110
4. Patch via minimal diff        ──▶  git diff  (ask the AI to reply with a unified diff only)
```

---

## 📦 What's Inside

```text
ai-token-trimmer/
├── repo_map.py                 # Zero-dependency Python AST symbol mapper & line slicer
├── templates/
│   ├── CLAUDE.md               # Rules instructing Claude Code to locate first & prefer diffs
│   └── settings.example.json   # Example permissions.deny rules for Claude Code
├── LICENSE                     # MIT License
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Copy into your project
Copy [`repo_map.py`](repo_map.py) (and optionally [`templates/CLAUDE.md`](templates/CLAUDE.md) or [`templates/settings.example.json`](templates/settings.example.json)) into your repository root.

### 2. Generate a compact symbol map (Python)
Instead of pasting whole `.py` files, generate a map of every class, method, and line range:

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
Once you know the exact line range, extract just that function (and check imports/callers with `git grep` so you don't lose context):

```bash
python repo_map.py --slice argon/agent.py 507 575
```

### 4. Windows PowerShell Clipboard Shortcut
Send the map or slice straight to your clipboard and paste it into Claude, ChatGPT, or Gemini:

```powershell
python repo_map.py | clip
python repo_map.py --slice argon/agent.py 507 575 | clip
```

### 5. Claude Code `permissions.deny` Example
Place this in `.claude/settings.json` (in addition to `.gitignore`) to block heavy non-code directories:

```json
{
  "permissions": {
    "deny": [
      "Read(logs/**)",
      "Read(reports/**)",
      "Read(dist/**)",
      "Read(node_modules/**)",
      "Read(**/*.log)",
      "Read(**/*.lock)"
    ]
  }
}
```

---

## 🛠️ Classic Git & CLI Habits That Save Tokens

| Tool / Command | Purpose | Why It Helps |
| :--- | :--- | :--- |
| `git grep -n "func_name"` | Find exact file, imports & callers | **0 LLM tokens** spent searching |
| `git diff` / `git diff --stat` | Share only changed lines for review | Avoids re-sending full files |
| `git log --oneline -n 10` | Compact commit history | Minimal context |
| `gh pr diff <id>` | Inspect a Pull Request via CLI | Diff only |
| `gh run view --log-failed` | Grab only failing CI log lines | Skips passing logs |
| `.gitignore` & `permissions.deny` | Hide `logs/`, `dist/`, `*.lock`, images | Prevents accidental reads in Claude Code |

---

## ⚠️ Current Limitations & Roadmap

1. **Python only (for now)** — `repo_map.py` uses Python's built-in `ast` module, so it indexes `.py` files only.
   - *Roadmap:* Optional `tree-sitter` backend to support JavaScript/TypeScript, Go, Rust, and PHP.
2. **Don't lose context when slicing** — When sharing a function slice, include the file's top `imports` (e.g., lines `1-30`) or `git grep` callers if the function depends on external types.
3. **Commit & reset chats** — After finishing a task, `git commit` and start a fresh chat to keep context focused.

## 📄 License

MIT — see [LICENSE](LICENSE).
