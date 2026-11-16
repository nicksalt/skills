# Working in this repo

This repo holds Nick's personal agent skills. Each folder under `skills/` (or `trial/`) is one skill with a `SKILL.md`; `install.sh` symlinks them into `~/.agents/skills` and `~/.claude/skills`, so an edit here is live at once.

- Edit skill prose by the `writing-for-agents` skill. Keep `name:` equal to the folder name.
- `disable-model-invocation: true` means manual only. Keep each skill's `agents/openai.yaml` `allow_implicit_invocation` in step with it.
- Keep skills generic and public: no organization names, project IDs, credentials, or customer details. Repo-specific rules belong in that repo's `docs/agents/*.md` or its own `.agents/skills/`.
- When you merge, rename, or add a skill, update `upstream.json`, `README.md`, `docs/flows.md`, and `skills/ask-nick/SKILL.md` in the same change. Add a retired name to `RETIRED` in `install.sh`.
- Upstream changes are reviewed by `docs/upstream-review.md`. Don't bump `synced` in `upstream.json` without applying or explicitly skipping the reviewed changes.
