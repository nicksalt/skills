---
name: ask-nick
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask Nick

You don't remember every skill, so ask. Before stating what a skill does or recommending a step be skipped, read that skill's SKILL.md: the summaries here are for orientation only.

A **flow** is a path through the skills. Most work travels the **main flow**; the side flows join it. Everything else is a standalone tool, or a vocabulary layer underneath.

## The main flow: idea → ready-to-merge PR

1. **`/grilling`** sharpens the idea by interview, a round of numbered questions at a time. In a repo it also runs **`domain-modeling`**, so settled terms land in `GLOSSARY.md` and hard decisions become ADRs.
   - A question that needs a runnable answer (a state model, business logic, a UI you have to see)? Detour through **`/prototype`**, with **`/handoff`** out and back if it lives in another directory.
   - Not sure the task is deep enough? **`/sharpen`** rewrites the prompt first.
2. **`spec`** writes the settled conversation up as **one ticket** that owns the outcome, with the implementation plan inside it. It splits into several tickets only for independent outcomes, or when you ask.
3. **`implement`** takes the ticket to a PR that is **ready to merge, then stops** (full stop). On the way it builds with **`tdd`**, proves the change (visual evidence for anything a user sees, via the repo's **`verify-*`** skill when there is one), reviews with **`code-review`**, files with **`pr`**, and watches CI and bots with **`babysit-pr`**. A big chunk fans out on an integration branch, one subagent per step. Say **"full send"** to have it merge too.
4. **`/retro`** closes the loop after a build, especially one that went sideways: it turns mistakes into checks, standards and steering files. For a mistake agents keep repeating, **`/correct`** makes it impossible (architecture, types, lint) instead of writing another rule.

Keep steps 1 and 2 in one context window so the spec builds on the grilling. `implement` can start fresh from the ticket. See [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for when to continue, clear, compact, hand off, or use a subagent.

## Side flows

- **Something is broken:** **`diagnose`** (reproduce, minimise, hypothesise, instrument, fix, regression test), then `implement`'s Prove onward, or `spec` to file it if it's not for now.
- **Incoming issues or PRs:** **`/triage`** moves them through the triage states and writes agent-ready briefs that `implement` can pick up.
- **Work too big for one session to plan:** **`/wayfinder`** maps it as decision tickets and resolves them one at a time. For an ambitious change someone reviews after stepping away, **`/figure-it-out`** designs its own auditable playbook.
- **Someone else's PR or thread:** **`takeover`** finishes it and keeps their credit. Just rebasing an old PR? Same skill, modernize mode.
- **Picking work back up:** **`/handoff`** writes a handoff doc, or resumes from a T3 thread or a handoff doc.
- **A second opinion from other models:** **`/council`** (asks you which models and how many rounds). Best for UI work, with screenshots.

## Before you build

- **`codebase-design`**: the deep-module vocabulary, plus Architect mode (sketch types and signatures before code) and Scan mode (find deepening opportunities across the codebase).
- **`explain`**: How mode (what the code does now) and Why mode (what the record says about why).
- **`blast-radius`**: what a change breaks somewhere else, proven by running code.
- **`/research`**: primary-source research into a Markdown file. **`/teach`** when you want to learn the concept yourself.

## Proof

- **`verification`**: create a repo's `verify-<app>` skill, or maintain one as the app changes. `implement` uses whichever `verify-*` skill the repo has.

## Communication and meta

- **`/wait-what`**: that last message didn't land, so re-pitch it.
- **`/to-questionnaire`**: a decision you can't answer alone becomes a questionnaire for someone else.
- **`/unslop`**: cut AI tells from a piece of writing (manual only).
- **`writing-for-agents`**: the style guide for editing skills, `AGENTS.md` and `CLAUDE.md`.
- **`/workhorse`**: hand implementation to economical models while the lead plans and checks (manual only).
- **`/setup`**: run once per repo. It records the tracker (GitHub, Azure DevOps, GitLab, local), triage labels, PR rules and domain-doc layout under `docs/agents/`, which most skills above read.

## Trials

Skills in the repo's `trial/` folder are on probation: `ketchup`, `automate-me`, `benchmark-checklist`, `no-comments`. Suggest one only when it clearly fits, and say it's a trial.

The visual version of this map is `docs/flows.md` in the skills repo.
