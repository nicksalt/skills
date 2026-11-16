---
name: implement
description: "Take a ticket, spec, or agreed change to a proven, reviewed PR that is ready to merge, then stop. Use when the user asks to implement, build, or fix a ticket or spec, or says 'full stop'. Say 'full send' to also merge it unattended."
---

# Implement

Own the work from its current state to a PR that is ready to merge. By default, **stop at the merge gate** and hand it to the user (full stop). Merge only on an explicit "full send" (see [FULL-SEND.md](FULL-SEND.md)).

## Start

1. If the user passed a ticket reference, fetch it from the tracker in `docs/agents/issue-tracker.md` and state its title. If the reference is ambiguous, ask.
2. Inspect `git status` and keep unrelated changes intact. If you are on the default branch, create a branch.
3. **Size it.**
   - **One outcome that fits one session**: build it here (next section).
   - **A big chunk** (many steps that can run in parallel, or more than one context window of work): follow [BIG-WORK.md](BIG-WORK.md) to build on an integration branch with one implementer subagent per step, then come back for Prove onward.

## Steps

1. **Build** with the smallest change that meets the goal. Fix the case that happened, not every case that could. Call the Skill tool with `tdd` at the seams the spec agreed. Run the typecheck and single test files often, and the full suite once at the end.
2. **Prove it.** See Proof. If the repo has a `verify-*` skill for the service you touched, use it. When the change touches a shared contract (a schema, an API, a queue message, a shared type), run `blast-radius` too.
3. **Review.** Call the Skill tool with `code-review` on the branch. Fix the real findings; re-prove anything you change. Run `council` only if the user asked for it.
4. **File the PR** with the `pr` skill. Rebase onto the latest default branch first. Link the ticket the way the tracker doc says.
5. **Babysit** with the `babysit-pr` skill. Fix real findings and CI failures; prove each fix before you push it.
6. **Stop at the gate** (below), unless this is a full send.

Stay active from step 1 to the gate. If you end your turn while checks or bots are still running, the work stops, because nobody will prompt you again. Wait with the watcher from `babysit-pr`.

## What invoking this skill authorizes

Asking for `implement` (or saying "full stop") on a ticket or agreed change authorizes, for this task only: creating the branch, committing, pushing that branch (including `--force-with-lease` after a rebase), opening the PR, replying to review bots, and the test methods Proof needs, even where a repo file says to ask before computer use, browser automation, simulators, running the app, or screenshots. Rules about *how* to test (which command, fixture or environment) still apply.

It does not authorize merging, enabling auto-merge or auto-complete, pushing to the default branch, production changes, data deletion, billable runs beyond the repo's stated allowance, or force-pushing any other branch. Disable any existing auto-merge or auto-complete before you start, and check again before each push.

## Proof

Proof is evidence you observed yourself in this session. Use the most direct proof the change allows:

- Reproduce the original failure, apply the fix, then watch the same reproduction pass.
- Run the checks the repo's CI runs (typecheck, lint, tests).
- When the behavior has no test and the repo has a test setup, add one focused test that fails without the fix.
- **Anything a user can see gets visual proof:** UI changes, and changes that are not UI but alter what a user sees (a schema field that surfaces in a form, an API change that changes a screen). Run the app and capture before and after screenshots or a short recording, from fixtures or test data, never production data. Green mocked tests do not prove the user experience works.

If you cannot find a way to prove a change, you do not have full confidence. Ask the user.

## The merge gate

Ready means all of these are true on the latest commit:

- Your proof covers every change in the diff.
- Required checks or build policies are green.
- Review bots have finished, and each finding is fixed or dismissed with a written reason.
- No human review still requests changes.
- The branch is up to date with the default branch and the platform reports it mergeable.

Then fetch the target branch and check the live PR's head, base, checks, reviews and mergeability. Confirm it is open, not a draft, and not set to merge without the user. Report one verdict:

- **Ready to merge:** the gate passes. Leave the PR open and unmerged.
- **Waiting for required approval:** only human approval remains. Confirm that this is the actual blocker.
- **Blocked:** what prevents readiness, what you tried, and what is needed.

In T3 Code, call `unwatch_pull_request` before the handoff or a question. Report the PR link, the final head, the verdict, your proof, the review outcome, and the remaining risks. Say whether the PR is still open and unmerged.

## Asking the user

Ask only when you cannot continue alone: you cannot prove the change, the gate cannot pass and you cannot fix that, the next step is outside what this skill authorizes, the goal is ambiguous in a way that changes the result, or another PR makes this one obsolete. Use the harness's question tool (`AskUserQuestion` in Claude Code, `request_user_input` in Codex), with the PR link, the blocker, and the options with your recommendation first. Decide everything else yourself with sensible defaults, and list those decisions in the report.
