---
name: workhorse
description: Delegate implementation to economical models while the lead plans and validates. Use alongside implement or another implementation workflow, only when the user invokes it.
disable-model-invocation: true
---

Act as the lead developer with a limited token budget. Delegate implementation and substantial investigation to economical workers; retain decisions, focused inspection, and acceptance.

This is a companion to the active implementation workflow. That workflow owns scope, ticket sequencing, testing policy, integration, final review, commits, and delivery. Apply the delegation rules below within it; reuse its checks and review stages.

1. **Select.** The user chooses the workhorse. Recover any choice already established in the conversation, then verify the provider, model, and requested options against the live catalog. If the choice is missing, ambiguous, or unavailable, ask the user before launching any workers. Offer available options when helpful; wait for their answer. Honor effort and budget choices. Briefly name the worker and reviewer. Keep the current lead model. Use one implementer at a time by default; increase concurrency for independent work when requested, with separate write ownership.

   **Nick's provider preference:** When Nick requests Gemini, use Antigravity only unless he explicitly chooses another provider. Preserve the requested model and effort; if unavailable through Antigravity, ask before substituting.

2. **Brief.** Turn the next ready piece of work into a bounded assignment. Keep related behavior together; split when a dependency, ownership boundary, or independently verifiable outcome warrants it. Resolve architectural choices before handing off mechanical edits. Give each worker:
   - **Workspace:** absolute checkout path, branch/base, existing WIP, and permitted files or components.
   - **Outcome:** exact behavior and acceptance criteria for this slice, with the relevant decisions and constraints.
   - **Approach:** the simplest complete change that makes correct behavior obvious. Look for an existing implementation to reuse or extend. Keep edits scoped; add abstractions, dependencies, configuration, or execution paths only for a concrete requirement. Preserve required behavior and failure handling. Include the repository's relevant simplicity guidance.
   - **Pointers:** spec/ticket sections, known code seams, prior commits or findings, and existing check commands. Include essential facts inline when the worker cannot access a pointer; keep unrelated history out.
   - **Authority:** allowed mutations and inherited permissions, budgets, and stop conditions. Keep further delegation with the lead.
   - **Return:** completed changes, actual commands/results, remaining criteria or blockers, artifact paths, and branch/commit/worktree state. The worker finishes the slice or reports a concrete blocker. Shell commands finish before its final reply; an asynchronous delegated task may run in the background.

3. **Validate.** Read the terminal result, inspect the actual diff, and check the relevant output against the assigned criteria before accepting the slice. Apply the brief's simplicity standard: check for duplicated implementations, unnecessary indirection, speculative generality, and unrelated edits. When a simpler existing path satisfies the criteria, send that alternative back to the worker for simplification and revalidate it. Investigate unexpected changes and missing evidence. Check the claimed boundary: a mocked entry point cannot establish end-to-end behavior. Run focused checks when evidence is missing or changes warrant them; reuse valid results. Send concrete gaps back to the worker with the failing scenario and expected result. Keep bulk fixes with workers.

4. **Review.** Use the active workflow's final review on the integrated result, without adding a full review for every ticket. Use the requested reviewer; otherwise select a fresh capable reviewer at moderate effort. Send actionable findings to an economical worker, validate the fixes, then obtain a fresh review of the changed result carrying prior findings and unresolved objections. Repeated failures require a sharper brief, smaller slice, or more capable worker. Honor any requested review/budget limit; report remaining blockers when it is reached.

On a stall or quota failure, inspect task state, processes, and saved work before retrying. Preserve partial work and establish that the previous writer has stopped before replacing it. Ask the user to choose any replacement model unless they already authorized a specific fallback. Report a delegation capability gap and ask how to proceed before taking over bulk implementation.

In T3, discover models/options with `orchestrator_capabilities` and use `delegate_task` for cross-provider, model-option, or isolated-worktree tasks. Follow the runtime's orchestration instructions; retain task IDs and distinct request IDs for new rounds. Worktree isolation starts from committed state, so account for uncommitted dependencies before dispatch. Outside T3, use the host's supported delegation mechanism and verify its model/workspace controls.
