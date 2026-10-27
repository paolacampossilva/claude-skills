---
name: merge-charts
description: In one call, generate individual bar charts for a simulado grades spreadsheet, individual bar charts for a bimestral grades spreadsheet, AND a per-turma comparison chart between the two (média do simulado vs média bimestral) — equivalent to running create-chart on each spreadsheet plus the comparison. Only use this skill when the user explicitly invokes it by name — do not trigger it just because she uploads two grades spreadsheets and asks to compare them. If invoked without a bimestre stated, always ask before running.
---

# Merge Charts

Generates three sets of bar charts from two simulado-style spreadsheets, in
a single call and a single `.zip`:

- **simulado/** — one per-turma chart from the simulado spreadsheet, exactly
  as create-chart would produce it (per-subject colors from the
  spreadsheet, sorted highest to lowest, titulo "Média do Simulado por Área
  do Conhecimento").
- **bimestral/** — same, for the bimestral spreadsheet (titulo "Média
  Bimestral por Área do Conhecimento").
- **comparativo/** — one grouped bar chart per turma present in BOTH
  spreadsheets, comparing each subject's simulado average against its
  bimestral average, in the simulado spreadsheet's original subject order
  (not sorted).

This is a superset of running create-chart on each spreadsheet separately —
use this skill instead of two separate create-chart calls whenever the user
also wants the comparison.

## When this applies

**Explicit invocation only.** Only use this skill when the user names it
directly (e.g. "usa a skill merge-charts", "junta esses dois com o
merge-charts"). Do not trigger automatically just because she uploads two
simulado-style spreadsheets and asks to compare them — ask her first
whether she wants this skill, or wait for her to name it.

## Always confirm which file is which

The script has no way to tell which spreadsheet is the simulado one and
which is the bimestral one — it only trusts whichever path is passed to
`--simulado` vs `--bimestral`. It does NOT inspect file names or content to
decide. If the user hasn't made it unambiguous which upload is which (e.g. via
clearly named files, or by saying so directly), ask before running instead
of guessing — assigning them backwards silently mislabels every chart's
titulo and swaps the legend colors in the comparison.

## Always ask for the bimestre first

The bimestre is required and appears in every chart's title (individual and
comparison alike). If the user hasn't already stated it when invoking the
skill, ask before running. Never guess, default, or infer it from the
spreadsheet — but you don't need to insist on a specific format when
asking: any reasonable phrasing ("3", "3 bimestre", "3º") is normalized to
"3º Bimestre" by normalize_bimestre.

## How to run it

```bash
python3 scripts/merge_charts.py --simulado <simulado_path> --bimestral <bimestral_path> --bimestre "<bimestre>" --output-dir <output_dir>
```

- `--simulado`: path to the simulado grades spreadsheet (`.xlsx`, `.xlsm`,
  or `.numbers`).
- `--bimestral`: path to the bimestral/média geral grades spreadsheet, same
  format requirements.
- `--bimestre`: required. Any reasonable phrasing works (e.g. `"3"`, `"3
  bimestre"`, `"3º"`) — the script normalizes it to `"3º Bimestre"` for
  every title. See above.
- `--output-dir`: where the PNGs and the final `.zip` are written (defaults
  to `./charts`). Use a fresh directory under `/home/claude` for scratch
  work, then copy the `.zip` to `/mnt/user-data/outputs` and call
  `present_files` on it.
- Dependencies: `openpyxl` (already available) for `.xlsx`/`.xlsm`;
  `numbers-parser` for `.numbers` — `pip install numbers-parser
  --break-system-packages` if the import fails.

Both spreadsheets must use the same block layout create-chart expects (see
that skill's "Expected input" section) — repeating `<TURMA NAME>` /
`ÁREAS DO CONHECIMENTO` blocks. The two spreadsheets don't need identical
turma or subject sets: a turma present in only one spreadsheet still gets
its own individual chart, but is skipped from `comparativo/` (warning
printed to stderr). Same for a subject present in only one side of a
matched turma.

The script prints the path to the generated `.zip`, named
`<simulado_stem>_vs_<bimestral_stem>.zip`, containing the `simulado/`,
`bimestral/`, and `comparativo/` folders (one PNG per turma in each).

## Chart design — keep it fixed

Colors, figure size, DPI, axis labels, and title/legend text are hardcoded
as constants at the top of `scripts/merge_charts.py`
(`CHART_FIGSIZE`, `CHART_DPI`, `CHART_VALUE_MAX`, `CHART_BAR_HEIGHT`,
`CHART_DEFAULT_COLOR`, `INDIVIDUAL_Y_LABEL`, `INDIVIDUAL_TITLE_TEMPLATE`,
`COMPARISON_VALUE_LABEL`, `COMPARISON_TITLE_TEMPLATE`, `COLOR_SIMULADO`,
`COLOR_BIMESTRAL`, `LABEL_SIMULADO`, `LABEL_BIMESTRAL`,
`CHART_TITLE_OPTIONS`). Charts must look identical across calls and across
spreadsheets, aside from the per-call turma/subject data and bimestre. Do
not improvise alternate styling inline — if the design needs to change,
edit those constants in the script itself.

Individual charts (`simulado/`, `bimestral/`) are vertical columns, one
color per subject taken from that spreadsheet's own cell fill colors
(consistent across every turma in that spreadsheet), sorted highest to
lowest average — same behavior as create-chart. Comparison charts
(`comparativo/`) are vertical grouped columns, two fixed colors
(simulado/bimestral), NOT sorted — order follows the simulado
spreadsheet's original row order.

## After running

1. Check stderr for any "Aviso" (warning) lines about skipped turmas or
   subjects in the comparison, and mention them to the user — don't silently
   drop data.
2. Copy the `.zip` to `/mnt/user-data/outputs` and call `present_files` on
   it — deliver the `.zip`, not the loose PNGs.
