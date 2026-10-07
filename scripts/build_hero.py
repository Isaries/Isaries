"""Render the animated terminal hero as assets/hero-dark.svg and assets/hero-light.svg.

Every line mirrors a verifiable fact about WISE-API PR #325; see docs/hero-animation.md
before changing the script text.
"""
from html import escape
from pathlib import Path

# Muted (Morandi) hues to match scripts/palette.py, keeping each color's meaning: sage for success,
# dusty rose for the problem, mauve for the merge, ochre for the observation. Light-theme values keep
# at least 4.5:1 contrast on white.
THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#e6edf3", dim="#8b949e",
                 prompt="#8fa9c0", ok="#9bb59b", bad="#c99a95", merged="#ab9cc0", accent="#c9b48a",
                 dots=("#c48f8a", "#c9b48a", "#9bb59b")),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", text="#1f2328", dim="#59636e",
                  prompt="#4f6a82", ok="#5a7560", bad="#9c5f5a", merged="#6f5f88", accent="#7d6a43",
                  dots=("#c48f8a", "#c9b48a", "#9bb59b")),
}

# (kind, [(css_class, text), ...]); "cmd" lines are typed, others appear at once.
SCRIPT = [
    ("cmd", [("p", "$ "), ("t", "./mvnw package")]),
    ("out", [("ok", "  BUILD SUCCESS")]),
    ("gap", []),
    ("cmd", [("p", "$ "), ("t", "grep -n BatchStudentChangePassword pom.xml")]),
    ("out", [("d", "  159:  "), ("bad", "<exclude>**/…/BatchStudentChangePasswordControllerTest.java</exclude>")]),
    ("out", [("d", "  208:  "), ("bad", "<exclude>**/…/BatchStudentChangePasswordControllerTest.java</exclude>")]),
    ("out", [("d", "  # this controller's test is never compiled or run")]),
    ("gap", []),
    ("out", [("bad", "# meanwhile, a teacher could batch-reset passwords")]),
    ("out", [("bad", "# for a group in a run they did not own")]),
    ("gap", []),
    ("cmd", [("p", "$ "), ("t", "git apply re-check-run-ownership.patch")]),
    ("out", [("m", "  # PR #325, merged upstream")]),
    ("cmd", [("p", "$ "), ("t", "./mvnw package")]),
    ("out", [("ok", "  BUILD SUCCESS")]),
    ("gap", []),
    ("out", [("a", "# green before the fix. green after it.")]),
    ("out", [("q", "# which checks are actually protecting anything?")]),
]

W = 820
PAD_X = 24
BAR_H = 36
LINE_H = 22
FONT = 14
# Upper bound of monospace advance at 14px across common fonts, so the cover always clears the text.
CHAR_W = 8.6
TYPE_S = 0.035
PAUSE_S = 0.45
START_S = 0.6


def render(c):
    y0 = BAR_H + 30
    h = y0 + LINE_H * (len(SCRIPT) - 1) + 28
    t = START_S
    body, anims = [], []
    for i, (kind, spans) in enumerate(SCRIPT):
        y = y0 + i * LINE_H
        if kind == "gap":
            t += 0.15
            continue
        tspans = "".join(f'<tspan class="{cls}">{escape(s)}</tspan>' for cls, s in spans)
        if kind == "cmd":
            chars = len(spans[1][1])
            dur = chars * TYPE_S
            prompt_w = len(spans[0][1]) * CHAR_W
            body.append(f'<text x="{PAD_X}" y="{y}" class="o" style="animation-delay:{t:.2f}s">{tspans}</text>')
            body.append(
                f'<rect class="cover" x="{PAD_X + prompt_w:.1f}" y="{y - FONT}" width="{W}" height="{LINE_H}" '
                f'style="animation:type{i} {dur:.2f}s steps({chars}) {t + 0.2:.2f}s both"/>'
            )
            anims.append(f"@keyframes type{i}{{to{{transform:translateX({chars * CHAR_W:.1f}px)}}}}")
            t += 0.2 + dur + PAUSE_S
        else:
            if i == len(SCRIPT) - 1:
                tspans += f' <tspan class="cursor" style="animation-delay:{t:.2f}s">█</tspan>'
            body.append(f'<text x="{PAD_X}" y="{y}" class="o" style="animation-delay:{t:.2f}s">{tspans}</text>')
            t += 0.12

    alt = ("Terminal: WISE-API builds successfully both before and after the PR #325 run-ownership fix, "
           "because the controller's test is excluded from the build. "
           "Which checks are actually protecting anything?")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-labelledby="t d">
<title id="t">Green before the fix, green after it</title>
<desc id="d">{escape(alt)}</desc>
<style>
text{{font:{FONT}px ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;white-space:pre}}
.p{{fill:{c["prompt"]}}} .t{{fill:{c["text"]}}} .d{{fill:{c["dim"]}}} .ok{{fill:{c["ok"]};font-weight:700}}
.bad{{fill:{c["bad"]}}} .m{{fill:{c["merged"]}}} .a{{fill:{c["accent"]}}} .q{{fill:{c["text"]};font-weight:700}}
.title{{fill:{c["dim"]};font-size:12px}}
.cover{{fill:{c["bg"]}}} .cursor{{fill:{c["prompt"]};animation:blink 1.1s step-end infinite}}
.o{{animation:show .01s both}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes blink{{50%{{fill-opacity:0}}}}
{chr(10).join(anims)}
@media (prefers-reduced-motion:reduce){{.o,.cursor{{animation:none!important}}.cover{{display:none}}}}
</style>
<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="10" fill="{c["bg"]}" stroke="{c["border"]}"/>
<path d="M.5 10.5a10 10 0 0 1 10-10h{W - 21}a10 10 0 0 1 10 10v{BAR_H - 10}h-{W - 1}z" fill="{c["bar"]}"/>
<line x1=".5" y1="{BAR_H + .5}" x2="{W - .5}" y2="{BAR_H + .5}" stroke="{c["border"]}"/>
{"".join(f'<circle cx="{20 + 20 * i}" cy="18" r="6" fill="{dot}"/>' for i, dot in enumerate(c["dots"]))}
<text x="{W / 2}" y="22" text-anchor="middle" class="title">~/WISE-API   (upstream, UC Berkeley)</text>
<clipPath id="c"><rect x="1" y="{BAR_H + 1}" width="{W - 2}" height="{h - BAR_H - 2}"/></clipPath>
<g clip-path="url(#c)">
{chr(10).join(body)}
</g>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name, colors in THEMES.items():
        (out / f"hero-{name}.svg").write_text(render(colors), encoding="utf-8", newline="\n")
