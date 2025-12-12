import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width) or [""]
    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line.ljust(width) + " |\n" for line in lines)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot
