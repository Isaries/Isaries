"""Fail if any local image the README references is missing or empty.

The card actions log per-card API errors yet exit 0, and they wipe their output folder first, so a
transient failure would otherwise be committed as a broken image. Checking against the README ties
the check to what the profile actually renders.
"""
import re
import sys
from pathlib import Path

readme = Path(sys.argv[1] if len(sys.argv) > 1 else "README.md")
paths = sorted(set(re.findall(r'(?:src|srcset)="\./([^"]+)"', readme.read_text(encoding="utf-8"))))
if not paths:
    sys.exit(f"{readme}: no local images found; the pattern no longer matches the README")
bad = [p for p in paths if not (readme.parent / p).is_file() or (readme.parent / p).stat().st_size == 0]
for p in bad:
    print(f"missing or empty: {p}", file=sys.stderr)
print(f"checked {len(paths)} images, {len(bad)} bad")
sys.exit(1 if bad else 0)
