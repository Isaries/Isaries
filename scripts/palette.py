"""GitHub Primer colors shared by every generated image, so the cards and the 3D graph sit on the page's
own background instead of each tool's stock theme. assets/hero-*.svg use the same values.
"""
FONT = '-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans",Helvetica,Arial,sans-serif'

# chart: card bars and areas and the radar. levels: top faces of the 3D graph's cubes, from no
# contributions to the most. Both are a desaturated (Morandi) slate blue; the README's badges and banner
# use the same hues.
# Categorical colors for ranked series such as the language card, assigned by rank rather than by name.
# Muted enough to sit with the slate blue above, distinct enough to tell apart; the last is for "Other".
SERIES = ("#7d98b0", "#8fa58f", "#c2ae85", "#b7948f", "#9d8fb0", "#8aa6a8")
SERIES_OTHER = "#8f8b87"

PALETTES = {
    "dark": dict(bg="#0d1117", border="#30363d", fg="#e6edf3", muted="#8b949e", accent="#58a6ff",
                 chart="#7d98b0", levels=("#2d333b", "#3a4a5c", "#56708a", "#7d98b0", "#a9bfd0")),
    "light": dict(bg="#ffffff", border="#d0d7de", fg="#1f2328", muted="#59636e", accent="#0969da",
                  chart="#6f8aa0", levels=("#eef0f2", "#c9d4dd", "#9fb1c1", "#6f8aa0", "#4a6378")),
}
