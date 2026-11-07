# Checklist por slide

Write it **rich enough that `template-slides` can build the deck almost
entirely from it**, since that skill only handles layout and styling, not
content judgment. A skeleton of short phrases forces `template-slides` to
invent the substance itself, which is exactly what this skill exists to
avoid. For each planned slide, include:

- A working title, and a one-line subtitle if the slide type uses one
- Which `template-slides` slide type it maps to (cover / standard content
  with card grid / overview-objectives / process-diagram / column-table /
  closing) — pick based on the material, don't force everything into one
  shape
- For every card or bullet the slide will contain: full sentences, not
  fragments — what it is, why it mattered or what problem it solved, and
  any concrete detail that makes it real (a number, a concrete before/after,
  a specific capability now possible) rather than a generic restatement of
  the title. Write these close to how they'd actually read on the slide.
- The "Resultado" / takeaway line, written out in full, if the slide type
  has one
- For a process-diagram slide, describe each connection between boxes
  (what flows, in which direction), not just the box labels
- A short note on *why this slide exists* in the narrative — what point
  it's making in the overall story of the sprint — so `template-slides`
  (or the user, reviewing) can tell if a card belongs on this slide or another
