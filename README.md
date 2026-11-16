# skills

The agent skills I use every day, adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills), [tstack](https://github.com/t3dotgg/tstack) and [pstack](https://github.com/cursor/plugins/tree/main/pstack), merged down so there are fewer to remember. They work in Claude Code, Codex and T3 Code, on GitHub and Azure DevOps.

Start with [`docs/flows.md`](docs/flows.md) for how they chain, or run `/ask-nick`.

## Skills

`/name` = manual only. The rest the agent can pick up on its own.

| Area | Skill | What it does |
|---|---|---|
| Think | `grilling` | Interview a plan a round at a time; records glossary terms and ADRs as they settle |
| | `domain-modeling` | Build `GLOSSARY.md` and ADRs |
| | `codebase-design` | Deep-module vocabulary, plus Architect (sketch types first) and Scan (find deepening opportunities) modes |
| | `explain` | How code works (How mode) or why it's that way (Why mode) |
| | `/sharpen` | Make a task deeper, not bigger |
| | `/teach`, `research`, `/to-questionnaire` | Learn it, research it, or hand a decision to someone else |
| Plan | `spec` | Write the conversation up as one ticket that owns the outcome |
| | `/triage`, `/wayfinder`, `/figure-it-out` | Incoming issues; plans too big for one session; auditable playbooks for ambitious changes |
| Build | `implement` | Ticket → proven, reviewed PR, ready to merge. "full send" also merges |
| | `tdd`, `prototype`, `diagnose` | Test-first, throwaway prototypes, hard bugs |
| | `/workhorse` | Hand implementation to cheaper models |
| Prove | `verification` | Create or maintain a repo's `verify-<app>` skill |
| | `blast-radius`, `/correct` | What a change breaks elsewhere; make repeat mistakes impossible |
| Review | `code-review`, `/council` | Standards and spec review; multi-model review (you pick the models) |
| PRs | `pr`, `babysit-pr`, `takeover` | File with before/after evidence; watch CI and bots; finish or modernize someone's PR |
| Context | `/handoff`, `/wait-what`, `/retro` | Write or resume a handoff; re-pitch; learn from a session |
| Meta | `writing-for-agents`, `/unslop`, `/setup`, `/ask-nick` | Write skills; cut AI tells; configure a repo; find the right skill |

`trial/` holds skills on probation: `ketchup`, `automate-me`, `benchmark-checklist`, `no-comments`.

## Install

```bash
git clone https://github.com/nicksalt/skills
cd skills && ./install.sh          # or ./install.sh --dry-run first
```

`install.sh` symlinks every skill into `~/.agents/skills/` (Codex and `npx skills`) and `~/.claude/skills/` (Claude Code), so edits in the clone are live. Anything it replaces goes to `~/.agents/skills/.trash/`.

Without cloning: `npx skills add nicksalt/skills` (copies, no live edits).

Then run `/setup` once in each repo. The skills read that repo's specifics (tracker, PR rules, glossary) from `docs/agents/`.

## Staying in step with upstream

`upstream.json` records which upstream skills each one came from and the commit it was last synced to. Every Monday a scheduled task runs [`docs/upstream-review.md`](docs/upstream-review.md): `scripts/upstream-diff.py` collects what changed upstream and why, and an agent opens an issue saying what to port, adapt, or skip. Nothing changes until I say so.

## License

MIT. Upstream notices are in [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md).
