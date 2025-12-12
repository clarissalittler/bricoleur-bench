import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width) or [""]
    lines = [line.center(width) for line in lines]
    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line + " |\n" for line in lines)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot


print(render("one two three", 10), end="")
