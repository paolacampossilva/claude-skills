---
name: colorful-summary-pdf
description: Build a vivid, magazine-style PDF from study notes, slides, or any long reference material — a color-coded cover with a mini table of contents, one accent color per section/chapter, numbered circular badges, definition callout boxes, chip tags, styled tables, and numbered-step lists. Use this whenever the user asks for a "colorful", "pretty", "bonito e colorido", "styled", or "visual" PDF summary/study guide/report — not just any PDF export. Also use it proactively when the user asks to summarize slides, lecture notes, or a long document into a PDF they can study from, even if they don't specify styling, since a plain PDF is rarely what "make me a summary PDF" implies for study material. For math-heavy material it also typesets formulas as LaTeX with a legend for every term (see "Formulas"). Do not use this for PDFs the user explicitly wants plain/minimal, or for filling/editing existing PDF forms (use the general pdf skill for that).
---

# Colorful Summary PDF

Turns a set of topics/sections (lecture slides, notes, a long report) into a
single, good-looking PDF: a cover page with a colored index, and one section
per topic with a distinct accent color, using WeasyPrint to render styled
HTML/CSS.

The result looks like a well-designed study guide or brand report, not a
default markdown-to-PDF export — colored numbered badges per section, tinted
callout boxes for definitions, colored chip tags, styled tables, and
circular numbered step lists.

## When to use this

- The user explicitly asks for a colorful / pretty / styled / visual PDF.
- The user asks to turn slides, notes, or a document into a study-guide PDF,
  a summary PDF, or a report — even without mentioning style, since a bare
  PDF undersells what they're asking for. In that case, use this skill by
  default and mention you made it visual; offer to make a plainer version if
  they'd prefer.
- Works for any number of sections (tested from ~3 to ~15). Below 3 sections
  the color-coded index loses its point — for a single-topic document, still
  use the visual language (callouts, chips, tables) but skip the multi-color
  cover legend.

- The material contains formulas: use the formula-card pattern in the "Formulas" section
  (typeset equations + a legend saying what each term is and what it is for +
  context). Never write formulas as plain Unicode text with `<sub>`/pipes — that
  is what looked bad.

Not a fit for: filling an existing PDF form, merging/splitting PDFs, or a
document the user wants minimal/plain (use the general `pdf` skill instead).

## Workflow

### 1. Gather and outline the content first

Read/extract the source material (slides, notes, documents) completely
before designing anything — see the `pdf-reading` or `file-reading` skills
if the source isn't already in context. Then outline it into a numbered list
of sections/topics with a short title each. This section count drives the
palette in step 2.

### 2. Generate the color palette

```bash
python3 scripts/palette.py <section_count>
```

This prints, per section: `<index> <accent_hex> <tint_hex> <tint2_hex>`, plus
a ready-made `linear-gradient(...)` line for the cover's color rule. Defaults
(hue spacing from 5°, 55% saturation, 40% lightness) give a muted
rainbow progression that reads as an ordered sequence — adjust `--start-hue`,
`--sat`, `--light` only if the defaults clash with the subject matter (e.g.
a brand with a fixed hue to avoid).

### 3. Make sure fonts are installed

The design uses **Inter** (body/UI) and **Roboto Slab** (headings). Check
first with `fc-list | grep -iE "inter|roboto slab"`; if missing:

```bash
apt-get install -y fonts-inter fonts-roboto-slab
```

If the user's content is in a non-Latin script, swap in an appropriate Noto
font instead and update the `font-family` declarations in `style.css`.

### 4. Check WeasyPrint is available

```bash
pip show weasyprint || pip install weasyprint --break-system-packages
```

### 5. Build the HTML

Copy `assets/style.css` and `assets/template.html` into a working directory.
`style.css` is generic and rarely needs structural changes. `template.html`
has a cover skeleton and one fully-annotated example `<section class="topic">`
to duplicate per topic. For each section:

- Set the inline `style="--c:#..; --tint:#..; --tint2:#.."` on the `<section>`
  wrapper using that section's row from `palette.py`'s output.
- Set the matching `--c` on that section's `<span class="toc-num">` in the cover.
- Set `--rule-gradient` on `.toc-rule` to the gradient line `palette.py` printed.
- Fill in the `topic-num` digit (inside the `topic-num-cell` wrapper — keep
  both divs, they exist so the badge and the title reliably move together
  across a page break instead of splitting), the `kicker` (small label above
  the title), and the title.
- Write the content using the available components (see below) — use only
  what fits; most sections won't need all of them.
- **Every `<table>` must split its header into `<thead>` and the rest into
  `<tbody>`** (see `template.html`). Without this, a table taller than one
  page gets forced whole onto the next page by the page-break rules,
  stranding a near-empty page behind it; with `<thead>`/`<tbody>`, it breaks
  cleanly between rows instead, repeating the header.
- Two small CSS placeholders need real values once per document: the
  `@bottom-center` footer text at the top of `style.css`, and the
  `--rule-gradient` fallback (already overridden inline per the point above).

**Content components available in `style.css`** (see `template.html` for markup):
| Component | Class | Use for |
|---|---|---|
| Callout box | `.callout` (with `.label` inside) | A definition, key fact, or a "must-remember" point. 1-3 per section. |
| Chip tags | `.chip-row` > `.chip` | A short flat set of related terms with no further explanation needed. |
| Table | `<table>` with `<thead>`/`<tbody>` (always split this way — see note below) | Any side-by-side comparison or structured reference data. |
| Numbered steps | `ol.steps` | A sequential process/procedure (each `<li>` gets an auto-numbered circular badge in the accent color). |
| Two-column list | `ol.two-col` / `ul.two-col` | A longer flat list (8+ short items) that would look sparse as a single column. |
| Subheadings | `h2.sub`, `h3.sub3` | Break up a section into labeled sub-topics. |
| Formula card | `.fcard` (needs `math.css` + `mathify.py`) | One formula (or a few related ones) with context and a term-by-term legend. See "Formulas". |
| Process flow | `.fc-flow` inside an `.fcard` | A short pipeline of boxes and arrows (A → B → C). |
| Formula cheat sheet | `.cola` > `.ci` | A one-page, formulas-only grid meant to be copied by hand. |

Write the actual content in whatever language the user has been
communicating in / the source material uses — the design system itself is
language-agnostic.

### 6. Render to PDF

If the HTML contains math (`$...$` / `$$...$$`), typeset it first — see "Formulas":

```bash
python3 scripts/mathify.py index.html index_math.html   # writes fx/*.svg next to the html
```

```python
from weasyprint import HTML
HTML("index_math.html", base_url=".").write_pdf("output.pdf")   # index.html if there is no math
```

### 7. Visually check before delivering — this step is not optional

Rasterize every page and actually look at each one:

```bash
pdftoppm -png -r 100 output.pdf page
```

Then view each `page-NN.png`. Specifically check for:
- **Text clipping/overlap** — most common on the cover, where the color rule
  or long titles can collide with text if margins are off.
- **Nearly-empty pages** — a page that's mostly whitespace almost always
  means a block got pushed whole to the next page. `.callout`/`.steps`/
  `ol.two-col` use `break-inside: avoid-page` to stay together, and headings
  use `break-after: avoid-page` — tables deliberately do NOT avoid breaking
  (they split between rows instead, see the `<thead>`/`<tbody>` note above),
  since a table is often the biggest single block in a section and forcing
  it whole onto one page is what causes this exact problem. Check anyway —
  if you see a page more than ~60% empty with content continuing on the
  next page, tighten spacing or move a callout so it starts earlier.
- **Truncated numbers/labels** — e.g. two-digit numbers clipped in a
  fixed-width badge; widen the element if so.
- **Formulas** (when present): every formula image actually appears (no blank gaps
  where an image failed to load); inline symbols in legends sit on the text
  baseline and look the same size as the text; no display formula is wider than
  its card; a card's title, formulas and context are not separated by a page
  break; no accented characters were pasted inside TeX (they break the build).
- **Color contrast** — chip/table-header text must stay legible (white on
  the accent color); if a generated accent color is too light, nudge
  `--light` down a few points in `palette.py` and regenerate.

Only present the PDF to the user after this check.

### 8. Deliver

Save to the outputs directory and present the file. Briefly describe the
color-coding choice made (e.g. "each topic gets its own color, matching the
legend on the cover") — don't narrate the whole build process.

## Formulas: typeset equations with a legend for every term

WeasyPrint cannot render MathML/MathJax, and formulas typed as Unicode text
(`θ<sub>j</sub>`, `∂L/∂w`, pipes between formulas) look cramped and amateur.
The fix used here: write real LaTeX in the HTML, convert each formula to a
vector SVG (LaTeX Computer Modern quality), and place it as an `<img>` sized in
pt and aligned to the text baseline. Use it whenever the material has more than
a trivial formula or two.

### Setup (once per environment)

```bash
which pdflatex pdftocairo && kpsewhich standalone.cls   # all three must print a path
# if missing:
apt-get install -y texlive-latex-base texlive-latex-extra poppler-utils
```

If LaTeX cannot be installed, `mathify.py` falls back automatically to
matplotlib's mathtext (fractions, sums, Greek, hats, sub/superscripts work;
`cases`, `underbrace`, `aligned` do not and raise a clear error — rewrite those
as separate lines or plain HTML). The fallback draws fractions smaller (no
display style), so prefer LaTeX for formula-heavy documents.

Files for this feature: `scripts/mathify.py` (converter), `assets/math.css`
(card styles; copy it next to `style.css` and link it after it, or concatenate
the two files) and `assets/formula-example.html` (markup to copy from).

### Writing the math

- Inline: `$\hat{y}=\sigma(z)$`. Display: `$$\frac{\partial L}{\partial w}=-2\,(y-\hat{y})\,x$$`.
  Do not use a literal `$` anywhere else in the document.
- Put several related formulas of a card in **separate `$$…$$` inside the same
  `<div class="fc-eq">`**; they sit side by side and wrap to a new line, which
  keeps each image narrow. `mathify.py` warns when one is wider than ~430pt.
- **No accented characters inside TeX or `\text{}`** (the default pdflatex setup
  has no utf8/T1 fonts and fails). Use ASCII words inside formulas
  (`\text{error}`) and put accented text in the surrounding HTML (for example a
  `<div class="cn">` line in the cheat sheet).
- Decimal comma: `0{,}5`. `<` and `&` (e.g. in `cases`) can be written as-is:
  the conversion runs on the raw source before the HTML is parsed.
- Use `\dfrac` for a big fraction inside inline math in legends; `\bigl( \bigr)`
  or `\Bigl[ \Bigr]` around tall subexpressions; `\underbrace{…}_{\text{x}}` to
  label the factors of a chain rule (keep the labels short so they do not touch).
- Sizes are set by `--display-scale` (default 1.12 ≈ 13.4pt) and
  `--inline-scale` (default 1.15 ≈ 11.5pt, matched to Inter body text); change
  them only if the body font size in `style.css` changes.

### The formula card (the pattern to reuse)

Every important formula gets a card with four parts (see `assets/formula-example.html`):

1. **Title** (`.fc-title`): the name of the formula. If the document tags sources
   (teacher / notes / textbook / general knowledge), put the tags here.
2. **Formula** (`.fc-eq`): one or more `$$…$$`. Group the definition, the
   derivative and the update rule of the same idea in the same card (one
   `.fc-eq` row each).
3. **Context** (`p.fc-ctx`): *when and why it is used*, the intuition in plain
   words, common mistakes, and the relation to neighboring formulas (which one
   it is derived from, which one it feeds). Give a tiny numeric illustration only
   if it clarifies a term; do not turn it into a solved exercise.
4. **Legend** (`table.fc-legend`, columns **Term | What it is | What it is for**,
   written in the document's language): one row per symbol, with the symbol
   typeset as inline math (`$\hat{y}$`) so it matches the formula exactly.
   "What it is" names the object (prediction, weight, learning rate…);
   "What it is for" says why it is there or what it controls (e.g. "too small:
   slow; too large: oscillates"). Include the non-obvious operators too
   (squared error, summation, threshold) — that is where students get lost.

Optional extras: a small comparison table in place of the legend (e.g. activation
functions × range × derivative × typical use); a `.fc-flow` pipeline instead of a
formula; a closing `p.fc-ctx` for a variant from another source.

### Organizing many formulas

- One `h2.sub` per topic block; give the block its own accent by setting
  `--c` (and `--tint`) inline on the `h2` and on that block's `.fcard`s, using the
  same colors as the section of that topic elsewhere in the document.
- End with a **one-page cheat sheet** (`.cola`, `break-before: page` on its
  heading): only formulas, two columns, each in a `.ci` tile with a `.ct` label.
  Useful when the student may copy formulas by hand (open-formula exams).
- Cards may split between legend rows (CSS repeats the header); the CSS keeps the
  title, the formula rows and the start of the context together, so a card never
  starts with a stranded title or a formula alone at the bottom of a page.

### Build order

1. Write the HTML with `$…$` / `$$…$$` and `.fcard` markup, linking `style.css` and `math.css`.
2. `python3 scripts/mathify.py index.html index_math.html` (the `fx/` cache folder
   is created next to it; identical formulas are compiled once, so rebuilds are fast).
3. WeasyPrint on `index_math.html` with `base_url="."`. Keep `fx/` beside the HTML.
4. Rasterize and look at every page (step 7). If a formula fails to compile, the
   error prints the offending TeX; fix that formula and rerun.

## Design rationale (for when the user wants tweaks)

- **Palette**: evenly-spaced hues at fixed, moderate saturation/lightness so
  every section is distinguishable without looking like a neon UI kit or a
  generic SaaS gradient. The cover's vertical rule doubles as a color legend.
  If the user wants a different mood (e.g. monochrome + one accent, a
  specific brand palette), replace `scripts/palette.py`'s output with hand-
  picked values instead — the rest of the CSS only cares about the three
  variables per section (`--c`, `--tint`, `--tint2`).
- **Numbered circular badges**: appropriate because the content generally
  *is* a sequence (chapters/topics in order). Don't force numbering onto
  content that isn't actually sequential — drop `.topic-num` for an
  unordered set of topics.
- **Typefaces**: Roboto Slab for headings gives a warm, book-like editorial
  feel distinct from the generic sans-only default; Inter for body/UI text
  because it stays highly legible at small sizes (chips, table cells,
  footer). Swap both together if the subject calls for a different voice
  (e.g. a more technical/startup feel) — keep one serif/slab for headings
  and one clean sans for body rather than mixing more than two families.
- **Continuous flow, not one-page-per-topic**: sections are *not* forced
  onto their own page (no `break-before: page` on `.topic`). Forcing new
  pages reliably strands half-empty pages when a topic runs slightly over
  or under a page boundary. Letting topics flow and only keeping headings
  glued to their first bit of content (`break-after: avoid-page`) uses the
  paper efficiently while still keeping each section visually anchored by
  its colored header.
