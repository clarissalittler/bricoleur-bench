# Problem List

This list tracks candidate programs to trace, along with their goals, personas covered, and current state. Use it to prioritize which traces need more depth or additional student types.

| Problem | Description | Personas Covered | Status | Next Actions |
| --- | --- | --- | --- | --- |
| Temperature Converter CLI | Build a Python script that converts between Celsius and Fahrenheit from the command line. | Bricoleur, Planner, Improviser | Draft traces added | Flesh out interim mistakes, add richer validation scenarios, and record sample runs. |
| Word Frequency Counter | Produce a script that reports word counts from a text file while ignoring punctuation and case. | Bricoleur, Planner, Skeptic | Initial traces added | Add fixtures for punctuation-heavy inputs and expand skeptic tests into reusable harness. |
| Todo List TUI | Implement a terminal todo manager with add/list/complete commands and simple persistence. | Planner, Improviser, Architect | Initial traces added | Refine persistence format, add undo/redo notes, and capture more error-handling branches. |
| Markdown Link Checker | Parse Markdown files and report broken or redirected links with optional caching. | (TBD) | Proposed | Define caching strategy, CLI flags, and which personas to trace first (Debugger? Optimizer?). |
| ASCII Art Poster | Render text as an ASCII “poster” with borders, alignment, and optional themes. | Bricoleur, Planner, Improviser, Debugger, Optimizer, Skeptic, Architect | Initial traces added | Add deeper missteps around wrapping/alignment; add trace-02 with theme/font experiments. |
| Interactive Fiction Engine | Run a branching text adventure from a JSON story file with choices and state. | Bricoleur, Planner, Improviser, Debugger, Optimizer, Skeptic, Architect | Initial traces added | Add traces covering corrupt JSON, missing node ids, and richer state (inventory/counters). |
| Conway’s Game of Life | Simulate cellular automata from a text pattern file; print frames as ASCII. | Bricoleur, Planner, Improviser, Debugger, Optimizer, Skeptic, Architect | Initial traces added | Add additional patterns (blinker/glider checks), and a trace-02 with viewport/wrap mode. |
| Haiku / Microfiction Generator | Generate short poems from a wordlist with a seed for determinism. | Bricoleur, Planner, Improviser, Debugger, Optimizer, Skeptic, Architect | Initial traces added | Add traces that address template drift, punctuation, and style customization while keeping determinism. |
| Maze Generator + Solver | Generate a maze with `--seed`, then solve it and print path length. | Bricoleur, Planner, Improviser, Debugger, Optimizer, Skeptic, Architect | Initial traces added | Add trace-02 with stronger maze validation, optional path overlay, and generator refinements. |
| SVG Logo Generator | Generate a simple SVG “logo” for a phrase with optional color/theme flags. | Bricoleur, Planner, Improviser, Debugger, Optimizer, Skeptic, Architect | Initial traces added | Add trace-02 exploring layout variations and text fitting; keep default output deterministic. |

## Adding a new problem
1. Create a subdirectory under `traces/` named after the problem (kebab-case recommended).
2. Add a `README.md` in that directory describing the goal, acceptance criteria, and any constraints.
3. Create one subdirectory per student type included in the traces (e.g., `bricoleur`, `planner`).
4. Place sequential trace files (e.g., `trace-01.md`, `trace-02.md`) in each student directory that narrate the editing journey.
5. Update this list with the personas covered, status of the traces, and the next actions for improving depth or coverage.
