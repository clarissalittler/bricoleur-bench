# Trace 01 – Improviser (SVG Logo Generator)

Spikes a couple looks, then standardizes output + flags.

## Step 1: Quick “badge” look

Snapshot: logo.py
```python
import sys

text = " ".join(sys.argv[1:]) or "Hello"
print('<svg xmlns="http://www.w3.org/2000/svg" width="320" height="120">')
print('  <rect x="0" y="0" width="320" height="120" rx="16" fill="#222"/>')
print(f'  <text x="24" y="74" fill="#fefefe" font-size="36">{text}</text>')
print("</svg>")
```

Notes: Wants to make size configurable.

## Step 2: Argparse + escape text

Snapshot: logo.py
```python
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
```

Notes: Ok; now add a theme flag.

## Step 3: Theme flag + validation

Snapshot: logo.py
```python
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
```
