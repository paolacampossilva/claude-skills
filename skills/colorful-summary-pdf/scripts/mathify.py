"""Typeset math for colorful-summary-pdf documents (WeasyPrint has no math support).

Write formulas directly in the HTML source:

    inline   ->  $\\hat{y}=\\sigma(z)$
    display  ->  $$\\frac{\\partial L}{\\partial w}=-2\\,(y-\\hat{y})\\,x$$

Run this script BEFORE WeasyPrint. Every formula is replaced by an <img> that
points to a vector SVG (rendered with LaTeX by default), with an explicit width
in pt and, for inline math, a vertical-align that puts the formula on the text
baseline. Identical formulas are compiled once and cached in the fx/ folder.

Usage:
    python3 mathify.py in.html out.html [--fx-dir fx] [--display-scale 1.12]
                       [--inline-scale 1.15] [--engine auto|latex|mpl]
                       [--max-width 430]

Or from Python:
    from mathify import mathify
    html_out = mathify(html_in, display_scale=1.12, inline_scale=1.15)

Keep the output HTML and the fx/ folder in the same directory (the <img src>
paths are relative), and render with HTML("out.html", base_url=".").

Engines
- latex (default when available): pdflatex + the `standalone` class + pdftocairo.
  Full TeX Computer Modern quality; supports amsmath (cases, underbrace, dfrac,
  \\text, \\lVert ...). Needs: texlive-latex-base, texlive-latex-extra (for
  standalone.cls), poppler-utils.
- mpl (automatic fallback when LaTeX is missing): matplotlib mathtext. Handles
  fractions, sums, Greek, hats, sub/superscripts, \\sqrt, \\partial ..., but NOT
  cases/underbrace/aligned. A few commands are translated (\\dfrac, \\bigl, \\text,
  \\lVert ...); anything else unsupported raises an error naming the formula.

Rules for the TeX you write (they come from real failures):
- Do not use accented characters inside math or \\text{...}: the default
  pdflatex setup here has no T1/utf8 fonts. Put words with accents in the HTML
  text next to the formula instead of inside it.
- Use plain ASCII only inside $...$; write "<" and "&" as-is (the conversion runs
  on the raw source before the HTML is parsed, so no HTML escaping is needed).
- Decimal comma in Portuguese: write 0{,}5 so TeX does not add a space.
- Do not use any other "$" in the document text.
"""

import argparse
import hashlib
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor

_MPL_LOCK = threading.Lock()   # matplotlib's mathtext parser is not thread-safe

TEX_TEMPLATE = r"""\documentclass[%(size)spt,border=%(border)spt]{standalone}
\usepackage{amsmath,amssymb}
\newwrite\dpf
\begin{document}%%
\setbox0=\hbox{$%(disp)s%(tex)s$}%%
\immediate\openout\dpf=\jobname.dp%%
\immediate\write\dpf{\the\dp0}%%
\immediate\closeout\dpf%%
\box0%%
\end{document}
"""


def have_latex() -> bool:
    """True when pdflatex, pdftocairo and standalone.cls are all available."""
    if not (shutil.which("pdflatex") and shutil.which("pdftocairo")):
        return False
    if shutil.which("kpsewhich"):
        r = subprocess.run(["kpsewhich", "standalone.cls"], capture_output=True, text=True)
        return bool(r.stdout.strip())
    return True


def _key(tex: str, display: bool, engine: str) -> str:
    return hashlib.md5(f"v3|{engine}|{int(display)}|{tex}".encode()).hexdigest()[:14]


def _compile_latex(tex: str, display: bool, fx_dir: str, key: str) -> dict:
    size = 12 if display else 10
    border = 1.0 if display else 0.25   # inline formulas: tight border so no extra space around them
    disp = r"\displaystyle " if display else ""
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, "f.tex")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(TEX_TEMPLATE % dict(size=size, border=border, disp=disp, tex=tex))
        r = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", d, src],
            capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(os.path.join(d, "f.pdf")):
            raise RuntimeError(f"LaTeX failed for formula: {tex!r}\n{r.stdout[-700:]}")
        svg = os.path.join(fx_dir, f"{key}.svg")
        subprocess.run(["pdftocairo", "-svg", os.path.join(d, "f.pdf"), svg], check=True)
        head = open(svg, encoding="utf-8").read(600)
        w = float(re.search(r'width="([\d.]+)"', head).group(1))
        h = float(re.search(r'height="([\d.]+)"', head).group(1))
        dp = float(open(os.path.join(d, "f.dp")).read().strip().replace("pt", ""))
    return dict(w=w, h=h, dp=dp + border)  # + the standalone border


_MPL_SUBS = [
    (r"\\displaystyle", ""), (r"\\dfrac", r"\\frac"), (r"\\tfrac", r"\\frac"),
    (r"\\(?:bigl|bigr|Bigl|Bigr|biggl|biggr|Big|big)\b", ""),
    (r"\\left\s*\\lVert|\\right\s*\\rVert", r"\\Vert"), (r"\\lVert|\\rVert", r"\\Vert"),
    (r"\\lvert|\\rvert", "|"), (r"\\text\{", r"\\mathrm{"), (r"\\;", r"\\ "), (r"\\qquad", r"\\quad\\quad"),
]


def _compile_mpl(tex: str, display: bool, fx_dir: str, key: str) -> dict:
    with _MPL_LOCK:
        return _compile_mpl_locked(tex, display, fx_dir, key)


def _compile_mpl_locked(tex: str, display: bool, fx_dir: str, key: str) -> dict:
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib.figure import Figure
    from matplotlib.font_manager import FontProperties
    from matplotlib.mathtext import MathTextParser

    for bad in (r"\begin{cases}", r"\underbrace", r"\begin{aligned}", r"\overbrace"):
        if bad in tex:
            raise RuntimeError(f"{bad} needs the LaTeX engine (mathtext cannot render it): {tex!r}")
    t = tex
    for pat, rep in _MPL_SUBS:
        t = re.sub(pat, rep, t)
    s = f"${t}$"
    size = 12 if display else 10
    prop = FontProperties(size=size)
    res = MathTextParser("path").parse(s, 72, prop)
    depth = res.depth if hasattr(res, "depth") else res[2]   # namedtuple (new) or tuple (old matplotlib)
    fig = Figure()
    fig.patch.set_alpha(0)
    fig.text(0, 0, s, fontsize=size)
    svg = os.path.join(fx_dir, f"{key}.svg")
    fig.savefig(svg, format="svg", bbox_inches="tight", pad_inches=1 / 72, transparent=True)
    head = open(svg, encoding="utf-8").read(800)
    w = float(re.search(r'width="([\d.]+)pt"', head).group(1))
    h = float(re.search(r'height="([\d.]+)pt"', head).group(1))
    return dict(w=w, h=h, dp=depth + 1.0)


def _compile(tex: str, display: bool, fx_dir: str, engine: str) -> tuple:
    key = _key(tex, display, engine)
    meta_path = os.path.join(fx_dir, f"{key}.json")
    if os.path.exists(meta_path):
        return key, json.load(open(meta_path))
    fn = _compile_latex if engine == "latex" else _compile_mpl
    try:
        meta = fn(tex, display, fx_dir, key)
    except ValueError as e:   # matplotlib mathtext parse error
        raise RuntimeError(f"mathtext could not parse formula: {tex!r}\n{str(e).strip()[-300:]}") from None
    json.dump(meta, open(meta_path, "w"))
    return key, meta


def mathify(text: str, fx_dir: str = "fx", display_scale: float = 1.12, inline_scale: float = 1.15,
            engine: str = "auto", max_width: float = 430.0) -> str:
    """Replace $$...$$ and $...$ in `text` with <img> tags pointing to SVGs in fx_dir."""
    if engine == "auto":
        engine = "latex" if have_latex() else "mpl"
        print(f"[mathify] engine: {engine}", file=sys.stderr)
    os.makedirs(fx_dir, exist_ok=True)

    jobs = []
    for m in re.finditer(r"\$\$(.+?)\$\$", text, flags=re.S):
        jobs.append((htmllib.unescape(m.group(1)).strip(), True))
    rest = re.sub(r"\$\$(.+?)\$\$", "", text, flags=re.S)
    for m in re.finditer(r"\$(.+?)\$", rest, flags=re.S):
        jobs.append((htmllib.unescape(m.group(1)).strip(), False))
    uniq = list(dict.fromkeys(jobs))
    with ThreadPoolExecutor(max_workers=6) as ex:
        results = dict(zip(uniq, ex.map(lambda j: _compile(j[0], j[1], fx_dir, engine), uniq)))

    def display(m):
        tex = htmllib.unescape(m.group(1)).strip()
        key, meta = results[(tex, True)]
        w = meta["w"] * display_scale
        if w > max_width:
            print(f"[mathify] WARNING: display formula is {w:.0f}pt wide (> {max_width:.0f}pt); "
                  f"split it into several $$..$$ inside the same .fc-eq: {tex[:70]!r}", file=sys.stderr)
        return f'<img class="fx" src="{fx_dir}/{key}.svg" style="width:{w:.1f}pt" alt="">'

    def inline(m):
        tex = htmllib.unescape(m.group(1)).strip()
        key, meta = results[(tex, False)]
        w = meta["w"] * inline_scale
        va = meta["dp"] * inline_scale
        return (f'<img class="mi" src="{fx_dir}/{key}.svg" '
                f'style="width:{w:.1f}pt; vertical-align:-{va:.2f}pt" alt="">')

    text = re.sub(r"\$\$(.+?)\$\$", display, text, flags=re.S)
    return re.sub(r"\$(.+?)\$", inline, text, flags=re.S)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--fx-dir", default="fx")
    ap.add_argument("--display-scale", type=float, default=1.12)
    ap.add_argument("--inline-scale", type=float, default=1.15)
    ap.add_argument("--engine", choices=["auto", "latex", "mpl"], default="auto")
    ap.add_argument("--max-width", type=float, default=430.0)
    a = ap.parse_args()
    out = mathify(open(a.src, encoding="utf-8").read(), a.fx_dir, a.display_scale,
                  a.inline_scale, a.engine, a.max_width)
    open(a.dst, "w", encoding="utf-8").write(out)
    print(f"[mathify] wrote {a.dst}", file=sys.stderr)


if __name__ == "__main__":
    main()
