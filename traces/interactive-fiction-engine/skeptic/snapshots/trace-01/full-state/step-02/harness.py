import subprocess
import sys

run = subprocess.run(
    [sys.executable, "play.py", "example-story.json"],
    input="1\n",
    text=True,
    capture_output=True,
)
assert run.returncode == 0
assert "1." in run.stdout
assert "> " in run.stdout or run.stdout.endswith("> ") or run.stdout.endswith(">\n")
