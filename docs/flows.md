# Flows

How the skills chain. Solid arrows are a skill calling another; dotted arrows are optional detours. `/name` means manual only: it runs when you call it. Everything else the agent can pick up on its own.

## Main flow: idea → ready-to-merge PR

```mermaid
flowchart LR
  idea([Idea]) --> grill["/grilling"]
  grill -.->|in a repo| dm[domain-modeling]
  grill -.->|needs a runnable answer| proto[prototype]
  grill -.->|task feels shallow| sharpen["/sharpen"]
  grill --> spec[spec]
  spec -->|one ticket| impl[implement]
  impl --> pr[pr]
  pr --> babysit[babysit-pr]
  babysit --> gate{{merge gate}}
  gate -->|full stop: default| ready([Ready for you to merge])
  gate -->|full send| merged([Merged])
  ready -.-> retro["/retro"]
  merged -.-> retro
  retro -.->|repeat mistake| correct["/correct"]
```

## Inside `implement`

```mermaid
flowchart TB
  start([Ticket or agreed change]) --> size{Fits one session?}
  size -->|yes| build[Build with tdd]
  size -->|no: BIG-WORK.md| fan[Integration branch,<br/>one subagent per step,<br/>each runs tdd]
  fan --> prove
  build --> prove[Prove it]
  prove -.->|repo has one| verify["verify-&lt;app&gt; skill"]
  prove -.->|shared contract| blast[blast-radius]
  prove --> review[code-review]
  review -.->|only if asked| council["/council"]
  review --> file[pr: problem first,<br/>before/after visuals]
  file --> watch[babysit-pr:<br/>pr-wait / watch_pull_request /<br/>ado-pr-wait]
  watch -->|findings or CI| prove
  watch --> gate{{Merge gate}}
```

## Side flows

```mermaid
flowchart LR
  bug([Something broke]) --> diag[diagnose] --> implp[implement: Prove onward]
  diag -.->|not for now| spec[spec]
  inbox([Issues / external PRs]) --> triage["/triage"] -->|agent-ready brief| impl[implement]
  huge([Too big to plan in one go]) --> way["/wayfinder"]
  huge --> fio["/figure-it-out"]
  theirs([Someone else's PR or thread]) --> take[takeover]
  take -.->|just rebase| mod[takeover: modernize mode]
  take --> pr[pr] --> bab[babysit-pr]
  later([Pick work back up]) --> hand["/handoff: resume"]
  stop([Stop for now]) --> handw["/handoff: write"]
```

## Before you build, and around it

```mermaid
flowchart LR
  q([A question about the code]) --> explain[explain]
  explain -->|How mode| how[what it does now]
  explain -->|Why mode| why[what the record says]
  design([Designing a module]) --> cd[codebase-design]
  cd -->|Architect mode| sketch[types and signatures first]
  cd -->|Scan mode| scan[HTML report of deepening candidates] --> grill["/grilling"]
  change([A risky diff]) --> blast[blast-radius]
  learn([I want to understand it]) --> teach["/teach"]
  facts([Need primary sources]) --> research["/research"]
  newrepo([New repo]) --> setup["/setup"] --> docs[(docs/agents/*.md)]
  newrepo --> vcreate[verification: create] --> vskill["verify-&lt;app&gt; skill"]
  vskill -.->|app changed| vmaint[verification: maintain]
```

## What every repo provides

The skills stay generic. Each repo tells them its specifics in `docs/agents/`, written by `/setup`:

| File | Read by | Says |
|---|---|---|
| `issue-tracker.md` | spec, triage, wayfinder, implement, code-review | GitHub, Azure DevOps, GitLab or local; how to create, link, block, close |
| `triage-labels.md` | triage, spec | the label or tag for each triage role |
| `pull-requests.md` | pr, babysit-pr, implement | review policy, body limits, required sections, evidence mechanics |
| `domain.md` | grilling, domain-modeling, codebase-design | where `GLOSSARY.md` and ADRs live |

Project-only skills (`verify-*`, work-item helpers, meeting sweeps) live in the project's `.agents/skills/`, not here.
