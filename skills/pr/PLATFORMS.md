# Platforms

The repo's `docs/agents/pull-requests.md` and `docs/agents/issue-tracker.md` win over this file. Use this file for the mechanics they don't cover.

## GitHub (`gh`)

- **Create:** `gh pr create --title ... --body-file <file> --base <base>`. If it fails because the GraphQL rate limit is used up, use REST: `gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@<file>`.
- **Update:** `gh pr edit <n> --body-file <file>`.
- **Link issues:** `Closes #<n>` in the body for each issue the PR completes; `Refs #<n>` for one it only advances.
- **Screenshots:** GitHub has no API for PR attachments. Commit the images to a dedicated evidence branch (for example `pr-evidence`, never the PR's own branch, so the diff stays clean), under a folder per PR, and embed them as `![What it shows](https://github.com/<owner>/<repo>/blob/pr-evidence/<pr>/<file>.png?raw=true)`. Scale each one to 1,600 px wide or less (`sips -Z 1600 <file>` on macOS). If the repo has its own way (a docs folder, an uploads action), use that.

## Azure DevOps (`az repos`)

Use the Azure CLI. Verify access with a read-only call first (`az repos show --repository <repo>`), and never print a token.

- **Create:** `az repos pr create --repository <repo> --source-branch <branch> --target-branch <base> --title ... --description "$(cat <file>)" --work-items <id> [<id> ...]`.
- **Update:** `az repos pr update --id <n> --description "$(cat <file>)"`.
- **Body limit:** Azure DevOps caps the description at 4,000 characters. Run `wc -m` before you post. Cut file trees before you cut evidence.
- **Link work items:** `--work-items` on create, or `az repos pr work-item add --id <n> --work-items <id>`. A PR that links no work item can't be completed on most boards.
- **Markdown:** ADO renders Mermaid only in some views and scrolls code blocks wider than about 90 characters. Prefer short code blocks and tables. Use one level of bullets at most.
- **Screenshots:** ADO shows an image only when it is an attachment of that PR; a local path or an outside link doesn't render. The PR must exist first (a draft is fine). Upload each file and put the returned `url` in the body:

  ```bash
  TOKEN=$(az account get-access-token \
    --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv)
  REPO_ID=$(az repos show --repository <repo> --query id -o tsv)
  curl -s -X POST -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/octet-stream" --data-binary @shot.png \
    "<org-url>/<project>/_apis/git/repositories/$REPO_ID/pullRequests/<pr-id>/attachments/<unique-name>.png?api-version=7.1-preview.1" \
    | python3 -c "import json,sys; print(json.load(sys.stdin)['url'])"
  ```

  Give each file a name unique within the PR. Each image link costs about 210 of the 4,000 characters, so pick the few that matter.
- **Comments:** `az repos pr` has no thread command. Post threads with `az devops invoke --area git --resource pullRequestThreads --route-parameters project=<project> repositoryId=<repo-id> pullRequestId=<n> --http-method POST --in-file <thread.json> --api-version 7.1`.
