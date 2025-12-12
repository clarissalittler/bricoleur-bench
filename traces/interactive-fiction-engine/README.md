# Interactive Fiction Engine

Goal: Build a Python CLI that runs a branching text adventure described by a JSON file.

This problem allows creativity in story content while keeping the engine testable with a fixed schema and a small example story.

## Requirements
- `python play.py story.json` loads a story file and starts at a known start node.
- Print the current scene text and numbered choices.
- Read a choice from stdin and move to the next node.
- Support simple state:
  - flags that can be set by visiting nodes
  - conditional choices (shown only when a flag is set)
- Handle invalid input (non-integer, out-of-range) with a reprompt or a clear error and non-zero exit.

## Story schema (minimal)
- `start`: string node id
- `nodes`: mapping from id -> node
- node fields:
  - `text`: string
  - `choices`: list of `{ "label": str, "to": str, "requires": [str]? }`
  - `sets`: [str]? (flags to set when entering node)
  - `end`: bool? (if true, game ends after printing text)

See `example-story.json` for a concrete instance.

## Acceptance criteria (using the example story)
- `python play.py example-story.json` prints the start node text and at least one choice.
- Selecting a valid choice advances to the correct next node.
- Selecting an invalid choice yields a clear message and does not crash.
- A node with `end: true` terminates the program with exit 0 after printing.

## Creative extensions (optional)
- Inventory, variables, counters.
- Save/load.
- Richer rendering (ASCII boxes), but keep a default plain mode for testing.

## Trace organization
Good traces here include lots of “input loop” tinkering and refactors from ad-hoc parsing to a clearer state machine.
