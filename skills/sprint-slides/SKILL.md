---
name: sprint-slides
description: >-
  [Uses → template-slides] Plans the *content* of a team end-of-sprint presentation from a project
  folder the user points to (code, .md task files, PDFs, images), at a level a
  mixed, non-technical audience can follow. Produces a slide-by-slide outline
  for the user to approve, then hands off to template-slides to generate the
  .pptx. Only use when the user explicitly invokes it by name (e.g. "usa o
  sprint-slides nessa pasta") — not just because they ask for slides or a
  summary of a folder in general terms. Always ask for the folder path if
  missing.
---

# Sprint Slides

Turns "here's everything we worked on" into a presentation outline a
non-technical audience can follow, then hands off to `template-slides` to
generate the styled `.pptx`. This skill owns the *content* decisions —
what to say, how much technical detail to keep, how to group it into
slides. It does not touch layout, color, or typography; that's
`template-slides`'s job.

## When this applies

**Explicit invocation only**, same convention as the user's other skills. They
will invoke this by name and give a folder path (e.g. "usa o sprint-slides
na pasta ./sprint-4"). If they name the skill without a path, ask for one
before doing anything else — don't guess a folder, and never infer it from
the current directory.

## Step 1 — Read everything in the folder

The folder's contents vary per sprint and aren't limited to one file type —
expect a mix of source code, `.md` task files, and sometimes PDFs or
images. Read all of it before drafting anything:

- **Code files**: read for *what capability changed*, not implementation
  detail. You're extracting "we built X" / "X now does Y", not documenting
  functions.
- **`.md` files**: usually the most direct source of what was planned and
  done — read these closely, they likely state intent in the user's own words.
- **PDFs**: extract text (and skim embedded images/diagrams if any).
- **Images**: view them directly — screenshots, diagrams, whiteboard
  photos may carry information nothing else in the folder does.

If the folder has many files (more than ~5-6), launch agents in parallel
(tool `Agent`, one file group per agent) rather than reading everything
sequentially — breadth still matters more than depth on any single file, the
goal is a high-level map of the sprint, not a deep read of one module.

If something in the folder is ambiguous or contradicts something else
(e.g. a task `.md` describes a plan but the code shows it changed), ask
the user rather than guessing which is current.

## Step 2 — Draft the outline

Write a slide-by-slide outline, not the final slide text — but write it
**rich enough that `template-slides` can build the deck almost entirely
from it**, since that skill only handles layout and styling, not content
judgment. A skeleton of short phrases forces `template-slides` to invent
the substance itself, which is exactly what this skill exists to avoid.
Follow `references/checklist-slides.md` for what each planned slide needs.

**Audience calibration — this is the part that matters most:** the
audience is not only computer-science people. Simplify liberally, but
don't strip out technical accuracy entirely — it's fine to name things
like "API", "banco de dados", or "modelo de linguagem" as concepts, but
skip implementation detail (specific libraries, function names, code
structure, internal architecture decisions) unless it's the actual point
of the slide. Prefer framing around what changed and why it matters over
how it was built. When in doubt, cut a technical detail rather than keep
it — the outline should read like an explanation to an interested outsider,
not a subset of the commit log. Richer detail means more concrete
substance and context, not more jargon — a longer sentence that's still
in plain language beats a short one that hides the interesting part.

Don't guess the sprint number if it isn't findable in the folder — ask
the user if it's genuinely unclear. Team name, team members, and advisors
are `template-slides`'s inputs, which it asks for if missing — you don't
need to gather them here.

**Copy style — confirmed preferences, apply from the first draft:**

- Join two related clauses with a comma, never an em dash. The user
  prefers commas over dashes — treat this as a hard rule, not a
  style option, for any prose you draft (card bodies, "Resultado" callouts,
  subtitles).
- Don't repeat a card's number as a text prefix ("Objetivo 1 — ...",
  "Etapa 2 — ...") when the slide's numbered icon badge already shows that
  number — it's redundant. Start the title straight at the substance
  ("Mapear o sistema de origem", not "Objetivo 1 — Mapear o sistema de origem").
- Keep illustrative examples vendor/product-neutral. Don't name a specific
  AI assistant or tool as a parenthetical example ("um cliente de IA (ex.:
  Claude) fala com...") unless the slide's actual subject is that specific
  tool — say "um cliente de IA fala com..." instead.
- Avoid a manual line break inside a title when natural word-wrap already
  breaks it reasonably — write it as one continuous string and let the
  card's word-wrap decide, rather than hardcoding where it splits. Only
  force a manual break for a title with a genuine two-part structure meant
  to read as two lines.

## Step 3 — Get approval before generating anything

Present the outline in the conversation (plain text/markdown, not a file)
and ask the user to review it. Treat this as a real checkpoint, not a
formality:

- If they ask for changes, revise and show the updated outline again.
- Don't touch `template-slides` or write any `pptxgenjs` code until they
  clearly approve the outline.

## Step 4 — Hand off to template-slides

Once approved, follow the `template-slides` skill's own instructions to
generate the `.pptx`, using this outline as the finished content — it's
written in full sentences precisely so `template-slides` can drop it into
cards largely as-is rather than drafting its own wording. Don't let
`template-slides` re-interview the user for content the outline already
settled (its own SKILL.md says to treat an approved outline this way). You
only need to pass along the sprint number and anything `template-slides`
asks for that the outline doesn't answer (team, advisors, logos).
