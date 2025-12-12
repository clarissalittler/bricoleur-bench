import subprocess
import sys
import tempfile
from pathlib import Path


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "count_words.py", *args], text=True, capture_output=True)


def write_tmp(contents: str) -> Path:
    f = tempfile.NamedTemporaryFile("w+", delete=False)
    f.write(contents)
    f.flush()
    return Path(f.name)


empty = write_tmp("")
punct = write_tmp("!!! ... ---")
contractions = write_tmp("Don't stop. Can't stop.")

assert run([str(empty)]).returncode == 0
assert run([str(empty)]).stdout == ""

assert run([str(punct)]).returncode == 0
assert run([str(punct)]).stdout == ""

missing = run(["nope-does-not-exist.txt"])
assert missing.returncode != 0
assert "missing file" in (missing.stderr + missing.stdout).lower()
