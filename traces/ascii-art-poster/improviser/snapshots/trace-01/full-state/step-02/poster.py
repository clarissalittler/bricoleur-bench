import sys
import textwrap

msg = " ".join(sys.argv[1:]) or "hi"
width = 24
align = "center"

lines = textwrap.wrap(msg, width=width) or [""]
if align == "center":
    lines = [line.center(width) for line in lines]

print("+" + "-" * (width + 2) + "+")
for line in lines:
    print("| " + line + " |")
print("+" + "-" * (width + 2) + "+")
