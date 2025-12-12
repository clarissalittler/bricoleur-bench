import sys
import textwrap

message = " ".join(sys.argv[1:]) or "hi"

width = 20
lines = textwrap.wrap(message, width=width) or [""]

print("+" + "-" * width + "+")  # oops: should include padding
for line in lines:
    print("| " + line.ljust(width) + " |")
print("+" + "-" * width + "+")
