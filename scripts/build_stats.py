"""Collect all-time profile stats and render a language card that splits each repository's commits by
that repository's language mix.

The stock cards credit every commit to a repository's primary language, so a Python + Vue project counts
as 100% Python. Here each repository's commit count is distributed by its linguist byte shares, over all
years and every repository the token can see (personal, organization and private).

Usage: GITHUB_TOKEN=... python build_stats.py <login> <output_dir>
Writes languages-{dark,light}.svg and stats.json. Only aggregates are printed or written, because Actions
logs and files on a public repository are public.
"""
import json
import math
import os
import sys
import urllib.request
from collections import defaultdict
from html import escape
from pathlib import Path

USER_QUERY = """query($login:String!){user(login:$login){
  pullRequests(states:MERGED){totalCount}
  contributionsCollection{contributionYears}}}"""
REPOS_QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){
  restrictedContributionsCount
  totalPullRequestReviewContributions
  commitContributionsByRepository(maxRepositories:100){
    contributions{totalCount}
    repository{nameWithOwner languages(first:100){edges{size node{name color}}}}
  }}}}"""

THEMES = {
    "dark": dict(bg="#0d1117", border="#2e343b", title="#0366d6", text="#77909c", strong="#c9d1d9"),
    "light": dict(bg="#ffffff", border="#e4e2e2", title="#0366d6", text="#586069", strong="#24292f"),
}
ROWS = 6
ROW_H = 22
OTHER_COLOR = "#8b949e"


def gql(query, **variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        body = json.load(resp)
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return body["data"]["user"]


def collect(login):
    weights, colors = defaultdict(float), {}
    repos, commits, reviews, restricted = set(), 0, 0, 0
    user = gql(USER_QUERY, login=login)
    for year in user["contributionsCollection"]["contributionYears"]:
        data = gql(REPOS_QUERY, login=login, **{"from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        data = data["contributionsCollection"]
        restricted += data["restrictedContributionsCount"]
        reviews += data["totalPullRequestReviewContributions"]
        for item in data["commitContributionsByRepository"]:
            repo = item["repository"]
            # The profile repository holds README edits and these generators, not project code.
            if repo["nameWithOwner"].lower() == f"{login}/{login}".lower():
                continue
            n = item["contributions"]["totalCount"]
            repos.add(repo["nameWithOwner"])
            commits += n
            edges = repo["languages"]["edges"]
            total = sum(e["size"] for e in edges)
            for e in edges:
                weights[e["node"]["name"]] += n * e["size"] / total
                colors[e["node"]["name"]] = e["node"]["color"] or OTHER_COLOR
    stats = dict(commits=commits, repositories=len(repos), merged_prs=user["pullRequests"]["totalCount"],
                 reviews=reviews, restricted_contributions=restricted)
    return weights, colors, stats


def top_rows(weights, colors):
    total = sum(weights.values())
    ranked = sorted(weights.items(), key=lambda kv: kv[1], reverse=True)
    rows = [(name, w / total, colors[name]) for name, w in ranked[: ROWS - 1]]
    rest = sum(w for _, w in ranked[ROWS - 1:]) / total
    if len(ranked) == ROWS:
        name, w = ranked[-1]
        rows.append((name, w / total, colors[name]))
    elif rest > 0:
        rows.append(("Other", rest, OTHER_COLOR))
    return rows


def arc(cx, cy, r_out, r_in, a0, a1):
    large = 1 if a1 - a0 > math.pi else 0
    p = lambda r, a: (cx + r * math.sin(a), cy - r * math.cos(a))
    (x0, y0), (x1, y1) = p(r_out, a0), p(r_out, a1)
    (x2, y2), (x3, y3) = p(r_in, a1), p(r_in, a0)
    return (f"M{x0:.2f} {y0:.2f}A{r_out} {r_out} 0 {large} 1 {x1:.2f} {y1:.2f}"
            f"L{x2:.2f} {y2:.2f}A{r_in} {r_in} 0 {large} 0 {x3:.2f} {y3:.2f}Z")


def render(rows, c):
    legend, slices, a = [], [], 0.0
    for i, (name, share, color) in enumerate(rows):
        y = 56 + i * ROW_H
        legend.append(
            f'<rect x="40" y="{y:.1f}" width="14" height="14" fill="{color}" stroke="{c["bg"]}"/>'
            f'<text x="62" y="{y + 12:.1f}" style="fill:{c["text"]};font-size:14px">{escape(name)}</text>'
            f'<text x="182" y="{y + 12:.1f}" text-anchor="end" style="fill:{c["strong"]};font-size:14px;font-weight:600">{share * 100:.1f}%</text>'
        )
        # A lone 100% slice would draw a zero-length arc, so cap it just short of a full turn.
        a1 = min(a + share * 2 * math.pi, 2 * math.pi - 1e-4)
        slices.append(f'<path d="{arc(262, 120, 55, 33, a, a1)}" fill="{color}" stroke="{c["bg"]}" stroke-width="2"/>')
        a = a1
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="340" height="200" viewBox="0 0 340 200" role="img" aria-label="Languages by commit, weighted by each repository's language mix">
<style>*{{font-family:'Segoe UI',Ubuntu,"Helvetica Neue",Sans-Serif}}</style>
<rect x="1" y="1" rx="5" ry="5" width="338" height="198" fill="{c["bg"]}" stroke="{c["border"]}"/>
<text x="30" y="40" style="font-size:22px;fill:{c["title"]}">Languages by Commit</text>
{"".join(legend)}
{"".join(slices)}
</svg>
'''


def main():
    login, out = sys.argv[1], Path(sys.argv[2])
    weights, colors, stats = collect(login)
    if not weights:
        sys.exit("no commit contributions with language data")
    rows = top_rows(weights, colors)
    print(" ".join(f"{k}={v}" for k, v in stats.items()))
    total = sum(weights.values())
    print(", ".join(f"{k} {w / total:.1%}" for k, w in sorted(weights.items(), key=lambda kv: -kv[1])[:10]))
    out.mkdir(parents=True, exist_ok=True)
    for theme, palette in THEMES.items():
        (out / f"languages-{theme}.svg").write_text(render(rows, palette), encoding="utf-8", newline="\n")
    (out / "stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
