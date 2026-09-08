# Logic Prototype

An executable experiment for **business logic, state transitions, or data shape**. Use focused probes, assertions, or tests when concrete examples answer the question; use a tiny interactive terminal app when the user needs to explore the model by hand. The TUI steps below apply only to that interactive shape.

## When this is the right shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where the user wants to **press buttons and watch state change**.

If the question is "what should this look like" — wrong branch. Use [UI.md](UI.md).

## Process

### 1. State the question

Before writing code, write down what state model and what question you're prototyping. One paragraph, in the prototype's README or a comment at the top of the file.

### 2. Pick the language

Use whatever the host project uses. If the project has no obvious runtime (e.g. a docs repo), ask.

Match the project's existing conventions for tooling — don't add a new package manager or runtime just for the prototype.

### 3. Choose the smallest logic surface

Use an existing callable seam when it answers the question. A probe against an existing API or state function needs no new module. When the experiment requires new logic, isolate it behind a small inspectable interface where that separation helps evaluation or later reuse. New logic and any TUI remain prototype code until explicit implementation authorization promotes the validated result under the repository workflow.

When new logic is needed, its shape depends on the question:

- **A pure reducer** — `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine** — explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state — just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick whichever shape best fits the question being asked, not whichever is easiest to wire to a TUI. Prefer pure logic when I/O is not part of the question; keep presentation separate where useful rather than refactoring existing code merely to satisfy a prototype shape.

### 4. Exercise the model

For concrete-case probes, provide executable inputs, expected results, and visible actual state or assertion failures. Run them and record what they demonstrate, including limitations. No TUI is required when those results answer the question.

For interactive exploration, build it as a **lightweight TUI** — on every tick, clear the screen (`console.clear()` / `print("\033[2J\033[H")` / equivalent) and re-render the whole frame.

Each frame has two parts, in this order:

1. **Current state**, pretty-printed and diff-friendly (one field per line, or formatted JSON). Use **bold** for field names or section headers and **dim** for less important context (timestamps, IDs, derived values). Native ANSI escape codes are fine — `\x1b[1m` bold, `\x1b[2m` dim, `\x1b[0m` reset. No need to pull in a styling library unless one is already in the project.
2. **Keyboard shortcuts**, listed at the bottom: `[a] add user  [d] delete user  [t] tick clock  [q] quit`. Bold the key, dim the description, or vice-versa — whatever reads cleanly.

Behaviour:

1. **Initialise state** — a single in-memory object/struct. Render the first frame on start.
2. **Read one keystroke (or one line)** at a time, dispatch to a handler that mutates state.
3. **Re-render** the full frame after every action — don't append, replace.
4. **Loop until quit.**

The whole frame should fit on one screen.

### 5. Make it runnable in one command

Reuse an existing test or execution command when it runs the probe. Add a task-runner entry only when it makes a new experiment easier to run; no new runner or script is required for an existing command. Put the exact command in the handoff or prototype notes.

### 6. Hand it over

Give the user the run command and any observed probe results. For a TUI, they can drive the model themselves; surprising transitions expose bugs in the idea. Add requested cases or actions within the experiment's scope.

### 7. Capture the answer and the prototype

Once the prototype has answered its question, capture the answer and prototype as [SKILL.md](SKILL.md) describes. Record which reducer, machine, or function set may inform later production work. Prototype selection alone does not authorize production changes. Explicitly authorized implementation may reuse the validated code and add the production checks or hardening it needs; no rewrite or new Ticket is required solely because of its prototype origin.
