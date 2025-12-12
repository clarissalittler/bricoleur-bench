#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


STEP_HEADING_RE = re.compile(r"^(#{2,3})\s+Step\s+(\d+)\s*(?:[:–—-]\s*(.*))?\s*$")
SNAPSHOT_LINE_RE = re.compile(r"^Snapshot:\s+(.+?)\s*$")
FENCE_START_RE = re.compile(r"^```(?:\w+)?\s*$")
FENCE_END_RE = re.compile(r"^```\s*$")


@dataclass
class Step:
    number: int
    title: str
    snapshots: dict[str, str] = field(default_factory=dict)


def iter_trace_files(traces_root: Path) -> Iterable[Path]:
    for path in traces_root.rglob("trace-*.md"):
        if "/snapshots/" in path.as_posix():
            continue
        yield path


def safe_rel_path(raw: str) -> Path:
    raw = raw.strip()
    if not raw:
        raise ValueError("Empty snapshot path")
    candidate = Path(raw)
    if candidate.is_absolute():
        raise ValueError(f"Snapshot path must be relative, got: {raw}")
    if any(part == ".." for part in candidate.parts):
        raise ValueError(f"Snapshot path must not contain '..', got: {raw}")
    return candidate


def parse_trace_markdown(trace_path: Path) -> list[Step]:
    lines = trace_path.read_text(encoding="utf-8").splitlines()

    steps: list[Step] = []
    current_step: Step | None = None

    i = 0
    while i < len(lines):
        line = lines[i]

        heading_match = STEP_HEADING_RE.match(line)
        if heading_match:
            step_no = int(heading_match.group(2))
            step_title = (heading_match.group(3) or "").strip()
            current_step = Step(number=step_no, title=step_title)
            steps.append(current_step)
            i += 1
            continue

        snapshot_match = SNAPSHOT_LINE_RE.match(line)
        if snapshot_match:
            if current_step is None:
                raise ValueError(f"{trace_path}: Snapshot before any Step heading")

            rel_path = safe_rel_path(snapshot_match.group(1))

            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1

            if j >= len(lines) or not FENCE_START_RE.match(lines[j]):
                raise ValueError(f"{trace_path}: Snapshot for {rel_path} missing fenced code block")

            j += 1
            content_lines: list[str] = []
            while j < len(lines) and not FENCE_END_RE.match(lines[j]):
                content_lines.append(lines[j])
                j += 1

            if j >= len(lines):
                raise ValueError(f"{trace_path}: Snapshot for {rel_path} missing closing fence")

            current_step.snapshots[rel_path.as_posix()] = "\n".join(content_lines).rstrip() + "\n"
            i = j + 1
            continue

        i += 1

    return sorted(steps, key=lambda s: s.number)


def trace_output_root(trace_path: Path, *, write_full_state: bool) -> Path:
    # Expected layout: traces/<problem>/<persona>/trace-01.md
    # Output: traces/<problem>/<persona>/snapshots/trace-01/<mode>/...
    mode = "full-state" if write_full_state else "changed-only"
    return trace_path.parent / "snapshots" / trace_path.stem / mode


def write_snapshots(trace_path: Path, steps: list[Step], *, write_full_state: bool, clean: bool) -> dict:
    out_root = trace_output_root(trace_path, write_full_state=write_full_state)
    if clean and out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    state: dict[str, str] = {}
    manifest_steps: list[dict] = []

    for step in steps:
        changed_files = sorted(step.snapshots.keys())
        for rel_path, content in step.snapshots.items():
            state[rel_path] = content

        step_dir = out_root / f"step-{step.number:02d}"
        step_dir.mkdir(parents=True, exist_ok=True)

        files_to_write = state.items() if write_full_state else [(p, state[p]) for p in changed_files]
        wrote_files: list[str] = []
        for rel_path_str, content in files_to_write:
            rel_path = safe_rel_path(rel_path_str)
            target = step_dir / rel_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            wrote_files.append(rel_path.as_posix())

        manifest_steps.append(
            {
                "number": step.number,
                "title": step.title,
                "changed_files": changed_files,
                "written_files": sorted(wrote_files),
                "all_files": sorted(state.keys()),
            }
        )

    manifest = {
        "trace": trace_path.as_posix(),
        "output_root": out_root.as_posix(),
        "write_full_state": write_full_state,
        "steps": manifest_steps,
    }
    (out_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Extract code snapshots from trace Markdown files.\n\n"
            "In a trace, add blocks like:\n"
            "  Snapshot: path/to/file.py\n"
            "  ```python\n"
            "  ...full file contents...\n"
            "  ```\n"
        )
    )
    parser.add_argument("--traces-root", type=Path, default=Path("traces"))
    parser.add_argument("--changed-only", action="store_true", help="Only write files changed in each step")
    parser.add_argument("--trace", type=Path, default=None, help="Extract only one trace file")
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Do not delete existing output before writing",
    )
    args = parser.parse_args(argv)

    traces_root: Path = args.traces_root
    if args.changed_only:
        write_full_state = False
    else:
        write_full_state = True
    clean = not args.no_clean

    trace_files = [args.trace] if args.trace else list(iter_trace_files(traces_root))
    if not trace_files:
        raise SystemExit(f"No trace files found under {traces_root}")

    manifests = []
    for trace_path in sorted(trace_files):
        steps = parse_trace_markdown(trace_path)
        if not steps:
            continue
        manifests.append(write_snapshots(trace_path, steps, write_full_state=write_full_state, clean=clean))

    summary = {
        "count": len(manifests),
        "traces": [m["trace"] for m in manifests],
    }
    summary_path = traces_root / "snapshots-summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv[1:]))
