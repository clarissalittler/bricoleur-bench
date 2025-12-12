import argparse
import sys
from html import escape


THEMES = {
    "default": {"bg": "#222222", "fg": "#fefefe"},
    "mint": {"bg": "#0b3d2e", "fg": "#b9f6ca"},
}


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=320)
    p.add_argument("--height", type=int, default=120)
    p.add_argument("--theme", choices=sorted(THEMES.keys()), default="default")
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    theme = THEMES[args.theme]
    t = escape(args.text)
    y = args.height // 2 + 14
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}">')
    print(f'  <rect x="0" y="0" width="{args.width}" height="{args.height}" rx="16" fill="{theme["bg"]}"/>')
    print(f'  <text x="24" y="{y}" fill="{theme["fg"]}" font-size="36">{t}</text>')
    print("</svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
