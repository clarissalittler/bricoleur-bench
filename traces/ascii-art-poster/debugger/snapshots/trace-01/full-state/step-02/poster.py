import textwrap


def render(message: str, width: int) -> str:
    lines = textwrap.wrap(message, width=width) or [""]
    aligned = [line.center(width) for line in lines]
    for a in aligned:
        if len(a) != width:
            raise SystemExit(f"debug: bad width {len(a)} for {a!r}")

    top = "+" + "-" * (width + 2) + "+\n"
    body = "".join("| " + line + " |\n" for line in aligned)
    bot = "+" + "-" * (width + 2) + "+\n"
    return top + body + bot


print(render("one two three", 10), end="")
