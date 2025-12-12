import argparse
import sys

from maze_core import gen, solve_length
from maze_io import parse, render


def main() -> int:
    p = argparse.ArgumentParser(prog="maze.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gen")
    g.add_argument("--width", type=int, required=True)
    g.add_argument("--height", type=int, required=True)
    g.add_argument("--seed", type=int, required=True)
    s = sub.add_parser("solve")
    s.add_argument("maze")
    args = p.parse_args()

    try:
        if args.cmd == "gen":
            maze = gen(args.width, args.height, args.seed)
            print(render(maze), end="")
            return 0

        maze = parse(args.maze)
        dist = solve_length(maze)
        if dist is None:
            print("error: unsolvable", file=sys.stderr)
            return 1
        print(f"path_length={dist}")
        return 0
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
