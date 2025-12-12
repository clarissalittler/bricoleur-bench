import sys

text = " ".join(sys.argv[1:]) or "Hello"
print(f'<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120">')
print(f'  <rect width="100%" height="100%" fill="black"/>')
print(f'  <text x="20" y="70" fill="white" font-size="32">{text}</text>')
print("</svg>")
