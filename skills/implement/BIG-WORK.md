# Big work: build on an integration branch

Use this when the work is too big for one session. The spec may have separate tickets, or (the usual case) one ticket whose **Implementation Plan** lists the steps and which ones block others. Treat each step or ticket as a unit of work.

The tracker is configured in `docs/agents/issue-tracker.md`. If it's missing, tell the user to run `/setup`.

The goal is the entire spec implemented on a single **integration branch**.

The units are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of units which are ready to be grabbed.

Start every subagent with a fresh context window.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec (and any tickets) to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch.

4. Use a fresh **implementer subagent** for each unit, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `tdd` to build the unit;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier**, kick off more **implementer subagents** for the newly unblocked units. This allows for maximum concurrency.

7. Once every unit is merged, clean up all **implementer subagent** worktrees.

8. Return to [SKILL.md](SKILL.md) at **Prove it**, working on the integration branch. Its review step runs `code-review` on the whole branch; fix what it raises in a single fresh **implementer subagent**.


If the user asked for the `workhorse` pattern, give implementer subagents the economical model it names.
