def parse_grid(path: str) -> list[list[str]]:
    lines = [line.rstrip("\n") for line in open(path).read().splitlines() if line.strip()]
    if not lines:
        raise SystemExit("error: empty pattern")
    w = len(lines[0])
    if any(len(line) != w for line in lines):
        raise SystemExit("error: ragged grid")
    for line in lines:
        for ch in line:
            if ch not in (".", "#"):
                raise SystemExit("error: grid must contain only . and #")
    return [list(line) for line in lines]
