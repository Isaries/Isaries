"""Patch the summary cards in ways the card action offers no option for.

The profile-details card's "N Public Repos" line, which counts only public, non-fork repositories the user
owns, is replaced with the number of repositories committed to from build_stats.py's stats.json. The stock
theme colors and font are replaced with scripts/palette.py's, so the cards match the rest of the profile.

Usage: python patch_summary_cards.py <card_output_dir> <stats.json>
"""
import json
import re
import sys
from pathlib import Path

from palette import FONT, PALETTES

PUBLIC_REPOS = re.compile(r">\d+ Public Repos?<")
FONT_RULE = re.compile(r"font-family:[^}]*")
# Output folder -> (palette, {stock theme color: palette key}).
THEMES = {
    "github": ("light", {"#e4e2e2": "border", "#0366d6": "accent", "#586069": "muted", "#40c463": "chart"}),
    "github_dark": ("dark", {"#2e343b": "border", "#0366d6": "accent", "#77909c": "muted", "#40c463": "chart"}),
}


def recolor(text, theme):
    name, mapping = THEMES[theme]
    for stock, key in mapping.items():
        text, n = re.subn(re.escape(stock), PALETTES[name][key], text, flags=re.IGNORECASE)
        # Every card draws a border and a title, so a missing stock color means the theme changed upstream.
        if n == 0 and key in ("border", "accent"):
            raise ValueError(f"stock color {stock} not found")
    text, n = FONT_RULE.subn(f"font-family: {FONT}\n        ", text, count=1)
    if n != 1:
        raise ValueError("font rule not found")
    return text


out, stats = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
cards = sorted(card for theme in THEMES for card in (out / theme).glob("*.svg"))
if not cards:
    sys.exit(f"{out}: no cards found")
failed = False
for card in cards:
    text = card.read_text(encoding="utf-8")
    try:
        if card.name == "0-profile-details.svg":
            text, n = PUBLIC_REPOS.subn(f">Committed to {stats['repositories']} Repos<", text)
            # Cards are regenerated on every run, so a missing line means the card's markup changed upstream.
            if n != 1:
                raise ValueError(f"expected 1 Public Repos line, found {n}")
        text = recolor(text, card.parent.name)
    except ValueError as e:
        print(f"{card}: {e}", file=sys.stderr)
        failed = True
        continue
    card.write_text(text, encoding="utf-8", newline="\n")
sys.exit(1 if failed else 0)
