import argparse
import sys

from logo_core import THEMES, render_svg


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    p.add_argument("--theme", choices=sorted(THEMES.keys()), default="default")
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    theme = THEMES[args.theme]
    print(render_svg(args.text, args.width, args.height, theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
