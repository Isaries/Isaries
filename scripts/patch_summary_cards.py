"""Replace the profile-details card's "N Public Repos" line, which counts only public, non-fork repositories
the user owns, with the number of repositories committed to from build_stats.py's stats.json.

Usage: python patch_summary_cards.py <card_output_dir> <stats.json>
"""
import json
import re
import sys
from pathlib import Path

PUBLIC_REPOS = re.compile(r">\d+ Public Repos?<")

out, stats = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
cards = sorted(out.glob("*/0-profile-details.svg"))
if not cards:
    sys.exit(f"{out}: no profile-details cards found")
failed = False
for card in cards:
    text, n = PUBLIC_REPOS.subn(f">Committed to {stats['repositories']} Repos<", card.read_text(encoding="utf-8"))
    # Cards are regenerated on every run, so a missing line means the card's markup changed upstream.
    if n != 1:
        print(f"{card}: expected 1 Public Repos line, found {n}", file=sys.stderr)
        failed = True
        continue
    card.write_text(text, encoding="utf-8", newline="\n")
sys.exit(1 if failed else 0)
