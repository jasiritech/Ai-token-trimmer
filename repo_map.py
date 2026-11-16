"""Lightweight Python repo indexer & slicer (ctags/tree/slice replacement) to save AI tokens."""

from __future__ import annotations

import argparse
import ast
from pathlib import Path

SKIP_DIRS = {
    ".git",
    ".agents",
    "__pycache__",
    ".pytest_cache",
    "logs",
    "evidence",
    "reports",
    "scratch",
    "docs",
    "node_modules",
    ".venv",
    "venv",
}


def iter_python_files(root: Path) -> list[Path]:
    """Return sorted Python files excluding ignored directories."""
    files: list[Path] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def summarize_file(path: Path, root: Path) -> list[str]:
    """Extract top-level classes, functions, and methods with line ranges."""
    rel = path.relative_to(root).as_posix()
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rel)
    except (OSError, SyntaxError) as exc:
        return [f"{rel}: <parse error: {exc}>"]

    lines = [f"{rel} ({len(source.splitlines())} lines)"]
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            end = getattr(node, "end_lineno", node.lineno)
            lines.append(f"  class {node.name} [L{node.lineno}-L{end}]")
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    iend = getattr(item, "end_lineno", item.lineno)
                    lines.append(f"    def {item.name}() [L{item.lineno}-L{iend}]")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            end = getattr(node, "end_lineno", node.lineno)
            lines.append(f"  def {node.name}() [L{node.lineno}-L{end}]")
    return lines


def slice_file(path: Path, start: int, end: int) -> str:
    """Print numbered lines from start to end (1-indexed, inclusive)."""
    all_lines = path.read_text(encoding="utf-8").splitlines()
    start_idx = max(1, start)
    end_idx = min(len(all_lines), end)
    out = [f"--- {path.as_posix()} [L{start_idx}-L{end_idx}] ---"]
    for lineno in range(start_idx, end_idx + 1):
        out.append(f"{lineno:4d}: {all_lines[lineno - 1]}")
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Token-saving repo map & file slicer.")
    parser.add_argument("--slice", nargs=3, metavar=("FILE", "START", "END"), help="Print a specific line range.")
    parser.add_argument("--stats", action="store_true", help="Compare full Python source size vs. repo_map output.")
    args = parser.parse_args()

    root = Path.cwd()
    if args.slice:
        file_path = Path(args.slice[0])
        print(slice_file(file_path, int(args.slice[1]), int(args.slice[2])))
        return

    py_files = iter_python_files(root)
    map_lines: list[str] = []
    for py_file in py_files:
        map_lines.extend(summarize_file(py_file, root))
    map_output = "\n".join(map_lines)

    if args.stats:
        full_chars = sum(len(p.read_text(encoding="utf-8", errors="replace")) for p in py_files)
        map_chars = len(map_output)
        reduction = (1 - (map_chars / full_chars)) * 100 if full_chars else 0.0
        print(f"Files: {len(py_files)} Python files")
        print(f"Full source: {full_chars:,} chars (~{round(full_chars / 4):,} tokens)")
        print(f"Repo map:    {map_chars:,} chars (~{round(map_chars / 4):,} tokens)")
        print(f"Index size reduction: {reduction:.1f}% (approximate; exact tokens depend on tokenizer)")
        return

    print(map_output)


if __name__ == "__main__":
    main()
