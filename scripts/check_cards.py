"""Exit 1 if a card theme's output folder lacks any of the five summary cards.

The card action logs per-card API errors (e.g. a 502) yet exits 0, so this is how the workflow notices a
run needs repeating.

Usage: python check_cards.py <theme>
"""
import sys
from pathlib import Path

CARDS = ["0-profile-details", "1-repos-per-language", "2-most-commit-language", "3-stats", "4-productive-time"]

theme = sys.argv[1]
bad = [c for c in CARDS if not (p := Path("profile-summary-card-output") / theme / f"{c}.svg").is_file() or p.stat().st_size == 0]
for c in bad:
    print(f"missing or empty: {theme}/{c}.svg", file=sys.stderr)
sys.exit(1 if bad else 0)
