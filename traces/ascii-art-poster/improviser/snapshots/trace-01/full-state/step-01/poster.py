import sys

msg = " ".join(sys.argv[1:]) or "hi"
width = 24

print("+" + "-" * (width + 2) + "+")
print("| " + msg[:width].ljust(width) + " |")
print("+" + "-" * (width + 2) + "+")
