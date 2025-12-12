import argparse
import sys
from html import escape


def render(text: str, width: int, height: int) -> str:
    t = escape(text)
    y = height // 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="#111111"/>'
        f'<text x="20" y="{y}" fill="#ffffff" font-size="32">{t}</text>'
        f"</svg>\n"
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    args = p.parse_args()
    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1
    print(render(args.text, args.width, args.height), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
