---
name: handoff
description: "Hand work between sessions. Write mode compacts this conversation into a handoff document for another agent. Resume mode picks up a previous T3 thread or a handoff document and continues its unfinished work here. Use for 'handoff', 'write a handoff', 'resume', 'continue from thread X', or 'pick up where that left off'."
argument-hint: "Write: what the next session is for. Resume: a T3 thread ID/link or a handoff doc path."
disable-model-invocation: true
---

# Handoff

Pick the mode from the request: a thread ID, link or handoff doc path means **Resume**; otherwise **Write**.

## Write

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS (`$TMPDIR`, else `/tmp`; `%TEMP%` on Windows) - not the current workspace.

Include a "suggested skills" section in the document, naming which skills the next agent should call the Skill tool for.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Resume

Continue here from the supplied T3 thread ID or link. Any accompanying message steers the continuation. Keep this conversation's selected model and account.

The source thread is read-only. Never send to, steer, resume, fork, or start a run in it: it may run on another subscription and would re-cache its whole history at full cost. All work, including child tasks, happens from this conversation.

1. Use `t3_thread_read` to recover the original task, latest user instructions, decisions, and stopping point. Paginate with `afterPosition: nextPosition`; recover relevant truncated text with `itemId` and `textOffset: nextTextOffset`. Follow artifact pointers and relevant predecessor/child results rather than dumping entire histories. If T3 access is unavailable, report the missing access.
2. Identify completed, partial, and remaining work. Check whether the final user instructions were acted on before the interruption. Preserve the original working method, including child models/options, roles, concurrency limits, and review checkpoints. For discussion, recover the questions that the user's new answers refer to.
3. Verify the source checkout, branch, WIP, and relevant artifacts against current state. Preserve existing changes. Check for active coordinators, children, or processes before editing; an imported child's `idle` label alone does not prove it stopped. Resolve workspace or ownership conflicts before overlapping work.
4. Briefly state where work stopped and the next action, then continue the authorized work here. Carry forward existing permissions, budgets, and stop conditions; ask only for information or authorization that cannot be recovered.

Use the existing thread and artifacts as context. Do not create a new thread or write a new handoff document.

For a handoff document instead of a thread: read it, follow its pointers, verify its claims against the current checkout (a handoff is context, not proof), then do steps 2 to 4 above. Call the Skill tool for the skills its "suggested skills" section names.
