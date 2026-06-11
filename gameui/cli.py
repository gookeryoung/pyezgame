"""GameUI CLI - Run GameLib examples from the command line."""
from __future__ import annotations
import argparse
import importlib.util
import sys
from pathlib import Path

# Installed: gameui/examples/; Dev: ../examples/ (relative to gameui/)
_pkg_dir = Path(__file__).resolve().parent
_candidates = [_pkg_dir / "examples", _pkg_dir.parent / "examples"]
EXAMPLES_DIR = next((p for p in _candidates if p.is_dir()), _pkg_dir / "examples")


def _discover_examples() -> list[tuple[str, str, str]]:
    """Return sorted list of (number, name, filepath) tuples."""
    results: list[tuple[str, str, str]] = []
    if not EXAMPLES_DIR.is_dir():
        return results
    for f in sorted(EXAMPLES_DIR.glob("*.py")):
        if f.name.startswith("_"):
            continue
        num, _, rest = f.stem.partition("_")
        if num.isdigit():
            results.append((num, rest.replace("_", " "), str(f)))
    return results


def _run_example(filepath: str) -> None:
    import os
    # Change cwd to the examples directory so relative asset paths work
    prev_cwd = os.getcwd()
    os.chdir(EXAMPLES_DIR)
    try:
        spec = importlib.util.spec_from_file_location("__main__", filepath)
        if spec is None or spec.loader is None:
            print(f"Error: cannot load {filepath}")
            sys.exit(1)
        mod = importlib.util.module_from_spec(spec)
        mod.__name__ = "__main__"
        spec.loader.exec_module(mod)
    finally:
        os.chdir(prev_cwd)


def cmd_list(_args: argparse.Namespace) -> None:
    """List all available examples."""
    examples = _discover_examples()
    if not examples:
        print("No examples found.")
        return
    print("Available examples:")
    for num, name, _ in examples:
        print(f"  {num}. {name}")
    print("\nRun: gameui <number|name>")


def cmd_run(args: argparse.Namespace) -> None:
    """Run an example by number or name keyword."""
    query: str = args.example.lower()  # pyright: ignore[reportAny]
    examples = _discover_examples()
    if not examples:
        print("No examples found.")
        sys.exit(1)

    # Match by number or name keyword
    match = None
    for num, name, filepath in examples:
        if num == query or query in name.lower() or query in num.lower():
            match = filepath
            break

    if match is None:
        print(f"Example '{args.example}' not found.\n")  # pyright: ignore[reportAny]
        print("Use 'gameui list' to see available examples.\n")
        sys.exit(1)

    _run_example(match)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="gameui",
        description="GameUI - Run GameLib examples",
    )
    sub = parser.add_subparsers(dest="command")

    # list
    _ = sub.add_parser("list", help="List all available examples")

    # run
    run_p = sub.add_parser("run", help="Run an example by number or name")
    _ = run_p.add_argument("example", help="Example number (e.g. 01) or name keyword (e.g. snake)")

    args = parser.parse_args()

    if args.command == "list": # pyright: ignore[reportAny]
        cmd_list(args)
    elif args.command == "run": # pyright: ignore[reportAny]
        cmd_run(args)
    elif args.command is None: # pyright: ignore[reportAny]
        parser.print_help()
        print()
        cmd_list(args)


if __name__ == "__main__":
    main()
