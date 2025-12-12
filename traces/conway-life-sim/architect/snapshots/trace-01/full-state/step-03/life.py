import argparse
import sys
from pathlib import Path

from life_core import step
from life_io import parse_grid, render


def main() -> int:
    p = argparse.ArgumentParser(prog="life.py")
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("pattern", type=Path)
    args = p.parse_args()
    if args.steps < 0:
        print("error: --steps must be >= 0", file=sys.stderr)
        return 1

    try:
        grid = parse_grid(args.pattern)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(render(grid))
    for _ in range(args.steps):
        print()
        grid = step(grid)
        print(render(grid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
