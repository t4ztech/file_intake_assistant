# File Intake Assistant — Downloadable Plan

## Goal

Turn File Intake Assistant from a development-stage project into a simple downloadable tool that can be tested like a normal user product.

The goal is not to rush into packaging too early.

The goal is to move step by step toward a version that feels simple, safe, and understandable outside the development environment.

---

## Current state

The project already has:

- working CLI preview flow
- safety-first rename and move preview logic
- README
- changelog
- roadmap
- GUI v0.1 prototype
- GUI findings
- example screenshots
- real mixed-folder testing

This is already a strong base.

---

## Main problem before download testing

The main issue is not the core logic.

The main issue is user experience around preview and environment behavior.

In particular:

- WSL introduces extra friction
- Linux-style folder selection is not ideal for normal Windows users
- external preview opening behavior is unreliable in the current environment
- the downloadable version should feel like a normal Windows tool, not a development setup

---

## Recommended path

### Phase 1 — Stable local prototype
Keep improving the existing local version until the main preview flow feels clean and predictable.

Focus:

- folder input
- preview generation
- summary visibility
- preview details inside the GUI
- simple and functional layout

### Phase 2 — Small GUI polish
Make the GUI more usable without turning it into a bloated interface.

Focus:

- slightly cleaner spacing
- simple labels
- better readability
- keep the interface primitive in a good way
- avoid unnecessary UX decoration

### Phase 3 — Windows-side execution
Move from WSL-centered testing toward normal Windows-side use.

Goal:

- run the GUI through Windows Python
- reduce WSL-specific path and shell issues
- make testing closer to real user conditions

This is the key bridge toward a real downloadable version.

### Phase 4 — First downloadable test format
Create the simplest practical downloadable form.

This may be:

- a zip package
- a small launcher
- a Windows Python-based runnable version
- later, possibly an `.exe`

The first downloadable version does not need to be perfect.

It needs to be testable.

### Phase 5 — Self-download test
Download the project from GitHub like a normal user and test it from scratch.

This should answer questions like:

- Is the repo easy to understand?
- Is the README good enough?
- Is the entry point obvious?
- Is setup too technical?
- What feels unclear when approaching it fresh?

This is a critical test step before showing it more widely.

### Phase 6 — Small external testing
After self-download testing, try a small round of feedback from a few real users.

Only after that should the tool be pushed harder for wider visibility.

### Phase 7 — Reddit presentation
Once the tool is stable enough to test without confusion, prepare a simple Reddit presentation.

The post should focus on:

- the problem
- the safety-first angle
- the preview workflow
- the simple GUI
- before / preview examples
- what kind of feedback is wanted

---

## Product principle

The tool should not feel flashy.

It should feel:

- simple
- safe
- direct
- useful
- non-threatening

Primitive is fine.

Confusing is not.

---

## Key reminder

Do not build throwaway work.

Each step should stay useful for the real product whenever possible.

---

## Immediate next steps

1. Clean up the repo
2. Improve GUI preview experience
3. Do small GUI polish
4. Prepare for Windows-side execution
5. Download and test from GitHub like a real user