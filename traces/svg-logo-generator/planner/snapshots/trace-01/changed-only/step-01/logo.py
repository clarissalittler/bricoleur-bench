from html import escape


def render(text: str, width: int, height: int, bg: str, fg: str) -> str:
    t = escape(text)
    y = height // 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="100%" height="100%" fill="{bg}"/>'
        f'<text x="20" y="{y}" fill="{fg}" font-size="32">{t}</text>'
        f"</svg>\n"
    )
