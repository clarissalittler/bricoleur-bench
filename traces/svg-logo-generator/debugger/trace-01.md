# Trace 01 – Debugger (SVG Logo Generator)

Repro targets: invalid XML when text contains `&`, and negative sizes.

## Step 1: Broken XML with special characters

Snapshot: logo.py
```python
import sys

text = " ".join(sys.argv[1:])
print('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">')
print(f"<text x='10' y='50'>{text}</text>")
print("</svg>")
```

Notes: `python logo.py "a & b"` yields invalid XML. Next: escape and add size validation.

## Step 2: Escape + add a quick probe

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("text")
    p.add_argument("--width", type=int, default=200)
    p.add_argument("--height", type=int, default=100)
    args = p.parse_args()

    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    t = escape(args.text)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}"><text x="10" y="50">{t}</text></svg>'
    if "&" in args.text and "&amp;" not in svg:
        raise SystemExit("debug: escaping failed")
    print(svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Notes: Adds theming after correctness is pinned.

## Step 3: Theme flag + stable formatting

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


THEMES = {
    "default": {"bg": "#111111", "fg": "#ffffff"},
    "invert": {"bg": "#ffffff", "fg": "#111111"},
}


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
    y = args.height // 2
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}">')
    print(f'  <rect width="100%" height="100%" fill="{theme["bg"]}"/>')
    print(f'  <text x="20" y="{y}" fill="{theme["fg"]}" font-size="32">{t}</text>')
    print("</svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
