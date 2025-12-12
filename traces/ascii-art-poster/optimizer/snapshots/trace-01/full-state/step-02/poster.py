import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width, break_long_words=True, break_on_hyphens=False) or [""]

    top = "+" + "-" * (width + 2) + "+\n"
    bot = top

    out: list[str] = [top]
    for line in lines:
        out.append("| " + line.ljust(width) + " |\n")
    out.append(bot)
    return "".join(out)
