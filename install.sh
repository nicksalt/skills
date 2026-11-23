#!/usr/bin/env bash
# Link this repo's skills into the folders agents read, so an edit here is live everywhere.
#
#   ./install.sh            link skills/* and trial/*
#   ./install.sh --dry-run  print what would change
#
# For each skill it makes ~/.agents/skills/<name> (Codex, and the `npx skills` layout)
# and ~/.claude/skills/<name> (Claude Code) symlinks to this repo. A real folder already
# at either path is moved to ~/.agents/skills/.trash/replaced-<date>/ first, never deleted.
# Skills this repo merged away (RETIRED) are moved to the same trash, and their entries are
# dropped from ~/.agents/.skill-lock.json so `npx skills update` doesn't bring them back.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
AGENTS="$HOME/.agents/skills"
CLAUDE="$HOME/.claude/skills"
LOCK="$HOME/.agents/.skill-lock.json"
TRASH="$AGENTS/.trash/replaced-$(date +%Y-%m-%d)"
DRY=0
[[ "${1:-}" == "--dry-run" ]] && DRY=1

RETIRED=(grill-me grill-with-docs to-spec to-tickets implement-spec improve-codebase-architecture
         diagnosing-bugs ask-matt setup-matt-pocock-skills t3-resume wizard
         benchmark-checklist)

run() { if (( DRY )); then echo "would: $*"; else "$@"; fi; }

to_trash() { # path
  local p="$1" name; name="$(basename "$p")"
  if [[ -L "$p" ]]; then run rm "$p"
  elif [[ -e "$p" ]]; then run mkdir -p "$TRASH"; run mv "$p" "$TRASH/$name.$(basename "$(dirname "$p")")"; fi
}

link() { # src dest
  local src="$1" dest="$2"
  if [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]; then return; fi
  to_trash "$dest"
  run ln -s "$src" "$dest"
  echo "linked $(basename "$dest") -> $src"
}

mkdir -p "$AGENTS" "$CLAUDE"
names=()
for dir in "$REPO"/skills/*/ "$REPO"/trial/*/; do
  [[ -f "$dir/SKILL.md" ]] || continue
  name="$(basename "$dir")"; src="${dir%/}"
  names+=("$name")
  link "$src" "$AGENTS/$name"
  link "$src" "$CLAUDE/$name"
done

for name in "${RETIRED[@]}"; do
  for base in "$AGENTS" "$CLAUDE"; do
    if [[ -e "$base/$name" || -L "$base/$name" ]]; then to_trash "$base/$name"; echo "retired $name from $base"; fi
  done
done

if [[ -f "$LOCK" ]]; then
  if (( DRY )); then
    echo "would: drop ${#names[@]} linked + ${#RETIRED[@]} retired names from $LOCK (backup alongside)"
  else
    cp "$LOCK" "$LOCK.bak-$(date +%Y%m%d%H%M%S)"
    python3 - "$LOCK" "${names[@]}" "${RETIRED[@]}" <<'PY'
import json, sys
path, drop = sys.argv[1], set(sys.argv[2:])
d = json.load(open(path))
removed = [k for k in list(d.get("skills", {})) if k in drop]
for k in removed:
    del d["skills"][k]
json.dump(d, open(path, "w"), indent=2)
print(f"lock: dropped {len(removed)} entries now owned by this repo")
PY
  fi
fi

echo "done: ${#names[@]} skills linked from $REPO"
