import argparse
import sys
from html import escape


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    args = p.parse_args()
    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    text = escape(args.text)
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}">')
    print('  <rect width="100%" height="100%" fill="#111111"/>')
    print(f'  <text x="20" y="{args.height//2}" fill="#ffffff" font-size="32">{text}</text>')
    print("</svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
