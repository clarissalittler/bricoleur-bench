import argparse
import sys
from html import escape


THEMES = {
    "default": {"bg": "#111111", "fg": "#ffffff"},
    "invert": {"bg": "#ffffff", "fg": "#111111"},
}


def render(text: str, width: int, height: int, theme: str) -> str:
    t = escape(text)
    y = height // 2
    colors = THEMES[theme]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="100%" height="100%" fill="{colors["bg"]}"/>',
        f'<text x="20" y="{y}" fill="{colors["fg"]}" font-size="32">{t}</text>',
        "</svg>",
        "",
    ]
    return "\n".join(parts)


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
    print(render(args.text, args.width, args.height, args.theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
