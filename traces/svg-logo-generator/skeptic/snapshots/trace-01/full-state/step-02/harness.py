import subprocess
import sys

run = subprocess.run([sys.executable, "logo.py", "Hello"], text=True, capture_output=True)
assert run.returncode == 0
out = run.stdout.strip()
assert out.startswith("<svg") or "<svg" in out
assert out.endswith("</svg>") or "</svg>" in out
assert "<text" in out
