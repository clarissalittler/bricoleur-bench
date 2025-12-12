import argparse


def render(message: str, width: int) -> str:
    inside = message[:width].ljust(width)
    top = "+" + "-" * (width + 2) + "+\n"
    return top + "| " + inside + " |\n" + top


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("--width", type=int, default=20)
    args = parser.parse_args()

    if args.width < 1:
        raise SystemExit(1)

    print(render(args.message, args.width), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
