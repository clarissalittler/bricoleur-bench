from __future__ import annotations

import random
from collections import deque

from maze_io import Maze


def gen(width: int, height: int, seed: int) -> Maze:
    if width < 3 or height < 3:
        raise ValueError("width/height must be >= 3")
    rng = random.Random(seed)
    grid = [["#"] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            grid[y][x] = "."

    sx, sy = 1, 1
    ex, ey = width - 2, height - 2
    path = {(sx, sy)}
    x, y = sx, sy
    while (x, y) != (ex, ey):
        if rng.random() < 0.5 and x < ex:
            x += 1
        elif y < ey:
            y += 1
        path.add((x, y))

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if (x, y) in path:
                continue
            if rng.random() < 0.30:
                grid[y][x] = "#"

    grid[sy][sx] = "S"
    grid[ey][ex] = "E"
    return Maze(grid)


def solve_length(maze: Maze) -> int | None:
    w = maze.width
    h = maze.height
    start = next((x, y) for y in range(h) for x in range(w) if maze.grid[y][x] == "S")
    end = next((x, y) for y in range(h) for x in range(w) if maze.grid[y][x] == "E")

    q = deque([(start[0], start[1], 0)])
    visited = [[False] * w for _ in range(h)]
    visited[start[1]][start[0]] = True
    while q:
        x, y, d = q.popleft()
        if (x, y) == end:
            return d
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny][nx]:
                if maze.grid[ny][nx] in (".", "E"):
                    visited[ny][nx] = True
                    q.append((nx, ny, d + 1))
    return None
