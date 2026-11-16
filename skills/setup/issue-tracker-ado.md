# Issue tracker: Azure DevOps

Work items for this repo live on the Azure DevOps board. Use the **Azure CLI only**: `az boards` for work items, `az repos` for PRs, `az rest` / `az devops invoke` for process and board APIs. The CLI must be installed and logged in where the agent runs; a browser login or MCP connection does not count. Verify with a read-only call before any write. Never print credentials.

## Project identity

- Organization: `<https://dev.azure.com/your-org>`
- Project: `<Project>`. Pass `--org` and `--project` explicitly; verify an item's project before updating it by ID.
- Human link: `<org>/<project>/_workitems/edit/{id}`. Report each item's title, ID and link.

## Team workflow

One work item owns one independently prioritizable outcome. Keep implementation steps, decisions, internal blocking order and verification checklists **inside** the item. Split only for independent priority, ownership, delivery, material risk, or separately managed acceptance. A service boundary, a spec section, or a fresh agent context alone does not justify another item.

- **Types:** `<Bug>` for broken expected behavior, `<Enhancement | User Story | Feature>` for new or improved behavior. Don't create retired types.
- **Parent:** link new outcomes to an existing `<Epic>`. Ask when none fits; Epics are durable product areas, not per-ticket containers.
- **New items** land in `<Triage column>` with state `New`. Backlog order is the priority.
- **States:** `New` → `Active` (being worked) → `Resolved` (complete, awaiting review or deployment) → `Done` / `Closed` (merged and deployed, with evidence).

## Conventions

- **Create:** `az boards work-item create --org <org> --project <project> --type "<type>" --title "..." --description "<html>" --fields "System.Tags=<tags>"`. Descriptions and acceptance criteria are HTML: use `<p>`, `<ul><li>`, `<h3>`; not Markdown.
- **Read:** `az boards work-item show --org <org> --id <id> --expand relations`.
- **Query:** `az boards query --org <org> --project <project> --wiql "SELECT [System.Id],[System.Title],[System.State] FROM WorkItems WHERE ..."`.
- **Update:** `az boards work-item update --org <org> --id <id> --state "<state>" --fields "..."`. Append to a field instead of overwriting someone else's text.
- **Comment:** `az boards work-item update --org <org> --id <id> --discussion "<html>"`.
- **Parent:** `az boards work-item relation add --org <org> --id <child> --relation-type parent --target-id <parent>`.
- **Blocking:** `az boards work-item relation add --org <org> --id <blocked> --relation-type predecessor --target-id <blocker>` (the blocker is the Predecessor). An item is startable when every Predecessor is `Resolved` or later.
- **Link a PR:** `--work-items <id>` on `az repos pr create`, or `az repos pr work-item add --id <pr> --work-items <id>`.

## Readiness tags

Azure DevOps has tags, not labels. The triage roles map to tags (see `triage-labels.md`). Apply with `--fields "System.Tags=<existing>; <tag>"`: read the current tags first, because setting the field replaces them.

## When a skill says "publish to the issue tracker"

Create one work item per outcome, as above, with the `ready-for-agent` tag (or this repo's equivalent).

## When a skill says "fetch the relevant ticket"

Read it as in **Read** above, including its relations and discussion.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a parent work item (an Epic or Feature tagged `wayfinder:map`); **child** tickets are its children, tagged `wayfinder:<type>`.

- **Frontier query:** the map's open children with no open Predecessor and no assignee; first in backlog order wins.
- **Claim:** assign the child to yourself and set it `Active`, as the session's first write.
- **Resolve:** comment the answer, set it `Resolved`, then append a context pointer (gist + link) to the map's description.
