---
name: verification
description: "Create or maintain a project-local verify-<app> skill that drives the real app the way a user does and keeps the evidence: launch, doctor, drive, evidence, cleanup, and a feature map. Use for 'make a verify skill for this repo', 'how do we prove this works', when a project has no scripted way to prove UI/CLI/service behavior, or 'audit/maintain the verify skill'."
---

# Verification

Two modes. **Create** (this file) generates a `verify-<app>` skill for a repo. **Maintain** ([MAINTAIN.md](MAINTAIN.md)) is the periodic pass that keeps an existing one honest as the app changes. Pick from the request; when a verify skill already exists, the answer is almost always Maintain.

## Create

Every serious project needs a scripted way to drive the real app and prove behavior: launch it, exercise a feature the way a user would, and capture evidence. This generates that as a project-local skill at `.agents/skills/verify-<app>/` (symlink it into `.claude/skills/` so Claude Code finds it too), tailored to the repo. You write the generator's output for the next agent, not for a human: it will be read cold, mid-task, by an agent that has never seen the app.

### 1. Interview the repo, not the user

Answer these from the codebase and only ask the user what you cannot observe:

- **Surface:** what does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have several; pick the primary one and note the rest.
- **Run:** how does the app start locally? Prefer the repo's own documented dev command (package scripts, Makefile, README quickstart). Note ports, env vars, seed data, auth.
- **Drive:** how can an agent interact with it programmatically? Existing harnesses first — Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port. Only then pick a generic recipe: browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services.
- **Observe:** what evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles)? If not, say so in the generated skill: refusing to double-drive a shared instance beats corrupting the user's session.

If the checkout doesn't build or start as-is, fix that first (or report it precisely) before generating; a skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup (a static dir the API never serves, a sample config), the generated skill may create it, clearly marked as verification scaffolding, and remove it in cleanup.

### 2. Generate the skill

Write `.agents/skills/verify-<app>/SKILL.md` with YAML frontmatter (`name: verify-<app>` and a `description` that names the app, the surface, and when to reach for it — without frontmatter the skill never registers) and these sections, each grounded in what the interview actually found (no placeholders left):

- **Launch:** the exact command that starts the app for verification, and how to tell it's ready (a log line, a prompt). Launch must reach a usable state from an empty data dir, including any migrations and seed data. Ready means usable, not just that a process answers. A database health check can pass while its init scripts are still running. Include teardown. For a short-lived CLI or TUI there is no server to keep alive: launch means build the binary (or install deps) once, then start each drive in its own isolated PTY or tmux session.
- **Doctor:** one read-only check that answers "is this instance worth driving?" — process up, right version/build, port owned by us, auth valid. An agent runs this first whenever anything looks off.
- **Drive:** the harness recipe with real selectors/commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) over coordinates and tab order.
- **Evidence:** what to capture for a proof and where it goes. State the proof standards: exercise the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent) alongside what's visible; mocks only where a production boundary already isolates the external system. When the safe path is a dry-run or test mode, verify what it actually skips by observing (files, network, git refs) rather than trusting its name: some dry-runs still touch the network or open a browser.
- **Cleanup:** how to tear down instances the run created. Never kill by process name; kill what you started. Cleanup removes instances and scratch state, never the evidence: proof artifacts survive the teardown, in a location the skill names.
- **Helpers:** any script the skill ships is executable and its invocation is shown in the skill body. A helper the reader has to reverse-engineer is not a helper.

### 3. Seed the feature map

Create `.agents/skills/verify-<app>/features/README.md` plus one file per user-facing feature you can identify (aim for the top 3-5 to start, from routes, commands, menus, or docs). Follow the shape in [`references/feature-map-example/`](references/feature-map-example/), with a README index and one file per feature. Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. If the seed data lacks a precondition that a journey needs, the journey reports a failure and the reason goes in that feature's `Gotchas`. Never weaken the journey to make it pass. The map is the repo's maintained verification source; a proof that drives one convenient entry point is incomplete when the map lists others.

### 4. Prove the generated skill before handing it over

Run its own instructions end to end once: launch, doctor, drive ONE mapped feature (one is enough; the map exists so later runs can cover the rest), capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location — a cleanup that eats the proof fails this step. Fix what fails, and run the generated cleanup after every failed iteration too, so broken attempts don't strand processes and ports. A generated skill that was never executed is a draft, not a deliverable. If you proved it in a stand-in for the real target (a container in place of a fresh VM, a local stack in place of a remote one), list every setup step the stand-in did that the target will not. Those steps stay unverified until a run on the real target covers them.

### 5. Offer the maintenance loop

Point the user at this skill's Maintain mode for keeping the map honest as the app changes. Suggest a cadence only if they ask.

## What a good verify skill has (lessons from real ones)

Build these into every generated skill. They are what made the difference between a skill agents trust and one they route around.

- **Smallest real route first.** The skill tells the agent to map the changed contract and its consumers to feature files, run only those, and broaden to `all` only for shared state or contracts, a new failure, or a whole-service claim. Doctor and the map check inventory; they don't force every feature to run for every fix.
- **One driver owns the ceremony.** A single helper script owns doctor, isolation, coverage, evidence and cleanup, so the agent runs one command per feature instead of re-deriving the steps. Feature files hold the exact test selections; the driver reads them rather than keeping a second list.
- **Offline by default, and say what was replaced.** Replays run the real entry point with only external boundaries (model replies, storage, queues, email, telemetry) supplied, and every proof lists its substitutions. The driver disables env-file loading and blocks accidental network calls. An offline `passed` is never production acceptance.
- **Live mode is separate and gated.** A live check (real model spend, real cloud writes, real third-party portals) has its own command, starts with a read-only preflight, and needs explicit flags. Flags record the intended mode; they do not replace the user's authorization. Writes go only to run-owned resources with unique names, are read back independently, and are deleted and checked absent.
- **Blocked is a result.** Missing credentials or an unreachable source produce a retained `blocked` result with the reason. Never substitute another source or fixed inputs for a requested live check.
- **A manifest per run.** Each run writes to a fresh evidence directory (refuse existing ones) with a manifest: revision, dirty state, exact command, test arguments, counts, per-feature coverage, source hashes, blocked attempts, and cleanup status. Require named scenarios, including failure and retry paths, in a coverage file.
- **Visual evidence for anything a user sees.** For UI, and for non-UI changes that alter what a user sees (a schema field that surfaces in a form), the skill captures before and after screenshots or a short recording from fixtures or test data, never production data, and names where they're saved so the `pr` skill can attach them.
- **Human review is still a step.** Exit 0 means it ran. For generated or judgment-heavy output, the skill says what a person must read before accepting it, and records unobserved paths (deployed workers, delivered notifications) as unverified.
