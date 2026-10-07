"""Strip parts of github-profile-3d-contrib output that it offers no option to hide.

Removed: the star and fork counters (always 0 here) and the language pie, which credits every commit
to a repository's primary language; scripts/build_lang_card.py replaces it.
"""
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


def remove_group(text, start):
    depth = 0
    for m in TAG.finditer(text, start):
        if m.group(2):
            continue
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return text[:start] + text[m.end():]
    raise ValueError("unbalanced <g>")


def process(text):
    text, n = COUNTER.subn("", text)
    if n != 2:
        raise ValueError(f"expected 2 counters, found {n}")
    if text.count(PIE_OPEN) != 1:
        raise ValueError(f"expected 1 language pie, found {text.count(PIE_OPEN)}")
    return remove_group(text, text.index(PIE_OPEN))


# The workflow always processes freshly generated files, so any mismatch means the markup changed upstream.
failed = False
for svg in sorted(Path(sys.argv[1]).glob("*.svg")):
    try:
        svg.write_text(process(svg.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
    except ValueError as e:
        print(f"{svg}: {e}", file=sys.stderr)
        failed = True
sys.exit(1 if failed else 0)
