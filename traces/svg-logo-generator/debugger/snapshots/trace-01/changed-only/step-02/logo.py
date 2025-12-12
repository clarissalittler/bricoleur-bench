import argparse
import sys
from html import escape


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("text")
    p.add_argument("--width", type=int, default=200)
    p.add_argument("--height", type=int, default=100)
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    t = escape(args.text)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}"><text x="10" y="50">{t}</text></svg>'
    if "&" in args.text and "&amp;" not in svg:
        raise SystemExit("debug: escaping failed")
    print(svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
