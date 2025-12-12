scale = input("convert to (c/f): ").strip().lower()
value = float(input("Temperature: "))

if scale == "f":
    print(value * 9/5 + 32)
elif scale == "c":
    print(value * 9/5 + 32)  # oops
else:
    print("unknown option")
