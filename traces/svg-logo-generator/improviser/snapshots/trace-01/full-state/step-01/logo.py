import sys

text = " ".join(sys.argv[1:]) or "Hello"
print('<svg xmlns="http://www.w3.org/2000/svg" width="320" height="120">')
print('  <rect x="0" y="0" width="320" height="120" rx="16" fill="#222"/>')
print(f'  <text x="24" y="74" fill="#fefefe" font-size="36">{text}</text>')
print("</svg>")
