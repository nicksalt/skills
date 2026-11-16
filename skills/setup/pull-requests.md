# Pull requests

Repo-specific rules for the `pr`, `babysit-pr` and `implement` skills. These win over the skills' defaults.

## Platform

`<GitHub | Azure DevOps>`. Default branch: `<main>`. Merge method: `<squash | merge | rebase>`.

## Review and completion

- Who must approve, and when the author may self-approve: `<rule>`.
- Required checks or build policies: `<names>`.
- Review bots, and which ones block: `<Greptile / Macroscope / CodeRabbit / none>`.
- Anything an agent must never do here (for example: complete the PR, requeue a policy): `<rule>`.

## Body

- Write for `<a teammate outside this service | the maintainer>`.
- Required sections beyond the `pr` skill's template: `<none | e.g. a Replay heading for changes under path X>`.
- Length limit: `<none | 4,000 characters on Azure DevOps>`.
- Attribution line: `<the harness default | none>`.

## Evidence

- How to capture screenshots here: `<Storybook | a fixture command | the verify-<app> skill>`.
- Where the images go: `<the evidence branch | PR attachments>`.
- Never from production data.
