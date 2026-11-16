---
name: takeover
description: "Take over someone else's PR, branch, or agent thread and finish it while keeping their credit, or bring an old PR up to date with its base (rebase, or modernize). Use when the user asks to take over, continue, rebase, or modernize a PR."
---

# Takeover

If the user only asked to rebase or modernize a PR, follow [MODERNIZE.md](MODERNIZE.md) and stop there.

Take responsibility for finishing the original goal while preserving the
original contributors' credit. Do not defend an implementation just because
another agent already built it.

Read the source PR, branch, or thread, including review findings and the user's
later corrections. Resolve the handoff to the actual code and current head,
and account for uncommitted work. Treat the handoff as context, not proof.

For a replacement PR, import the original commits onto a new branch and add
your fixes separately. Honor an explicitly requested in-place or stacked
continuation instead. Do not overwrite unrelated work or change the original
PR without authorization.

Preserve Git authorship and existing co-author trailers. Credit the original
contributors in the PR description and link the original PR when there is one.
If the work will be squashed, preserve human author/co-author credit in the
merge commit too, using verified identities rather than guessed emails. Model
attribution is not a substitute for contributor credit.

Follow [MODERNIZE.md](MODERNIZE.md) to update the continuation against its intended base and
current architecture. Rework what is necessary to finish the same goal, not
unrelated features. Simplify the implementation without dropping intended
behavior or surfaces. Recheck the source PR too: it may have improved while
you were working.

Independently verify the original failure and realistic workflows, following
repository guidance and permissions. Green mocked tests do not prove the user
experience works. State what remains unverified.

When the requested finish includes a PR, use the `pr` skill to file or update it,
then `babysit-pr` rather than stopping at creation. Format replies per the `pr`
skill's [COMMENTS.md](../pr/COMMENTS.md). Merge or close the original PR only when authorized.

Report what you inherited, what you changed, how you verified it, how credit
was preserved, and any remaining decision.
