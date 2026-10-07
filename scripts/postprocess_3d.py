"""Adjust github-profile-3d-contrib output in ways it offers no option for.

Removed: the star and fork counters (always 0 here) and the language pie, which credits every commit
to a repository's primary language (scripts/build_stats.py renders the weighted card instead). The pie's
corner is filled with all-time totals from build_stats.py's stats.json.

Usage: python postprocess_3d.py <svg_dir> <stats.json>
"""
import json
import re
import sys
from pathlib import Path

# Icon <g> at scale(2) followed by its number; the generator emits exactly one each for stars and forks.
COUNTER = re.compile(
    r'<g transform="translate\(\d+, \d+\), scale\(2\)"><path [^>]*></path></g>'
    r"<text [^>]*>[^<]*<title>[^<]*</title></text>"
)
PIE_OPEN = '<g transform="translate(40, 520)">'
TAG = re.compile(r"<(/?)g\b[^>]*?(/?)>")


def replace_group(text, start, replacement):
    depth = 0
    for m in TAG.finditer(text, start):
        if m.group(2):
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return text[:start] + replacement + text[m.end():]
    raise ValueError("unbalanced <g>")


def compact(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def totals_group(stats):
    cells = [("commits", stats["commits"]), ("repositories", stats["repositories"]),
             ("merged PRs", stats["merged_prs"]), ("code reviews", stats["reviews"])]
    parts = ['<text x="20" y="20" style="font-size: 16px; letter-spacing: 2px;" class="fill-weak">ALL TIME</text>']
    for i, (label, value) in enumerate(cells):
        x, y = 20 + (i % 2) * 210, 85 + (i // 2) * 105
        parts.append(f'<text x="{x}" y="{y}" style="font-size: 44px; font-weight: bold;" class="fill-strong">{compact(value)}</text>'
                     f'<text x="{x}" y="{y + 30}" style="font-size: 20px;" class="fill-fg">{label}</text>')
    return f'{PIE_OPEN}{"".join(parts)}</g>'


def process(text, totals):
    text, n = COUNTER.subn("", text)
    if n != 2:
        raise ValueError(f"expected 2 counters, found {n}")
    if text.count(PIE_OPEN) != 1:
        raise ValueError(f"expected 1 language pie, found {text.count(PIE_OPEN)}")
    return replace_group(text, text.index(PIE_OPEN), totals)


# The workflow always processes freshly generated files, so any mismatch means the markup changed upstream.
totals = totals_group(json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")))
failed = False
for svg in sorted(Path(sys.argv[1]).glob("*.svg")):
    try:
        svg.write_text(process(svg.read_text(encoding="utf-8"), totals), encoding="utf-8", newline="\n")
    except ValueError as e:
        print(f"{svg}: {e}", file=sys.stderr)
        failed = True
sys.exit(1 if failed else 0)
