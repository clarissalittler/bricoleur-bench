import argparse
from html import escape


def render(text: str, width: int, height: int, theme: str) -> str:
    if theme == "default":
        bg = "#111111"
        fg = "#ffffff"
    else:
        bg = "#ffffff"
        fg = "#111111"

    t = escape(text)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="{bg}"/>'
        f'<text x="20" y="{height//2}" fill="{fg}" font-size="32">{t}</text>'
        f"</svg>\n"
    )


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    p.add_argument("--theme", choices=["default", "invert"], default="default")
    args = p.parse_args()
    print(render(args.text, args.width, args.height, args.theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
