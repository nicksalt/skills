# Weekly upstream review

The skills here are adapted from public libraries. This review keeps them in step with what those libraries learn, without overwriting the adaptations.

A scheduled T3 task runs it every Monday morning. You can also run it by hand: "do the upstream review in the skills repo".

## Steps

1. From the repo root, `git pull`, then run `python3 -I scripts/upstream-diff.py`. It prints a directory holding `digest.md`, `patches/`, and `state.json`. It only reads.
2. If every source says "No new commits" and no release is new, stop. Post one line: "No upstream changes this week."
3. Otherwise, for each changed upstream skill that `upstream.json` maps to one of ours:
   - Read the upstream patch, the commit messages and PR bodies in the digest (the *why*), and **our current version** of the skill.
   - Decide one of: **port** (the improvement applies to our version; say where it goes), **adapt** (the idea applies but needs rewording for how we changed the skill), **skip** (it only touches something we removed or changed on purpose; say what).
   - Judge against our version, not upstream's. Many of our skills merge several upstream ones (see `upstream.json`), so one upstream change may land in a mode file such as `implement/FULL-SEND.md` or `pr/COMMENTS.md`.
4. For **new upstream skills**, one line each: what it does, and whether it overlaps one of ours or fills a gap. Declined skills (in `upstream.json`) get one line only if the change would make you reconsider.
5. Open one GitHub issue in this repo titled `Upstream review: <date>` with:
   - a summary table (upstream skill → our skill → port / adapt / skip → one-line reason);
   - for each port or adapt, the proposed edit as a short diff or quote, with the upstream link;
   - the new-skills list;
   - the `state.json` values to write into `upstream.json` once the review is applied.
   Use `gh issue create --repo nicksalt/skills`. Don't open a PR and don't edit skills: Nick decides first.
6. Post the issue link as the run's result.

## Applying a review

When Nick says which items to take: make the edits on a branch, bump `synced` (and `release`) in `upstream.json` to the reviewed `state.json` values, and open one PR that closes the issue. Edit prose by the `writing-for-agents` skill.
