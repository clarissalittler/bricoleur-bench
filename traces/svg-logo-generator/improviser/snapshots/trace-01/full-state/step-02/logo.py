import argparse
from html import escape


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("text")
    p.add_argument("--width", type=int, default=320)
    p.add_argument("--height", type=int, default=120)
    args = p.parse_args()

    t = escape(args.text)
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}">')
    print(f'  <rect x="0" y="0" width="{args.width}" height="{args.height}" rx="16" fill="#222"/>')
    print(f'  <text x="24" y="{args.height//2 + 14}" fill="#fefefe" font-size="36">{t}</text>')
    print("</svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
