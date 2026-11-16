---
name: council
description: "Get review or feedback from several models on different providers, and loop until they agree. Use only when the user says 'council'."
disable-model-invocation: true
---

# Council

Before an audit, address outstanding PR comments, fix known issues, and run
relevant checks. Give council the updated implementation; do not defer known
fixes until reviews return. If the user wants to discard the implementation
and explore new ideas, skip fixes to code being replaced.

## Pick the members

Council members are never baked into this skill. If the user's request (or
their `CLAUDE.md` / `AGENTS.md`) names the members, use those. Otherwise, before
starting anything, ask the user with the harness's question tool:

- which models sit on the council (in T3 Code, call `orchestrator_capabilities`
  first and offer the models it lists, one per provider by default);
- the reasoning effort for each;
- how many rounds they'll pay for (default: one review round, plus one
  re-check round after fixes).

Tokens are limited, so keep briefs short: context pointers (the branch, the
diff, the spec, screenshots) instead of pasted files.

In T3 Code, use `delegate_task` to start one delegate per model in parallel.
Elsewhere, use the harness's subagent tools. If a chosen member is
unavailable, report it instead of substituting.

## UI reviews

For UI work, the council reviews what a user sees: give each delegate the
before and after screenshots or recording (see the `pr` skill's Evidence
rules) alongside the diff, and ask what a user would notice, not only what
the code does.

## Run it

Give each delegate the request and relevant context. For review or feedback,
keep their work read-only. Collect their responses and summarize the useful
findings, disagreements, and recommended next steps.

Do not wait idle. When a result arrives, check its findings against the code
at once and decide what to fix while the other delegates run. Do not edit
files while a delegate still reviews the same checkout. If the user's
instructions mark a delegate as non-blocking, do not wait for it; treat a
late result as feedback and do not record its score.

For a code review, ask each delegate for a score out of 10.
Count each full review pass as one round.
A fresh review after fixes starts a new round.

If the work ends in a pull request, put the results in the PR description.
Put this section before the model and harness line at the end:

```markdown
## Council review

Rounds: 2

| Delegate | Round 1 | Round 2 |
| --- | --- | --- |
| Claude Opus | 7/10 | 9/10 |
| GPT Sol | 8/10 | 10/10 |
| Gemini Pro | 7/10 | 9/10 |
```

If a delegate gives no score, write `no score`. Do not invent one.
If the PR is open, edit the description. Do not post a comment for this.
If there is no PR, put the same results in the final reply only.

If you agree with their recommendations, make the changes and request a fresh
review after, within the rounds the user agreed to. Stop when all delegates are
satisfied or the rounds run out, and say which.

Do not let repeated reviews result in scope creep. It is your job to fight to
keep scope limited.
