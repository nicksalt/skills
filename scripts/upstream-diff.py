#!/usr/bin/env python3
"""Collect what changed upstream since each source's synced commit.

  scripts/upstream-diff.py [--out DIR]

Reads upstream.json, asks GitHub (via the authenticated `gh` CLI) for the commits
on each source's branch since `synced`, and writes:

  DIR/digest.md        one section per source: releases, commits with their PR
                       title and body (the "why"), changed files mapped to our
                       skills, and new upstream skills we have not seen
  DIR/patches/<source>/<path>.diff   the upstream patch per changed file
  DIR/state.json       per source, the head SHA (and newest release tag) to
                       write back into upstream.json once the digest is reviewed

It only reads. It never edits skills or upstream.json. Exit 0 even when nothing
changed (the digest says so).
"""
import argparse
import fnmatch
import json
import pathlib
import subprocess
import sys
import tempfile
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent


def gh(path, paginate=False):
    args = ["gh", "api", "-H", "Accept: application/vnd.github+json", path]
    if paginate:
        args.insert(2, "--paginate")
    out = subprocess.run(args, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"gh api {path}: {out.stderr.strip()}")
    text = out.stdout.strip()
    if paginate and text.startswith("[") and "][" in text:
        text = "[" + text[1:-1].replace("][", ",") + "]"
    return json.loads(text or "null")


def skill_dir(path, watch):
    for w in watch:
        if path.startswith(w.rstrip("/") + "/"):
            rest = path[len(w.rstrip("/")) + 1 :]
            first = rest.split("/", 1)[0]
            if first.endswith(".md") and "/" not in rest:
                return f"{w.rstrip('/')}/{first}"
            return f"{w.rstrip('/')}/{first}"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=None)
    ap.add_argument("--manifest", default=str(ROOT / "upstream.json"))
    a = ap.parse_args()
    out = pathlib.Path(a.out or tempfile.mkdtemp(prefix=f"upstream-{date.today()}-"))
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(pathlib.Path(a.manifest).read_text())

    owners = {}
    for ours, parts in manifest["skills"].items():
        for p in parts:
            owners.setdefault((p["source"], p["path"]), []).append(ours)

    lines = [f"# Upstream digest, {date.today()}", ""]
    state = {}
    for name, src in manifest["sources"].items():
        repo, branch, synced, watch = src["repo"], src["branch"], src["synced"], src["watch"]
        declined = manifest.get("declined", {}).get(name, [])
        lines += [f"## {name} ({repo})", ""]
        try:
            head = gh(f"repos/{repo}/commits/{branch}")["sha"]
        except RuntimeError as e:
            lines += [f"Could not read {repo}: {e}", ""]
            continue
        state[name] = {"synced": head}
        if head == synced:
            if src.get("release") is not None:
                state[name]["release"] = src["release"]
            lines += [f"No new commits since `{synced[:10]}`.", ""]
            continue
        cmp = gh(f"repos/{repo}/compare/{synced}...{head}")
        commits = cmp.get("commits", [])
        files = [f for f in cmp.get("files", []) if any(f["filename"].startswith(w.rstrip("/") + "/") for w in watch)]
        lines.append(f"`{synced[:10]}` → `{head[:10]}`: {len(commits)} commits, {len(files)} watched files changed.")
        if cmp.get("total_commits", 0) > len(commits) or len(cmp.get("files", [])) >= 300:
            lines.append("**Truncated by GitHub's compare limits.** Read the repo history directly for the rest.")
        lines.append("")

        if src.get("release") is not None:
            rels = gh(f"repos/{repo}/releases?per_page=20") or []
            if rels:
                state[name]["release"] = rels[0]["tag_name"]
            newer = []
            for r in rels:
                if r["tag_name"] == src["release"]:
                    break
                newer.append(r)
            if newer:
                lines.append("### Releases")
                for r in reversed(newer):
                    body = (r.get("body") or "").strip()
                    lines += [f"#### {r['tag_name']} ({r['published_at'][:10]})", "", body[:4000], ""]

        touched = {}
        for f in files:
            d = skill_dir(f["filename"], watch)
            touched.setdefault(d, []).append(f)
            patch = f.get("patch")
            if patch:
                p = out / "patches" / name / (f["filename"] + ".diff")
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(patch)

        lines.append("### Changed skills")
        for d, fs in sorted(touched.items(), key=lambda kv: kv[0] or ""):
            mine = owners.get((name, d), [])
            short = (d or "").rsplit("/", 1)[-1].removesuffix(".md")
            if mine:
                tag = "ours: " + ", ".join(f"`{m}`" for m in mine)
            elif any(fnmatch.fnmatch(short, pat) for pat in declined):
                tag = "declined"
            elif any(f["status"] == "added" for f in fs) and not any(f["status"] != "added" for f in fs):
                tag = "**new upstream skill**"
            else:
                tag = "not tracked"
            lines.append(f"- `{d}` ({tag}): " + ", ".join(f"{f['filename'].rsplit('/', 1)[-1]} {f['status']} +{f['additions']}/-{f['deletions']}" for f in fs))
        lines.append("")

        lines.append("### Commits (the why)")
        seen_prs = set()
        for c in commits:
            sha = c["sha"]
            msg = c["commit"]["message"].strip()
            first, _, rest = msg.partition("\n")
            lines.append(f"- `{sha[:10]}` {first}")
            if rest.strip():
                lines.append("  > " + rest.strip()[:1200].replace("\n", "\n  > "))
            try:
                prs = gh(f"repos/{repo}/commits/{sha}/pulls") or []
            except RuntimeError:
                prs = []
            for pr in prs:
                if pr["number"] in seen_prs:
                    continue
                seen_prs.add(pr["number"])
                body = (pr.get("body") or "").strip()
                lines.append(f"  - PR #{pr['number']}: {pr['title']} ({pr['html_url']})")
                if body:
                    lines.append("    > " + body[:2000].replace("\n", "\n    > "))
        lines.append("")

    (out / "digest.md").write_text("\n".join(lines) + "\n")
    (out / "state.json").write_text(json.dumps(state, indent=2) + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
