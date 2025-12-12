import argparse

from poster_core import render


def main() -> int:
    parser = argparse.ArgumentParser(prog="poster.py", description="Render an ASCII poster.")
    parser.add_argument("message")
    parser.add_argument("--width", type=int, default=20)
    parser.add_argument("--align", choices=["left", "center", "right"], default="left")
    parser.add_argument("--border", choices=["ascii", "none"], default="ascii")
    args = parser.parse_args()

    if args.width < 1:
        raise SystemExit("error: --width must be >= 1")

    print(render(args.message, args.width, args.align, args.border), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
