import sys
from html import escape

text = escape(" ".join(sys.argv[1:]) or "Hello")
print('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="120">')
print('  <rect width="100%" height="100%" fill="#111111"/>')
print(f'  <text x="20" y="60" fill="#ffffff" font-size="32">{text}</text>')
print("</svg>")
