---
name: create-chart
description: Generate one bar chart per turma (área do conhecimento x média do simulado, sorted highest to lowest) from a spreadsheet of school simulado grades. Only use this skill when the user explicitly invokes it by name — do not trigger it just because she uploads a grades spreadsheet and asks for charts/gráficos without naming the skill. If invoked without a bimestre stated, always ask which bimestre before running.
---

# Create Chart

Generates one bar chart PNG per turma (class) from a spreadsheet of simulado
grades, showing average score per área do conhecimento (knowledge area),
sorted from highest to lowest average.

## When this applies

**Explicit invocation only.** Only use this skill when the user names it
directly (e.g. "usa a skill create-chart", "roda o create-chart nessa
planilha"). Do not trigger automatically just because she uploads a
simulado spreadsheet and asks for charts/gráficos in general terms — ask
her first whether she wants this skill, or wait for her to name it. The
spreadsheet does not need to match a fixed column layout — see "Expected
input" below.

## Always ask for the titulo and bimestre first

Both are required and appear in every chart's title. If the user hasn't
already stated them when invoking the skill, ask before running the
script:

- `titulo`: must be exactly one of the two allowed options — "Média do
  Simulado por Área do Conhecimento" or "Média Bimestral por Área do
  Conhecimento". Never guess which one; ask the user to pick.
- `bimestre`: any reasonable phrasing works ("3", "3 bimestre", "3º"),
  normalized to "3º Bimestre" by normalize_bimestre — never guess, default,
  or infer it from the spreadsheet, but you don't need to insist on a
  specific format when asking the user.

## How to run it

```bash
python3 scripts/generate_charts.py <spreadsheet_path> --titulo "<titulo>" --bimestre "<bimestre>" --output-dir <output_dir>
```

- `<spreadsheet_path>`: the uploaded file (`.xlsx`, `.xlsm`, or `.numbers`).
- `--titulo`: required. One of the two allowed titles — see above. The
  script rejects anything else.
- `--bimestre`: required. Any reasonable phrasing works (e.g. `"3"`, `"3
  bimestre"`, `"3º"`) — the script normalizes it to `"3º Bimestre"` for the
  title. Ask the user for this, see above.
- `--output-dir`: where the PNGs and the final `.zip` are written (defaults
  to `./charts`). Use a fresh directory under `/home/claude` for scratch
  work, then copy the `.zip` to `/mnt/user-data/outputs` and call
  `present_files` on it.
- Dependencies: `openpyxl` (already available) for `.xlsx`/`.xlsm`;
  `numbers-parser` for `.numbers` — `pip install numbers-parser
  --break-system-packages` if the import fails.

The script prints the path to the generated `.zip` file, which contains one
PNG per turma found in the spreadsheet. The `.zip` is named after the input
spreadsheet (same stem, e.g. `notas_simulado.xlsx` → `notas_simulado.zip`).

## Expected input

The spreadsheet contains repeating blocks, one per turma, laid out as:

```
<TURMA NAME>
ÁREAS DO CONHECIMENTO | <any header, e.g. MÉDIA SIMULADO / MÉDIA GERAL>
<subject>              | <average>
<subject>              | <average>
...
<blank row>
```

Blocks can be arranged in any number of column-groups (e.g. Ensino
Fundamental in one set of columns, Ensino Médio in another) and any number
of blocks stacked vertically per group — the script finds them by scanning
for the "ÁREAS DO CONHECIMENTO" header, not by fixed row/column position.
The turma name is read from the cell directly above that header. The
value-column header text itself is not required to match anything specific
(tolerates "MÉDIA SIMULADO", "MÉDIA GERAL", etc.) — only the label column
header is used as the anchor.

If a spreadsheet uses a genuinely different layout (no "ÁREAS DO
CONHECIMENTO" header at all), don't force it through this script — ask
the user how the columns are organized before adapting the parser.

## Chart design — keep it fixed

Colors, figure size, DPI, axis labels, and title format are hardcoded as
constants at the top of `scripts/generate_charts.py`
(`CHART_FIGSIZE`, `CHART_DEFAULT_COLOR`, `CHART_DPI`, `CHART_Y_LABEL`,
`CHART_Y_MAX`, `CHART_TITLE_TEMPLATE`, `CHART_TITLE_OPTIONS`). Charts must
look identical across calls and across spreadsheets, aside from the
per-call `titulo` and `bimestre`. Do not improvise alternate styling
(colors, fonts, chart type) inline — if the design needs to change, edit
those constants in the script itself so every future run stays consistent.

Each bar is labeled with just the raw average (e.g. `8.4`) — no
percentage. Bars within each chart are sorted from highest to lowest
average (`sort_by_average_desc`), not spreadsheet order.

Bar colors are **not** fixed to a single palette color — each subject
(matéria) is colored using its own cell background color from the source
spreadsheet, resolved once into a global subject → color map so the same
subject gets the same color in every turma's chart, even across
column-groups (Fundamental vs Médio). Subjects with no discoverable fill
color fall back to `CHART_DEFAULT_COLOR`. This works for both `.xlsx`
(including Excel theme colors + tint/shade, resolved via the workbook's
theme XML) and `.numbers` (which exposes resolved RGB directly). Don't hardcode
per-subject colors — they must always come from the uploaded spreadsheet.

## After running

1. Verify the number of PNGs inside the `.zip` matches the number of
   turmas expected (sanity check against the spreadsheet before
   presenting).
2. Copy the `.zip` to `/mnt/user-data/outputs` and call `present_files` on
   it — deliver the `.zip`, not the loose PNGs.
