import argparse
from html import escape


def render(text: str, width: int, height: int, bg: str, fg: str) -> str:
    t = escape(text)
    y = height // 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="{bg}"/>'
        f'<text x="20" y="{y}" fill="{fg}" font-size="32">{t}</text>'
        f"</svg>\n"
    )


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    p.add_argument("--theme", choices=["default"], default="default")
    args = p.parse_args()
    print(render(args.text, args.width, args.height, bg="#111111", fg="#ffffff"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
