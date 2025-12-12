message = " ".join(__import__("sys").argv[1:]) or "hi"

width = 20
inside = message[:width].ljust(width)

print("+" + "-" * (width + 2) + "+")
print("| " + inside + " |")
print("+" + "-" * (width + 2) + "+")
