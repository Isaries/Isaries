"""GitHub Primer colors shared by every generated image, so the cards and the 3D graph sit on the page's
own background instead of each tool's stock theme. assets/hero-*.svg use the same values.
"""
FONT = '-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif'
# Matches the green of the summary cards' charts, which the card action does not let us change.
GREEN = "#40c463"

PALETTES = {
    "dark": dict(bg="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e", accent="#58a6ff"),
    "light": dict(bg="#ffffff", border="#d0d7de", fg="#1f2328", muted="#59636e", accent="#0969da"),
}
