# Student Types

This benchmark models several learner personas to capture different ways of tinkering and planning while solving programming problems. Each persona has expectations for how their trace should evolve, including characteristic mistakes, checkpoints, and testing habits.

## Personas

### Bricoleur
- **Style:** Experiments in small increments and keeps code running, even if messy; treats the REPL or script runs as a safety net.
- **Trace expectations:** Frequent small edits, opportunistic refactors, and quick tests to check intuition; intermittent comments showing hunches and course corrections.
- **Typical mistakes:** Copy/paste formulas, missing edge-case validation, temporarily duplicated logic; may forget to remove debug prints.
- **Signals of progress:** Gradual tightening of input handling, clearer outputs, and ad-hoc cleanup once a path works.

### Improviser
- **Style:** Mixes quick hacks with occasional planning; toggles between exploring and tidying depending on friction.
- **Trace expectations:** Alternates between exploratory edits and short design notes, sometimes reverting ideas mid-trace; might park TODOs inline while shifting to a new idea.
- **Typical mistakes:** Half-migrated refactors, inconsistent naming, or abandoned helper functions; drifts between CLI and interactive flows.
- **Signals of progress:** Consolidates helpers and removes dead code once a direction stabilizes; adds light comments about why a choice was made.

### Planner
- **Style:** Starts with an outline or checklist before coding and works methodically through it; prefers clear contracts and typed inputs.
- **Trace expectations:** Early notes outlining steps, followed by disciplined commits implementing each step; checkpoints that close TODOs with evidence of verification.
- **Typical mistakes:** Over-abstracting too early or forgetting to update the plan after a change; may over-format output before correctness is verified.
- **Signals of progress:** Plan items get checked off with short validation notes; functions gain docstrings or type hints as the solution stabilizes.

### Debugger
- **Style:** Focused on diagnosing failures; writes small probes and logging to isolate issues before changing core logic.
- **Trace expectations:** Early reproduction steps, instrumentation, and systematic narrowing of the bug surface; uses assertions or logging to confirm hypotheses.
- **Typical mistakes:** Leaving noisy logging enabled, narrowing too aggressively and missing alternative causes; may forget to clean up probes.
- **Signals of progress:** Logs become more precise, failing cases turn green, and cleanup removes temporary probes.

### Optimizer
- **Style:** Begins with a working baseline and then iterates on performance or ergonomics, often with rough measurements.
- **Trace expectations:** Baseline implementation, benchmarks or rough timing notes, and iterative improvements with comparisons; may toggle data structures during exploration.
- **Typical mistakes:** Premature micro-optimizations that obscure readability; relying on noisy benchmarks without repetition.
- **Signals of progress:** Stabilized benchmark numbers, clearer API boundaries, and commentary on trade-offs between speed and clarity.

### Skeptic
- **Style:** Leads with tests and probes to invalidate assumptions before writing or rewriting code.
- **Trace expectations:** Starts with failing cases, logs observations from instrumentation, and records how error messages evolve; keeps a tight loop of hypothesis -> probe -> adjustment.
- **Typical mistakes:** Overfitting to the latest failing case, leaving verbose logging enabled, or stalling while waiting for "perfect" evidence.
- **Signals of progress:** Shrinking set of failing cases, clearer exit codes, and trimmed diagnostics once confidence rises.

### Architect
- **Style:** Front-loads design, interfaces, and invariants before implementation; prefers separating concerns early.
- **Trace expectations:** Early sketches of modules and contracts, followed by deliberate implementation aligned to the design; notes on trade-offs and future-proofing.
- **Typical mistakes:** Spending too long on abstractions, overgeneralizing storage formats, or delaying testing until structure feels "clean".
- **Signals of progress:** Stable interfaces with small iterative refinements, validation steps that prove invariants hold, and documentation that matches the implemented shape.

## How to use these personas
- Every problem directory should include subdirectories named after the personas used in that problem's traces (e.g., `bricoleur`, `planner`).
- Each trace file should narrate a coherent sequence of edits for that persona, including mistakes, partial implementations, and course corrections on the way to the goal. Include short notes on what the student expected versus observed.
- When adding a new persona, append it to this file with notes about its characteristic editing style and the kinds of checkpoints or missteps a trace should surface.
- If a persona shows both code and narration, prefer short, time-stamped snippets (Step N) to keep the evolution legible while preserving the in-the-moment perspective.
