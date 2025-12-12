import subprocess
import sys

run = subprocess.run(
    [sys.executable, "life.py", "--steps", "1", "patterns/blinker.txt"],
    text=True,
    capture_output=True,
)
assert run.returncode == 0
out = run.stdout.strip().splitlines()
assert len(out) > 0
