---
name: spec
description: "Turn the current conversation into a spec and publish it to the project's tracker as one ticket that owns the outcome. Split into more tickets only for independent outcomes, or when the user asks. Use for 'write this up', 'make a spec', 'file this as a ticket', or 'break this into tickets'."
---

# Spec

Synthesize what the conversation already settled into one ticket that owns the outcome. Do NOT interview the user; if something important is unsettled, say what and suggest the `grilling` skill.

Read `docs/agents/issue-tracker.md` for the tracker (GitHub, Azure DevOps, local files) and its conventions, and `docs/agents/triage-labels.md` for readiness labels. If they're missing, tell the user to run `/setup`.

## One outcome, one ticket

Small teams keep the board thin. The default is **one ticket per independently prioritizable outcome**, with the implementation steps, internal blocking order and verification checklist inside it. The implementing agent breaks the work down as it goes.

Split into several tickets only when parts have independent priority, ownership, delivery, material risk, or separately managed acceptance. A service boundary, a spec section, or "it won't fit in one context window" alone does not justify another ticket. If the user explicitly asks to break it into tickets, follow [TICKETS.md](TICKETS.md).

When the repo's tracker doc has its own rule for when to split, that rule wins.

## Process

1. **Explore** the repo if you haven't already. Use the `GLOSSARY.md` vocabulary throughout, and respect the ADRs in the area you're touching.
2. **Find the test seams.** Prefer existing seams; use the highest one possible. If new seams are needed, propose them as high as you can. The ideal number is one. Check with the user that the seams match their expectations.
3. **Write the spec** with the template below. Fold the work plan into **Implementation Plan** as an ordered checklist, marking which steps block others.
4. **Publish** it as one ticket on the configured tracker, with the `ready-for-agent` readiness label (or the tracker doc's equivalent). Link it to the parent the tracker doc names (an Epic, a milestone), and ask when none fits. Report its title, ID and link.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A numbered list of user stories that covers every aspect of the feature, each in the form:

1. As an <actor>, I want a <feature>, so that <benefit>

## Implementation Decisions

The decisions that were made:

- The modules that will be built or modified, and their interfaces
- Technical clarifications from the developer
- Architectural decisions, schema changes, API contracts
- Specific interactions

Do NOT include specific file paths or code snippets; they go stale quickly. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline the decision-rich part and note that it came from a prototype.

## Implementation Plan

- [ ] Step 1 (prefactor first: "make the change easy, then make the easy change")
- [ ] Step 2 — blocked by step 1
- [ ] ...

Each step is a vertical slice where it can be: a narrow but complete path through every layer that can be verified on its own.

## Testing and Evidence

- What makes a good test here (external behavior, not implementation details)
- Which modules will be tested, and the prior art to copy
- The evidence that will prove it to a reviewer: screenshots or recordings for anything a user can see (including schema changes that surface in the UI), command output otherwise

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Out of Scope

What this spec does not cover.

## Further Notes

Anything else.

</spec-template>
