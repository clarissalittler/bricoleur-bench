# Temperature Converter CLI

Goal: Build a Python command-line script that converts temperatures between Celsius and Fahrenheit.

## Requirements
- Accept an input value and scale flag (e.g., `--to-f` or `--to-c`).
- Validate user input and provide helpful error messages for missing or invalid arguments.
- Print the converted value to standard output with the unit suffix.
- Reject contradictory flags (e.g., both `--to-f` and `--to-c`) and non-finite values such as `nan` or `inf`.
- Provide examples in help output so a new user can run the script without reading the source.

## Acceptance criteria
- Running `python convert.py --to-f 0` prints `32.00F` and exits successfully.
- Running `python convert.py --to-c 212` prints `100.00C` and exits successfully.
- Passing no direction flag exits with a clear error and non-zero status.
- Passing an invalid number (e.g., `abc` or `nan`) exits with a clear error and non-zero status.

## Trace organization
- `bricoleur/` contains a meandering, experiment-heavy path to a working script with incremental tests and occasional backtracks.
- `planner/` contains a more methodical path with upfront notes, checklists, and checkpointed steps.

Each trace file narrates a sequential editing journey for the persona, showing intermediate code snapshots, mistakes, and corrections. Include short test commands and observations when the student probes the script.
