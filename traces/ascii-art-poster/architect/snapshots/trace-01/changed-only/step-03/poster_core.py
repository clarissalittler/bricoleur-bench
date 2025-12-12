import textwrap


def wrap_message(message: str, width: int) -> list[str]:
    return textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    if align == "center":
        return line.center(width)
    raise ValueError("align must be left|center|right")


def render(message: str, width: int, align: str, border: str, *, padding: int = 1) -> str:
    lines = [align_line(line, width, align) for line in wrap_message(message, width)]
    if border == "none":
        return "\n".join(lines) + "\n"
    if border != "ascii":
        raise ValueError("border must be ascii|none")

    border_width = width + (2 * padding) + 2
    top = "+" + "-" * border_width + "+\n"
    body = "".join("| " + (" " * padding) + line + (" " * padding) + " |\n" for line in lines)
    bot = "+" + "-" * border_width + "+\n"
    return top + body + bot
