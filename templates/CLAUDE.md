# Repo Token-Saving Rules for Claude

1. **Locate before reading**: Run `python repo_map.py` or `git grep -n "<symbol>"` first instead of reading full files.
2. **Read line ranges only**: Use `python repo_map.py --slice <file> <start> <end>` or read only the relevant function lines.
3. **Use `git diff`**: Inspect `git diff` / `git diff --stat` for changes instead of re-reading modified files.
4. **Ignore heavy dirs**: Do not read `logs/`, `node_modules/`, `dist/`, or build outputs unless explicitly asked.
5. **Minimal output**: Prefer targeted edits or unified diffs over rewriting entire files.
