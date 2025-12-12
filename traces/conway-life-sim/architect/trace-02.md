# Trace 02 – Architect (conway-life-sim)

## Step 1: Add `--wrap` option

Snapshot: life.py
```python
import argparse
import sys


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def parse_lines(path: str) -> list[str]:
    raw = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit("error: empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit("error: ragged grid")
    for l in raw:
        for ch in l:
            if ch not in (".", "#"):
                raise SystemExit("error: grid must contain only . and #")

    return raw


def step(lines: list[str], wrap: bool) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if wrap:
                    ny %= h
                    nx %= w
                    if lines[ny][nx] == "#":
                        n += 1
                else:
                    if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == "#":
                        n += 1
            alive = lines[y][x] == "#"
            row.append("#" if (alive and n in (2, 3)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


def main() -> int:
    p = argparse.ArgumentParser(prog="life.py")
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("--wrap", action="store_true")
    p.add_argument("pattern")
    args = p.parse_args()
    if args.steps < 0:
        print("error: --steps must be >= 0", file=sys.stderr)
        return 1
    lines = parse_lines(args.pattern)
    print("\n".join(lines))
    for _ in range(args.steps):
        print()
        lines = step(lines, wrap=args.wrap)
        print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Step 2: Keep default rendering stable; add `--alive` and `--dead` chars

Snapshot: life.py
```python
import argparse
import sys


OFFSETS = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if not (dx == 0 and dy == 0)]


def parse_lines(path: str) -> list[str]:
    raw = [l.rstrip("\n") for l in open(path).read().splitlines() if l.strip()]
    if not raw:
        raise SystemExit("error: empty pattern")
    w = len(raw[0])
    if any(len(l) != w for l in raw):
        raise SystemExit("error: ragged grid")
    for l in raw:
        for ch in l:
            if ch not in (".", "#"):
                raise SystemExit("error: grid must contain only . and #")

    return raw


def step(lines: list[str], wrap: bool) -> list[str]:
    h = len(lines)
    w = len(lines[0])
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            n = 0
            for dx, dy in OFFSETS:
                ny, nx = y + dy, x + dx
                if wrap:
                    ny %= h
                    nx %= w
                    if lines[ny][nx] == "#":
                        n += 1
                else:
                    if 0 <= ny < h and 0 <= nx < w and lines[ny][nx] == "#":
                        n += 1
            alive = lines[y][x] == "#"
            row.append("#" if (alive and n in (2, 3)) or ((not alive) and n == 3) else ".")
        out.append("".join(row))
    return out


def render(lines: list[str], alive: str, dead: str) -> str:
    if alive == "#" and dead == ".":
        return "\n".join(lines)
    return "\n".join("".join(alive if ch == "#" else dead for ch in row) for row in lines)


def main() -> int:
    p = argparse.ArgumentParser(prog="life.py")
    p.add_argument("--steps", type=int, required=True)
    p.add_argument("--wrap", action="store_true")
    p.add_argument("--alive", default="#")
    p.add_argument("--dead", default=".")
    p.add_argument("pattern")
    args = p.parse_args()
    if args.steps < 0:
        print("error: --steps must be >= 0", file=sys.stderr)
        return 1
    lines = parse_lines(args.pattern)
    print(render(lines, args.alive, args.dead))
    for _ in range(args.steps):
        print()
        lines = step(lines, wrap=args.wrap)
        print(render(lines, args.alive, args.dead))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```
