# Architect: sketch the shape before the code

Sketch types, function signatures, and module structure, with `not implemented` bodies and pseudocode, before any real code. Then implement against the sketch and stay alert for the moment the sketch is wrong.

Use this mode for non-trivial new work where jumping to code would lock in the wrong shape. Skip it for a change that fits an existing shape.

## 1. Ground

Build a real mental model of every system the new code touches. Naming a file isn't grounding. For each subsystem, write a short architectural explanation (the `explain` skill's How mode does this). If the design changes ownership or layering, also run `explain`'s Why mode on the existing shape, so the old rationale becomes a constraint, not a guess.

Read `GLOSSARY.md` and the ADRs in the area. Skip this step only for true greenfield work with nothing around it.

## 2. Sketch twice

Write the caller's usage first, then derive the types and signatures from it.

Produce at least two structurally distinct candidates before choosing, even when the first looks fine: whole-shape alternatives, not point fixes inside one shape. For anything bigger than one module, use [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) to get them from parallel sub-agents.

Screen every candidate against [RED-FLAGS.md](RED-FLAGS.md). Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repo.

Compare the survivors on depth (see [SKILL.md](SKILL.md)). Prefer the one that hides more behind a smaller interface.

Output: one file with the new types and signatures for a small change; a module map plus type definitions for larger work. Add a short rationale: the usage sketch, the candidates, and why the winner won.

## 3. Agree (only when asked)

By default, go straight to implementation. Stop and show the sketch first only when the user asks for a checkpoint ("show me before you build it").

The sketch can ship as its own commit (scaffold first). If the user pushes back on the shape, treat that as new grounding: go back to step 1 and re-sketch before writing more code.

## 4. Implement against the sketch

Replace `not implemented` bodies with code and pseudocode with logic. The sketch is the contract. A deviation is a signal to surface, not friction to absorb silently. If a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

## 5. Scrap when the shape is wrong

If implementation keeps producing friction the sketch can't absorb, throw the sketch out. Don't bolt fixes onto a wrong design. The signal is a pattern, not one instance:

- The same shape of workaround appears across unrelated code.
- Several unrelated edge cases all need special-case branches.
- Types need escape hatches (`any`, casts, optional fields that are always set) to compile.
- The "we need a lock" reflex appears when the sketch said the state wasn't shared.
- Callers must know the abstraction's internal rules to use it.

A few edge cases don't condemn a design. Complexity in the data is not complexity in the design.

When you scrap: trace what's built, redesign as if the new constraints were day-one assumptions, make the new sketch smaller than the old one before it grows, and return to step 2.
