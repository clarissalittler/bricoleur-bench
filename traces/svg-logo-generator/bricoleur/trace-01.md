# Trace 01 – Bricoleur (SVG Logo Generator)

Starts with “print some SVG”, then slowly adds flags and escaping when things break.

## Step 1: Tiny SVG with text (no escaping)

Snapshot: logo.py
```python
import sys

text = " ".join(sys.argv[1:]) or "Hello"
print(f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120">')
print(f'  <rect width="100%" height="100%" fill="black"/>')
print(f'  <text x="20" y="70" fill="white" font-size="32">{text}</text>')
print("</svg>")
```

Notes: Works until the text includes `&` or `<`.

## Step 2: Add escaping and simple theme flag

Snapshot: logo.py
```python
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
```

Notes: Now `Hello & goodbye` doesn’t break the XML.

## Step 3: Validate dimensions and keep output stable

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


def render(text: str, width: int, height: int, theme: str) -> str:
    if theme == "default":
        bg = "#111111"
        fg = "#ffffff"
    elif theme == "invert":
        bg = "#ffffff"
        fg = "#111111"
    else:
        raise ValueError("unknown theme")

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
    p.add_argument("--theme", choices=["default", "invert"], default="default")
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    print(render(args.text, args.width, args.height, args.theme), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
