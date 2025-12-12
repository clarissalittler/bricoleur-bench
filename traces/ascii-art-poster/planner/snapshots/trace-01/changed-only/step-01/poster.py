import textwrap


def wrap_message(message: str, width: int) -> list[str]:
    lines = textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False)
    return lines if lines else [""]


def align_line(line: str, width: int, align: str) -> str:
    if align == "left":
        return line.ljust(width)
    if align == "right":
        return line.rjust(width)
    if align == "center":
        return line.center(width)
    raise ValueError("align must be left|center|right")
