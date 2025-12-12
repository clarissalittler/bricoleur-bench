# Trace 02 – Debugger (svg-logo-generator)

## Step 1: Add font-size fitting loop

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


THEMES = {
    "default": {"bg": "#111111", "fg": "#ffffff"},
    "invert": {"bg": "#ffffff", "fg": "#111111"},
}


def fit_font_size(text: str, width: int, base: int = 32) -> int:
    # crude heuristic: assume average char width ~ 0.6em
    if not text:
        return base
    max_chars = max(1, int((width - 40) / (base * 0.6)))
    if len(text) <= max_chars:
        return base
    scale = max_chars / len(text)
    return max(10, int(base * scale))


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
    t = escape(args.text)
    size = fit_font_size(args.text, args.width)
    y = args.height // 2
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}">')
    print(f'  <rect width="100%" height="100%" fill="{theme["bg"]}"/>')
    print(f'  <text x="20" y="{y}" fill="{theme["fg"]}" font-size="{size}">{t}</text>')
    print("</svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Keep output deterministic and validate theme

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


THEMES = {
    "default": {"bg": "#111111", "fg": "#ffffff"},
    "invert": {"bg": "#ffffff", "fg": "#111111"},
}


def fit_font_size(text: str, width: int, base: int = 32) -> int:
    if not text:
        return base
    max_chars = max(1, int((width - 40) / (base * 0.6)))
    if len(text) <= max_chars:
        return base
    scale = max_chars / len(text)
    return max(10, int(base * scale))


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
    t = escape(args.text)
    size = fit_font_size(args.text, args.width)
    y = args.height // 2
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}">')
    print(f'  <rect width="100%" height="100%" fill="{theme["bg"]}"/>')
    print(f'  <text x="20" y="{y}" fill="{theme["fg"]}" font-size="{size}">{t}</text>')
    print("</svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
