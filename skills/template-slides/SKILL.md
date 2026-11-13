---
name: template-slides
description: >-
  [Used by ← sprint-slides] Generates a PowerPoint (.pptx) deck in the user's fixed
  team-presentation visual identity (navy-and-teal design system — card grids
  with numbered icons, color-coded sections, navy "Resultado" callouts) —
  the visual/generation engine only, turning finished slide content into a
  styled .pptx. The team name, members, advisors and logos are inputs; if
  missing, ask, never infer. Only use when the user explicitly invokes it by
  name (e.g. "usa o skill template-slides") or via an approved sprint-slides
  handoff — not just because they ask for slides or a presentation in
  general terms.
---

# Template Slides

Generates a full deck (.pptx) in the user's fixed visual identity. The design (palette,
typography, component layouts) is fixed; only the content changes per deck.

This skill only handles the visual side. Deciding *what* each slide should
say — especially turning project/sprint context into a talk for a
non-technical audience — is the `sprint-slides` skill's job. If the user is
working in a project with `sprint-slides` available and hasn't already
approved an outline, point them to that skill instead of interviewing them
for content yourself.

## When this applies

**Explicit invocation only** — same convention as the user's other skills.
Do not build a deck in this style just
because they ask for "slides" or a "presentation" in general — wait for them
to name this skill (or for `sprint-slides` to hand off approved content to
it).

## Team info and logos — inputs, ask if missing

The cover and the closing slide need these, and they are the same for every
deck of one team. If the user didn't give them (and a previous deck's build
script next to the target folder doesn't hold them), ask with
`AskUserQuestion`. **Never infer them from the folder, the git log or the
user's name.** Once given, reuse them for the later decks of the same
session without asking again.

- **Team label**, e.g. "Team A" (called `<team label>` below)
- **Members**, one name per line
- **Advisors** ("Orientação"), as written on the closing slide
- **Sprint number**, which changes every deck
- **Logos** (file paths provided by the user, never invented): up to three,
  each in a version for dark backgrounds (white) and, when needed, one for
  light backgrounds (color). The positions below are boxes: scale each logo
  to fit its box keeping the aspect ratio, never stretch it. No logos given
  means no logo elements, and the rest of the layout stays the same.

## Cover and closing slides are fixed — never redesigned

These two slides are **not** content slides to lay out per deck — they are
the one fixed frame around whatever content slides 2..N-1 turn out to be.

- **Cover**: layout, positions, logos, stripes, decorative circle — all
  fixed, copied verbatim every time. The only three things that ever change
  between decks are the sprint number ("Sprint N"), the title text, and the
  one-paragraph description. Never resize, reposition, or restyle any
  element of the cover to "fit" a particular deck's title — if a title is
  too long for the fixed title box, shorten the title text instead.
- **Closing ("Agradecimentos")**: reproduced **exactly** — same layout,
  same text content and structure (title, "Membros do time:", the 4 names,
  the team/orientação line, the footer logos), same exact typography.
  Never add a synthesis paragraph, "next steps," or any other content to
  this slide — it doesn't vary by sprint content at all, only by the team
  info above. Exact values of the reference design:
  - Title "Agradecimentos": 36pt bold white, at `x:1.06 y:1.09 w:8.0 h:0.70`.
  - "Membros do time:": 19pt bold white, at `x:1.15 y:2.22 w:6.0 h:0.35`.
  - The member names: 19pt regular, color `DCEAEF` (not pure white), line
    spacing 1.35, at `x:1.15 y:2.85 w:6.0 h:1.70`.
  - Team line at `x:1.15 y:4.95 w:10.5 h:0.40`, two runs in one paragraph:
    `"<team label> "` 18pt bold white, then `"— Orientação: <nomes>"` 18pt
    regular color `DCEAEF`.
  - Up to 3 footer logos, as boxes: first at `x:6.50 y:5.75 w:0.85 h:1.23`,
    second at `x:8.05 y:6.10 w:1.90 h:0.43`, third at
    `x:10.60 y:5.95 w:1.70 h:0.71`.
  - Background: navy `073B4C` full-slide rect, two decorative ellipses
    filled `0C4A5C` at `x:8.6 y:-2.6 w:6.6 h:6.6` and `x:-1.6 y:3.9 w:5.2
    h:5.2`, left tricolor bar `0.16/0.12/0.14` wide in teal/green/yellow.

## Before generating, get the content

This skill has no fixed slide count or fixed slots — content varies every
deck. Before writing anything, make sure you have:

- The sprint number (for the cover and closing slide) — the only piece of
  cover/closing metadata that changes between decks; the rest is the team
  info above
- What each slide should cover — topics, groupings, and enough detail to
  write titles/body text and callout ("Resultado") text
- Whether any slide involves porta/serviço numbers, module names, or other
  project-specific labels the user uses internally

If content is arriving as an approved outline from `sprint-slides`, treat
that outline as the source of truth for structure and wording — don't
re-interview the user for things the outline already answers. Otherwise, if
the user pasted sprint notes, a task `.md` file, or a rough outline, extract the structure from that. Ask only for what's genuinely
missing.

Preserve the outline's wording as typed into the deck — don't introduce an
em dash, a redundant "Objetivo N —"-style prefix, a named AI-tool example,
or a manual title line-break while transcribing it (see `sprint-slides`'s
"Copy style" section for the full, confirmed list of what the user doesn't
want). If you're drafting copy yourself because no outline was handed off,
those same rules apply to you directly.

## Design system reference

Read `references/design-system.md` before writing any slide code — it has
the full palette, typography scale, and the exact layout spec (positions,
sizes, colors) for every slide type: cover, standard content (title + card
grid + Resultado callout), overview/objective cards, process/diagram slides,
column-table slides, and the closing "Agradecimentos" slide.

Use the logo files the user provided as-is (don't redraw or recolor them):
the white version on dark backgrounds (cover's teal panel, closing slide's
navy background) and the color version on light ones (cover footer).

## How to build it

1. Read `references/design-system.md` in full.
2. Find and read the `pptx` skill's own SKILL.md for the `pptxgenjs`
   gotchas (`pres.layout` must be `LAYOUT_WIDE` — 13.33" × 7.5" — before
   adding slides; hex colors never take `#`; every `addText` needs
   `isTextBox: true`; etc.) and its QA/validation scripts. In this
   environment that's `/mnt/skills/public/pptx/SKILL.md`; in Claude Code,
   look for it wherever skills are installed for that project (e.g. a
   `pptx` skill under `.claude/skills/` or a user-level skills directory).
   **If it isn't installed anywhere** (checked and confirmed missing, not
   just "couldn't find it in 30 seconds"), fall back to `python-pptx`
   instead of asking the user to install something: it can reproduce every
   component in the design system (rounded rectangles need
   `MSO_SHAPE.ROUNDED_RECTANGLE` + `shape.adjustments[0] = <0.05–0.08>` —
   plain `RECTANGLE` silently ignores the adjustment, which is the exact bug
   that made an entire deck look square-cornered once; the fix used since is
   to make a shared `rect()` helper pick `ROUNDED_RECTANGLE` automatically
   whenever a radius is given, so no call site can forget it). Tell the user
   which path was used.
3. Write a fresh script for this deck's specific content, following the
   component specs in the design system reference. Pick the slide type per
   topic (standard content grid vs. overview vs. diagram vs. column-table)
   based on what fits the material — don't force every slide into the same
   layout. When a slide needs a grid of N same-size cards, derive every
   card's `x`/`y` from the column/row count and the slide's usable width
   (`0.72` to `12.62`) with one shared gap constant — never hand-copy
   another slide's column positions for a different column count (that
   produces cards bunched on one side with the rest of the slide blank,
   and/or a card grid whose last row touches the "Resultado" box with no
   gap — both real defects seen in practice, not hypothetical).
4. Run the pptx skill's `validate.py` against the output and fix anything
   it flags. If that script isn't available (e.g. on the `python-pptx`
   fallback path), at minimum run the two checks in "Verifying without a
   renderer" below.
5. Convert to images and visually check every slide — text overflow inside
   cards is the most common defect here, since card body text is fixed at a
   small size (12.5pt) and long sentences will overflow a 3.41" × 1.61" card.
   Shorten the text or split into more cards rather than shrinking the font
   further. If no renderer is available (see "Verifying without a
   renderer"), rely on that section's checks instead, and say so explicitly
   when delivering the deck.
6. Deliver the final `.pptx`: in this environment, copy it to
   `/mnt/user-data/outputs` and call `present_files`. In Claude Code, save
   it in the folder the user names (ask; suggest `slides/`, and create it if
   it doesn't exist) **and save the generation script right next to it** in the same folder,
   named
   `<same-basename>_build.<py|js>` (e.g. `Sprint6_Apresentacao.pptx` +
   `Sprint6_Apresentacao_build.py`). This is what makes "Ajustando um deck
   já gerado" below possible — without it, a future request to tweak the
   deck has no source to edit, only the rendered file. Have the script save
   next to itself (derive the output path from `__file__`/`import.meta.url`
   rather than hardcoding a session-specific scratch path), so re-running it
   later regenerates in place. Tell the user where both files landed.

## Ajustando um deck já gerado

The user may come back later pointing at an existing `.pptx` asking for
specific fixes ("aumenta a fonte desse card", "esse slide ficou colado na
caixa de baixo") rather than a new deck. Don't rebuild from scratch:

1. Look for a `<same-basename>_build.py` (or `.js`) next to the `.pptx`. If
   it exists, treat it as the source of truth — read it, make the targeted
   edit(s) the request actually asks for (don't redesign slides nobody
   mentioned), re-run it, and it regenerates the `.pptx` in place.
2. If no sibling script exists (an older deck, predating this convention, or
   the script was lost), reconstruct only what's needed by reading the
   `.pptx` directly with `python-pptx` (shape positions/sizes, run text,
   font sizes, colors) to find the specific element the feedback refers to,
   then either patch the deck directly via `python-pptx` or rebuild a
   `_build` script matching the current structure — whichever is less work
   for the size of the fix — and save that script alongside the `.pptx` from
   then on.
3. Always re-run "Verifying without a renderer" below after the edit, even
   for a change that looks purely cosmetic (e.g. a font-size bump can turn a
   previously-fine card into an overflowing one).
4. Re-send the updated `.pptx` (and mention what changed, slide by slide, so
   the user doesn't have to diff it).

## Verifying without a renderer

Neither LibreOffice/`soffice` nor PowerPoint may be available. `qlmanage -t`
on macOS (Keynote's QuickLook generator) renders **only the first slide** as
a thumbnail — useful as a smoke test that shared helpers (used by every
slide, including the cover) haven't regressed, but it says nothing about
slides 2+. In that situation, two checks catch the two defect classes that
actually occurred building these decks:

- **Text-overflow heuristic**: for every text box, estimate wrapped line
  count from `usable_width / (font_pt * (0.56 if bold else 0.5) / 72)` chars
  per line, and flag when the estimated wrapped height exceeds the box's
  declared height. Bold needs its own (wider) constant — reusing the
  regular-weight constant under-counts wrapping on bold titles specifically.
- **Geometric collision check** (exact, not a heuristic): for every
  card-grid slide, confirm `max(card_bottom for card in slide) + margin ≤
  resultado_box_top`. This is what catches cards visually "glued" to the
  Resultado callout — a heuristic about font metrics won't catch it, since
  the bug is in the box coordinates, not the text.

Both are cheap to write inline as a one-off Bash/Python check against the
saved `.pptx` — no need for a permanent script in the repo.
