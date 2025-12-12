import subprocess
import sys
import tempfile

gen = subprocess.run([sys.executable, "maze.py", "gen", "--width", "9", "--height", "7", "--seed", "1"], text=True, capture_output=True)
assert gen.returncode == 0
maze_text = gen.stdout
assert "S" in maze_text and "E" in maze_text

tmp = tempfile.NamedTemporaryFile("w+", delete=False)
tmp.write(maze_text)
tmp.flush()

sol = subprocess.run([sys.executable, "maze.py", "solve", tmp.name], text=True, capture_output=True)
assert sol.returncode == 0
assert sol.stdout.strip().startswith("path_length=")
