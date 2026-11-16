# Full send: merge it unattended

Applies only when the user explicitly says "full send" (or plainly says to merge it without them). Otherwise stop at the gate in [SKILL.md](SKILL.md).

A full send means the user is not watching this thread. Your updates and final message go unread until long after you stop. You own the work all the way to a merged PR.

## What a full send adds

On top of what [SKILL.md](SKILL.md) authorizes, a full send grants permission to merge (or complete) the PR once the merge gate passes, using the repo's normal method.

It still does not cover production changes, data deletion, changes outside the repo, closing a PR, or force-pushing any branch but this task's. It does not bypass a harness or system approval prompt if one appears.

## Merging

- Merge with the method the repo uses: check the allowed methods and recently merged PRs. On Azure DevOps, complete the PR with the repo's merge type and its work-item and branch-deletion settings.
- If the repo uses a merge queue, auto-merge or auto-complete, stay until the platform reports the PR as merged.
- Merge through branch protection or branch policies as configured. Never use `--admin`, policy bypass, or any other override.
- Right before merging, fetch and check the PR again. Never merge when it is behind or conflicted, or when base commits that landed after the last green run touch this PR's files: rebase, push, and wait for green again.
- You may ignore an automated review that only asks for "human review" when your proof gives you high confidence.

## Report

In your final message: the PR link, the merge commit, your proof, and each decision you made for the user.

## When you can't continue

A question in a normal message goes unseen, and the thread looks done. Use the harness's question tool so the thread shows that it is waiting. If no question tool is available, or it returns no answer, take the safe path: leave the PR open and unmerged, and start your final message with the question.
