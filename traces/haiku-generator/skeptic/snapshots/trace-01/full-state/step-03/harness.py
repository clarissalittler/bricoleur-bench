import subprocess
import sys

cmd = [sys.executable, "haiku.py", "--seed", "123", "--style", "haiku", "words/basic.txt"]
a = subprocess.run(cmd, text=True, capture_output=True)
b = subprocess.run(cmd, text=True, capture_output=True)
assert a.returncode == 0
assert b.returncode == 0
assert a.stdout == b.stdout
assert len(a.stdout.strip().splitlines()) == 3
