import subprocess
import sys

expected = "+----+\n| hi |\n+----+\n"
out = subprocess.run([sys.executable, "poster.py", "hi", "--width", "2"], text=True, capture_output=True)
assert out.returncode == 0
assert out.stdout == expected
