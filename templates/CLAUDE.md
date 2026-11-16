# Repo Token-Saving Rules for Claude

1. **Locate before reading**: Run `python repo_map.py` or `git grep -n "<symbol>"` first instead of reading full files.
2. **Preserve context**: When slicing a function with `python repo_map.py --slice <file> <start> <end>`, check top-of-file imports and callers if needed.
3. **Use `git diff`**: Inspect `git diff` / `git diff --stat` for changes instead of re-reading modified files.
4. **Ignore heavy dirs**: Respect `.gitignore` and `permissions.deny` (do not read `logs/`, `dist/`, `node_modules/`, or build outputs unless asked).
5. **Minimal output**: Prefer targeted edits or unified diffs over rewriting entire files.
