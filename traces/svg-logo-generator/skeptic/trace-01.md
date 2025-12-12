# Trace 01 – Skeptic (SVG Logo Generator)

Pins minimal structural properties of the SVG output.

## Step 1: Harness first (must contain <svg>, </svg>, and <text>)

Snapshot: harness.py
```python
import subprocess
import sys

run = subprocess.run([sys.executable, "logo.py", "Hello"], text=True, capture_output=True)
assert run.returncode == 0
out = run.stdout.strip()
assert out.startswith("<svg") or "<svg" in out
assert out.endswith("</svg>") or "</svg>" in out
assert "<text" in out
```

Notes: Fails because `logo.py` doesn’t exist.

## Step 2: Minimal implementation to satisfy harness

Snapshot: logo.py
```python
import sys
from html import escape

text = escape(" ".join(sys.argv[1:]) or "Hello")
print('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120">')
print('  <rect width="100%" height="100%" fill="#111111"/>')
print(f'  <text x="20" y="60" fill="#ffffff" font-size="32">{text}</text>')
print("</svg>")
```

Notes: Harness passes; now add flags and validation.

## Step 3: CLI flags and validation (keeps structure stable)

Snapshot: logo.py
```python
import argparse
import sys
from html import escape


def main() -> int:
    p = argparse.ArgumentParser(prog="logo.py")
    p.add_argument("text")
    p.add_argument("--width", type=int, default=300)
    p.add_argument("--height", type=int, default=120)
    args = p.parse_args()
    if args.width < 1 or args.height < 1:
        print("error: width/height must be positive", file=sys.stderr)
        return 1

    text = escape(args.text)
    print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{args.width}" height="{args.height}">')
    print('  <rect width="100%" height="100%" fill="#111111"/>')
    print(f'  <text x="20" y="{args.height//2}" fill="#ffffff" font-size="32">{text}</text>')
    print("</svg>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
