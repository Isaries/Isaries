"""Remove the star and fork counters that github-profile-3d-contrib draws with no option to hide them."""
import re
import sys
from pathlib import Path

# Icon <g> at scale(2) followed by its number; the generator emits exactly one each for stars and forks.
COUNTER = re.compile(
    r'<g transform="translate\(\d+, \d+\), scale\(2\)"><path [^>]*></path></g>'
    r"<text [^>]*>[^<]*<title>[^<]*</title></text>"
)

failed = False
for svg in sorted(Path(sys.argv[1]).glob("*.svg")):
    text = svg.read_text(encoding="utf-8")
    stripped, n = COUNTER.subn("", text)
    # The workflow always strips freshly generated files, so any other count means the markup changed upstream.
    if n != 2:
        print(f"{svg}: expected 2 counters, found {n}", file=sys.stderr)
        failed = True
        continue
    svg.write_text(stripped, encoding="utf-8", newline="\n")
sys.exit(1 if failed else 0)
