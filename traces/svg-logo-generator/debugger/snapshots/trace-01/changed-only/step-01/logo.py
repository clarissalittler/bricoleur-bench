import sys

text = " ".join(sys.argv[1:])
print('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100">')
print(f"<text x='10' y='50'>{text}</text>")
print("</svg>")
