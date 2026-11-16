# ai-token-trimmer

Cut Claude / LLM coding token usage by **~90%+** using classic Git commands and a zero-dependency Python AST indexer (`repo_map.py`).

Instead of letting an AI assistant read entire files, logs, and build artifacts, `ai-token-trimmer` gives it:
1. A compact **symbol map** (classes, functions, and exact line ranges)
2. **Line-range slicing** (`--slice`) for reading only the target function
3. **Ignore templates** (`.claudeignore`, `CLAUDE.md`) to block heavy directories and enforce diff-first workflows

## Files Included

- `repo_map.py` — Zero-dependency Python AST mapper & line slicer (`ctags` + `sed` alternative)
- `templates/.claudeignore` — Blocks `logs/`, `node_modules/`, `__pycache__/`, build outputs, and media
- `templates/CLAUDE.md` — Instructs Claude Code to locate symbols first and edit via minimal diffs

## Quick Start

Copy `repo_map.py` (and optionally `templates/.claudeignore` and `templates/CLAUDE.md`) into your project root:

```bash
# 1. Generate a compact map of all classes, functions, and line numbers
python repo_map.py

# 2. Slice only the lines you need
python repo_map.py --slice path/to/file.py 50 120

# 3. Search locally before asking the AI (0 tokens)
git grep -n "my_function"

# 4. Review or share only changes
git diff
```

On Windows PowerShell, pipe directly to clipboard:

```powershell
python repo_map.py | clip
python repo_map.py --slice path/to/file.py 50 120 | clip
```
