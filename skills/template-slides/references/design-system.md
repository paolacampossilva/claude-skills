# Design system — template-slides

Canvas: 13.33" × 7.5" (`pptxgenjs` `LAYOUT_WIDE`). Font throughout: **Calibri**.

## Palette (semantic names → hex, no `#` in pptxgenjs)

| Token | Hex | Used for |
|---|---|---|
| `navy` | `073B4C` | Titles, "Resultado" callout fill, closing/cover background |
| `teal` | `008DB8` | Primary accent, blue-family icons/borders |
| `teal-light` | `1F9AC0` | Decorative cover circle |
| `teal-dark` | `006D91` | Cover eyebrow text ("Sprint N") |
| `green` | `00B52B` | Green-family icons |
| `yellow` | `FFD119` | Yellow-family icons, cover accent stripe, "Resultado" heading text |
| `blue-bright` | `2448FF` | Cover accent stripe (third stripe) |
| `red` | `CC0000` | Red-family icons (detailed cards) |
| `red-light` | `E71D36` | Red-family icons (simple overview cards) |
| `gray-text` | `6A7580` | Subtitles, card body text |
| `bg-light` | `F4F8FA` | Cover right-panel background |
| `white` | `FFFFFF` | Card titles on tinted cards, body text on navy |

Card tint + border per color family (fill = card background, border = card
outline, use `line: {none: true}` if the card has no visible border):

| Family | Icon fill | Card fill | Card border |
|---|---|---|---|
| Blue | `008DB8` | `E7F5F8` | `008DB8` |
| Green | `00B52B` | `D9EAD3` | none |
| Yellow | `FFD119` | `FFF6CB` | `E5CF72` |
| Red | `CC0000` | `F4CCCC` | `E06666` |
| Neutral (overview cards) | family color | `FFFFFF` | `D8E4EA` |

Connector lines between sequential cards (optional, only for process-flow
slides): color `A2C4C9`, hairline weight.

Pick **one family per slide** (or per logical group within a slide, as in
the overview slide) based on the semantic meaning: blue = default/process
step, green = success/completion, yellow = attention/rule, red = risk/error.
Don't mix families arbitrarily — they signal meaning across the deck.

## Typography scale

| Role | Size | Weight | Color |
|---|---|---|---|
| Cover title | 31pt | bold | `navy` |
| Cover eyebrow ("Sprint N") | 17pt | bold | `teal-dark` |
| Cover team label | 20pt | regular | `navy` |
| Cover description | 12.5pt | regular | `gray-text` |
| Slide title | 30.5pt | bold | `navy` |
| Slide subtitle (one line, under title) | 17.5pt | regular | `gray-text` |
| Card number (inside icon circle) | 13.5pt | bold | `white` |
| Card title | 14.5pt | bold | `navy` |
| Card body | 12.5pt | regular | `gray-text` |
| "Resultado" heading | 16.5pt | bold | `yellow` |
| "Resultado" body | 16pt | regular | `white` |
| Closing slide title | ~24pt | bold | `white` |
| Closing slide body (names, team line) | 14–16pt | regular/bold | `white` |

## Slide types

### 1. Cover — layout fixed, only 3 text fields vary per deck

Only "Sprint N", the title, and the description paragraph ever change
between decks. Everything else below — positions, sizes, logos, stripes,
the decorative circle — is copied verbatim every time, never resized or
repositioned to accommodate a particular title. If a title doesn't fit the
fixed title box on 2 lines, shorten the title text instead of changing the
box.

- Left panel: rect `x:0 y:0 w:5.25 h:7.5`, fill `teal`.
- Decorative circle behind the logo: ellipse `x:-0.9 y:-0.5 w:6.3 h:6.3`,
  fill `teal-light` (bleeds off the top-left edge; add it before the logo).
- The first logo (white version, provided by the user) centered on the teal
  panel, in the box `x:1.55 y:2.35 w:1.35 h:1.96`, aspect ratio kept.
- Three vertical accent stripes right of the panel, each full height
  (`h:7.5`): `x:5.25 w:0.17` fill `green`, `x:5.42 w:0.13` fill `yellow`,
  `x:5.55 w:0.15` fill `blue-bright`.
- Right content panel: rect `x:5.85 y:0 w:7.48 h:7.5`, fill `bg-light`.
- On the right panel: eyebrow "Sprint N" (`x:6.2 y:1.05`), title (`x:6.2
  y:1.5 w:6.5 h:1.6`, wraps to 2 lines), "<team label>" (`x:6.2 y:3.35`), one
  short description paragraph (`x:6.2 y:3.9 w:5.9 h:1.1`).
- Footer logos on the right panel (color versions, provided by the user), as
  boxes with the aspect ratio kept: second logo in `x:6.4 y:5.95 w:1.75
  h:0.4`, third in `x:10.1 y:5.75 w:2.0 h:0.83`.

### 2. Standard content slide (title + card grid + Resultado)

The workhorse slide — use for most technical/process content.

- Left-edge tricolor bar on every content slide (not the cover): three thin
  full-height vertical stripes at `x:0 w:0.23` fill `teal`, `x:0.23 w:0.1`
  fill `green`, `x:0.33 w:0.1` fill `yellow`.
- Title: `x:0.72 y:0.36 w:11.9 h:0.62`, slide-title style.
- Subtitle: `x:0.72 y:1.02 w:11.9 h:0.62`, one line, slide-subtitle style.
- Card grid: up to 3 columns × 2 rows, each card `w:3.41 h:1.61`, columns at
  `x: 0.72 / 4.87 / 9.08` (roughly, first row) and a slightly offset second
  row (`x: 0.72 / 4.93 / 9.14`), rows at `y: 1.7–1.9` and `y: 3.9–4.1` — copy
  the offsets loosely, exact alignment matters more than matching these to
  the decimal. Each card: colored rounded-rect background (card fill +
  border from the chosen family), a small circle (`0.34 × 0.34`, icon fill)
  in the top-left corner with the card number centered in it, the card title
  to the right of the circle, and 1–2 sentences of body text below,
  contained inside the card — keep body text short, it will overflow a card
  this size past ~120 characters.
- Optional thin connector lines (`A2C4C9`) between cards to suggest a
  sequence — skip these if the cards aren't strictly ordered steps.
- "Resultado" callout: navy rect pinned near the bottom, `x:0.75 y:5.88
  w:11.83 h:1.29`. Inside: "Resultado" heading (yellow, bold) then 1–2
  sentences of body text (white). Use this box for the takeaway/summary of
  the slide's content — every content slide should end with one.

### 3. Overview / objective slide (mini cards, no card fill tint)

Used for a slide that lists 3–4 short objectives/goals side by side (e.g. the
sprint objectives).

- Same title/subtitle/left-bar treatment as the standard content slide.
- Cards: single row, `w` ≈ 2.9", white fill, neutral border `D8E4EA`, no
  card-family tint. Icon circle top-left in the family color that matches
  each item's meaning (can differ per card in this slide type, unlike the
  standard content slide). Card title bold navy, short body gray.

### 4. Process / relationship diagram slide

Used to show how 2–4 modules or services connect (e.g. how three
modules relate). Boxes (one per module, family-tinted per the
same rules) connected by thin arrows/lines showing data or call direction.
Label each connection briefly. Keep to a simple left-to-right or hub-and-
spoke layout — don't try to fit more than 4–5 boxes on one diagram.

### 5. Column / table slide

Used for side-by-side categorized lists (e.g. where the
work fits in the existing processes) — a row of column headers, each with
a short label and one sentence of body text underneath, all in one family
color, plus an optional summary line at the bottom (not necessarily the
full navy Resultado box — a lighter one-line note works here).

### 6. Closing / "Agradecimentos" slide — fixed, reproduced exactly every time

Unlike every other slide type, this one is never redesigned per deck —
content doesn't vary with the sprint at all (only the team info does, which is
the same for every deck of one team). Exact spec of the reference design:

- Full-slide navy (`073B4C`) background; left tricolor bar `0.16/0.12/0.14`
  wide, teal/green/yellow (narrower than the `0.23/0.10/0.10` bar used on
  content slides — this slide's bar is its own width, don't reuse the
  content-slide constant here).
- Two decorative ellipses, fill `0C4A5C` (not a plain teal/navy mix — this
  specific value): `x:8.6 y:-2.6 w:6.6 h:6.6` and `x:-1.6 y:3.9 w:5.2 h:5.2`.
- Title "Agradecimentos": 36pt bold white, `x:1.06 y:1.09 w:8.0 h:0.70`.
- "Membros do time:": 19pt bold white, `x:1.15 y:2.22 w:6.0 h:0.35`.
- The team member names, one per line: 19pt regular, color `DCEAEF` (a pale
  blue-white, not pure `FFFFFF`), line spacing 1.35, `x:1.15 y:2.85 w:6.0
  h:1.70`.
- Team/orientação line at `x:1.15 y:4.95 w:10.5 h:0.40`, one paragraph with
  two runs: `"<team label> "` 18pt bold white, then `"— Orientação: <nomes>"`
  18pt regular color `DCEAEF`.
- Up to 3 footer logos, white versions on the navy background (a color logo
  is fine only if it reads on navy as-is), as boxes with the aspect ratio
  kept: `x:6.50 y:5.75 w:0.85 h:1.23`, `x:8.05 y:6.10 w:1.90 h:0.43` and
  `x:10.60 y:5.95 w:1.70 h:0.71`.
