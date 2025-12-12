scale = input("convert to (c/f): ").strip().lower()
if not scale:
    raise SystemExit("Need a target scale")

try:
    value = float(input("Temperature: "))
except ValueError:
    raise SystemExit("Temperature must be a number")

if scale == "f":
    print(value * 9/5 + 32)
elif scale == "c":
    print((value - 32) * 5/9)
else:
    print("unknown option")
