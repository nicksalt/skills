---
name: explain
description: "Explain how code works or why it is shaped that way. Use for 'how does X work', code walkthroughs before a change, placement and ownership questions ('where should this live'), or 'why is it like this', design rationale, regressions and postmortems."
---

# Explain

Two questions, two sources. Pick the mode from the question; run both when the user needs the shape and the reasons.

| Mode | Question | Source of truth |
|---|---|---|
| **How** | What does it do, where does it live, who owns it? | The code as it runs now |
| **Why** | Why was it built this way, why did it change? | The record: commits, PRs, ADRs, work items |

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

## How

Spawn one read-only subagent that explores and explains in one pass. Give it the user's question and this brief:

> You are writing an architectural explanation for a senior engineer. Explore the codebase and write an explanation that a senior engineer unfamiliar with this area could read and walk away with a solid mental model. They should understand the architecture well enough to start working in it confidently. Use the project's `GLOSSARY.md` terms where they exist. You have read-only access to the codebase.

Present the subagent's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Why

Answer from the record, not the code. Read the commits and PR discussions that introduced the target and each later change, the ADRs under `docs/decisions/` or `docs/adr/`, and the linked work items. Use other sources if the trail is thin.

Cite what the authors wrote. Mark your own inferences as inferences. Say what the record does not answer.
