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

from palette import FONT, PALETTES, SERIES, SERIES_OTHER

YEARS_QUERY = "query($login:String!){user(login:$login){contributionsCollection{contributionYears}}}"
AUTHORED_QUERY = """query($login:String!,$after:String){user(login:$login){
  pullRequests(states:MERGED,first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{id}}}}"""
REPO_PRS_QUERY = """query($owner:String!,$name:String!,$after:String){repository(owner:$owner,name:$name){
  pullRequests(states:MERGED,first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{id mergedBy{login}}}}}"""
REPOS_QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){
  restrictedContributionsCount
  totalPullRequestReviewContributions
  commitContributionsByRepository(maxRepositories:100){
    contributions{totalCount}
    repository{nameWithOwner languages(first:100){edges{size node{name}}}}
  }}}}"""

THEMES = {theme: dict(bg=p["bg"], border=p["border"], title=p["accent"], text=p["muted"], strong=p["fg"])
          for theme, p in PALETTES.items()}
ROWS = 6
ROW_H = 22


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
    return body["data"]


def paginate(query, path, **variables):
    after = None
    while True:
        conn = gql(query, after=after, **variables)
        for key in path:
            conn = conn[key]
        yield from conn["nodes"]
        if not conn["pageInfo"]["hasNextPage"]:
            return
        after = conn["pageInfo"]["endCursor"]


def merged_prs(login, repos):
    """PRs the user authored that were merged, plus PRs anyone authored (bots included) that the user merged.

    GitHub has no "merged by" search, so the second set is collected from each repository the user
    committed to, which is where they hold merge rights in practice.
    """
    authored = {pr["id"] for pr in paginate(AUTHORED_QUERY, ("user", "pullRequests"), login=login)}
    merged_by_user = set()
    for full_name in repos:
        owner, name = full_name.split("/")
        for pr in paginate(REPO_PRS_QUERY, ("repository", "pullRequests"), owner=owner, name=name):
            if (pr["mergedBy"] or {}).get("login", "").lower() == login.lower():
                merged_by_user.add(pr["id"])
    return len(authored), len(merged_by_user), len(authored | merged_by_user)


def collect(login):
    weights = defaultdict(float)
    repos, commits, reviews, restricted = set(), 0, 0, 0
    pr_repos = set()
    for year in gql(YEARS_QUERY, login=login)["user"]["contributionsCollection"]["contributionYears"]:
        data = gql(REPOS_QUERY, login=login, **{"from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        data = data["user"]["contributionsCollection"]
        restricted += data["restrictedContributionsCount"]
        reviews += data["totalPullRequestReviewContributions"]
        for item in data["commitContributionsByRepository"]:
            repo = item["repository"]
            pr_repos.add(repo["nameWithOwner"])
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
    authored, merged_by_user, prs = merged_prs(login, sorted(pr_repos))
    stats = dict(commits=commits, repositories=len(repos), prs_merged=prs, prs_authored_merged=authored,
                 prs_merged_by_user=merged_by_user, reviews=reviews, restricted_contributions=restricted)
    return weights, stats


def top_rows(weights):
    total = sum(weights.values())
    ranked = sorted(weights.items(), key=lambda kv: kv[1], reverse=True)
    rows = [(name, w / total, SERIES[i]) for i, (name, w) in enumerate(ranked[: ROWS - 1])]
    rest = sum(w for _, w in ranked[ROWS - 1:]) / total
    if len(ranked) == ROWS:
        name, w = ranked[-1]
        rows.append((name, w / total, SERIES[ROWS - 1]))
    elif rest > 0:
        rows.append(("Other", rest, SERIES_OTHER))
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
<style>*{{font-family:{FONT}}}</style>
<rect x="1" y="1" rx="5" ry="5" width="338" height="198" fill="{c["bg"]}" stroke="{c["border"]}"/>
<text x="30" y="40" style="font-size:22px;fill:{c["title"]}">Languages by Commit</text>
{"".join(legend)}
{"".join(slices)}
</svg>
'''


def main():
    login, out = sys.argv[1], Path(sys.argv[2])
    weights, stats = collect(login)
    if not weights:
        sys.exit("no commit contributions with language data")
    rows = top_rows(weights)
    print(" ".join(f"{k}={v}" for k, v in stats.items()))
    total = sum(weights.values())
    print(", ".join(f"{k} {w / total:.1%}" for k, w in sorted(weights.items(), key=lambda kv: -kv[1])[:10]))
    out.mkdir(parents=True, exist_ok=True)
    for theme, palette in THEMES.items():
        (out / f"languages-{theme}.svg").write_text(render(rows, palette), encoding="utf-8", newline="\n")
    (out / "stats.json").write_text(json.dumps(stats, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
