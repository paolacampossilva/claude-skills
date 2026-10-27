"""Generate individual and comparison bar charts from two simulado grade spreadsheets.

Each input spreadsheet must follow the same layout expected by the
create-chart skill — repeating blocks per turma:

    <TURMA NAME>
    ÁREAS DO CONHECIMENTO | <any value-column header>
    <subject>              | <average>
    <subject>              | <average>
    ...
    <blank row>

In one call, this script produces three sets of charts, bundled into a
single .zip under three folders:

- simulado/   — one per-turma bar chart from the simulado spreadsheet,
                exactly as create-chart would produce it (subject colors
                from the spreadsheet, sorted highest to lowest).
- bimestral/  — same, for the bimestral spreadsheet.
- comparativo/ — one grouped bar chart per turma present in BOTH
                spreadsheets, comparing média do simulado vs média
                bimestral per subject, in the simulado spreadsheet's
                original subject order (not sorted). Turmas or subjects
                present in only one spreadsheet are skipped, with a
                warning printed to stderr.

Supports .xlsx/.xlsm (via openpyxl) and .numbers (via numbers-parser).

Chart appearance (colors, sizes, fonts) is fixed via the CHART_* constants
below so that output stays visually identical across calls.
"""

import argparse
import colorsys
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt

HEADER_LABEL_COL = "ÁREAS DO CONHECIMENTO"

# Order of the <a:clrScheme> children in an .xlsx theme XML.
THEME_SCHEME_TAGS = (
    "dk1",
    "lt1",
    "dk2",
    "lt2",
    "accent1",
    "accent2",
    "accent3",
    "accent4",
    "accent5",
    "accent6",
    "hlink",
    "folHlink",
)
# openpyxl/Excel theme color indices swap dk1<->lt1 and dk2<->lt2 relative
# to the scheme's own declaration order.
THEME_INDEX_TO_SCHEME_INDEX = (1, 0, 3, 2, 4, 5, 6, 7, 8, 9, 10, 11)

# The only two allowed "titulo" values for individual charts, matching
# create-chart. Chosen automatically: index 0 for --simulado, index 1 for
# --bimestral — not user-configurable here.
CHART_TITLE_OPTIONS = (
    "Média do Simulado por Área do Conhecimento",
    "Média Bimestral por Área do Conhecimento",
)

# Fixed chart style — do not vary these between calls, so charts generated
# in different runs look identical. Shared by individual and comparison
# charts where the values coincide (figure size, DPI, value-axis max).
CHART_FIGSIZE = (10, 6)
CHART_DPI = 150
CHART_VALUE_MAX = 10
CHART_BAR_HEIGHT = 0.35
CHART_DEFAULT_COLOR = "#4C72B0"
INDIVIDUAL_Y_LABEL = "Média do Simulado"
INDIVIDUAL_TITLE_TEMPLATE = "{titulo} — {turma_name} — {bimestre}"
COMPARISON_VALUE_LABEL = "Média"
COMPARISON_TITLE_TEMPLATE = "{turma_name} — COMPARATIVO DE MÉDIAS (SIMULADO vs. BIMESTRAL) — {bimestre}"
COLOR_SIMULADO = "#B04A52"
COLOR_BIMESTRAL = "#F2C230"
LABEL_SIMULADO = "MÉDIA SIMULADO"
LABEL_BIMESTRAL = "MÉDIA BIMESTRAL"


@dataclass
class Cell:
    """A single spreadsheet cell: its value and its background color."""

    value: object
    color: str | None  # "#RRGGBB", or None if no fill / unresolvable


@dataclass
class TurmaGrades:
    """One turma's subjects, averages, and per-subject colors.

    subjects/averages/colors are kept in original spreadsheet order until
    sort_by_average_desc is applied (for individual charts only —
    comparison charts use the original order).
    """

    turma_name: str
    subjects: list[str]
    averages: list[float]
    colors: list[str | None]


@dataclass
class TurmaComparison:
    """Matched subject averages for one turma, from both spreadsheets."""

    turma_name: str
    subjects: list[str]
    simulado_averages: list[float]
    bimestral_averages: list[float]


def normalize_bimestre(raw: str) -> str:
    """Normalize a user-supplied bimestre value to "Nº Bimestre".

    Accepts flexible input like "3", "3 bimestre", "3º", or "3º bimestre"
    (case-insensitive) and returns a consistent "Nº Bimestre" string, so
    the chart title always reads the same way regardless of how the value
    was typed.

    Args:
        raw: User-supplied bimestre value.

    Returns:
        "Nº Bimestre" if a number is found in raw; otherwise raw itself
        with "Bimestre" appended, unless it already ends with that word.
    """
    match = re.search(r"\d+", raw)
    if match:
        return f"{match.group()}º Bimestre"

    stripped = raw.strip()
    if stripped.lower().endswith("bimestre"):
        return stripped
    return f"{stripped} Bimestre"


def normalize_header(value: object) -> str:
    """Normalize a cell value for header comparison.

    Args:
        value: Raw cell value, which may be None or non-string.

    Returns:
        The value as an uppercase, whitespace-trimmed string.
    """
    return str(value).strip().upper() if value is not None else ""


def normalize_subject(name: str) -> str:
    """Normalize a subject or turma name for matching across spreadsheets.

    Args:
        name: Raw name, e.g. " Português ".

    Returns:
        An uppercase, whitespace-trimmed version of the name.
    """
    return name.strip().upper()


def apply_theme_tint(base_rgb_hex: str, tint: float) -> str:
    """Apply an Excel theme tint/shade to a base RGB color.

    Args:
        base_rgb_hex: 6-digit hex color, no leading '#'.
        tint: Tint value from the cell's color, in [-1.0, 1.0]. Negative
            values darken (shade), positive values lighten (tint).

    Returns:
        6-digit hex color, no leading '#'.
    """
    red = int(base_rgb_hex[0:2], 16) / 255
    green = int(base_rgb_hex[2:4], 16) / 255
    blue = int(base_rgb_hex[4:6], 16) / 255
    hue, lightness, saturation = colorsys.rgb_to_hls(red, green, blue)

    if tint < 0:
        lightness = lightness * (1.0 + tint)
    else:
        lightness = lightness * (1.0 - tint) + tint

    red, green, blue = colorsys.hls_to_rgb(hue, lightness, saturation)
    return f"{round(red * 255):02X}{round(green * 255):02X}{round(blue * 255):02X}"


def load_xlsx_theme_colors(spreadsheet_path: Path) -> list[str]:
    """Read the 12 base theme colors from an .xlsx file's theme XML.

    Args:
        spreadsheet_path: Path to the .xlsx or .xlsm file.

    Returns:
        12 six-digit hex colors (no leading '#'), indexed by Excel's theme
        color index (already accounting for the dk1/lt1/dk2/lt2 swap).
    """
    namespace = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    with zipfile.ZipFile(spreadsheet_path) as archive:
        theme_xml = archive.read("xl/theme/theme1.xml")

    scheme_root = ET.fromstring(theme_xml)
    color_scheme = scheme_root.find(".//a:clrScheme", namespace)

    scheme_colors: list[str] = []
    for tag in THEME_SCHEME_TAGS:
        color_element = color_scheme.find(f"a:{tag}", namespace)
        srgb = color_element.find("a:srgbClr", namespace)
        sys_color = color_element.find("a:sysClr", namespace)
        if srgb is not None:
            scheme_colors.append(srgb.get("val"))
        else:
            scheme_colors.append(sys_color.get("lastClr"))

    return [scheme_colors[scheme_index] for scheme_index in THEME_INDEX_TO_SCHEME_INDEX]


def get_xlsx_cell_color(cell: object, theme_colors: list[str]) -> str | None:
    """Resolve an openpyxl cell's fill color to a hex string.

    Args:
        cell: An openpyxl cell.
        theme_colors: 12 theme colors, as returned by load_xlsx_theme_colors.

    Returns:
        "#RRGGBB", or None if the cell has no solid fill or the color
        cannot be resolved.
    """
    fill = cell.fill
    if fill is None or fill.patternType != "solid":
        return None

    fg_color = fill.fgColor
    if fg_color.type == "rgb" and isinstance(fg_color.rgb, str):
        rgb_hex = fg_color.rgb[-6:]
        if rgb_hex == "000000" and fg_color.rgb.upper().startswith("00"):
            return None  # fully transparent fgColor, not an actual black fill
        return f"#{rgb_hex}"

    if fg_color.type == "theme":
        base_hex = theme_colors[fg_color.theme]
        return f"#{apply_theme_tint(base_hex, fg_color.tint)}"

    return None


def load_sheet_grids(spreadsheet_path: Path) -> list[list[list[Cell]]]:
    """Load every sheet of a spreadsheet as a grid of Cell(value, color).

    Args:
        spreadsheet_path: Path to a .xlsx, .xlsm, or .numbers file.

    Returns:
        One grid per sheet. Each grid is a list of rows, each row a list
        of Cell objects (index 0 = row 1 / column 1).

    Raises:
        ValueError: If the file extension is not supported.
    """
    suffix = spreadsheet_path.suffix.lower()

    if suffix in (".xlsx", ".xlsm"):
        import openpyxl

        theme_colors = load_xlsx_theme_colors(spreadsheet_path)
        workbook = openpyxl.load_workbook(spreadsheet_path, data_only=True)
        return [
            [
                [Cell(cell.value, get_xlsx_cell_color(cell, theme_colors)) for cell in row]
                for row in workbook[sheet_name].iter_rows()
            ]
            for sheet_name in workbook.sheetnames
        ]

    if suffix == ".numbers":
        from numbers_parser import Document

        document = Document(spreadsheet_path)
        grids = []
        for sheet in document.sheets:
            for table in sheet.tables:
                grid = []
                for row in table.rows():
                    grid_row = []
                    for source_cell in row:
                        bg_color = source_cell.style.bg_color if source_cell.style else None
                        color = (
                            f"#{bg_color.r:02X}{bg_color.g:02X}{bg_color.b:02X}"
                            if bg_color is not None
                            else None
                        )
                        grid_row.append(Cell(source_cell.value, color))
                    grid.append(grid_row)
                grids.append(grid)
        return grids

    raise ValueError(f"Unsupported spreadsheet format: {suffix}")


def find_turma_blocks(grid: list[list[Cell]]) -> list[TurmaGrades]:
    """Scan a sheet grid for turma blocks and extract their grades.

    Args:
        grid: Rows of Cell objects, as returned by load_sheet_grids.

    Returns:
        One TurmaGrades entry per block found, in sheet order, with
        subjects in their original spreadsheet order (not sorted).
    """

    def cell(row_idx: int, col_idx: int) -> Cell | None:
        if 0 <= row_idx < len(grid) and 0 <= col_idx < len(grid[row_idx]):
            return grid[row_idx][col_idx]
        return None

    def cell_value(row_idx: int, col_idx: int) -> object:
        found_cell = cell(row_idx, col_idx)
        return found_cell.value if found_cell is not None else None

    num_rows = len(grid)
    num_cols = max((len(row) for row in grid), default=0)

    blocks: list[TurmaGrades] = []
    for col in range(num_cols):
        for row in range(num_rows):
            if normalize_header(cell_value(row, col)) != HEADER_LABEL_COL:
                continue

            turma_name = cell_value(row - 1, col)
            if turma_name is None:
                continue
            turma_name = str(turma_name).strip()

            subjects: list[str] = []
            averages: list[float] = []
            colors: list[str | None] = []
            data_row = row + 1
            while data_row < num_rows:
                subject_cell = cell(data_row, col)
                average_value = cell_value(data_row, col + 1)
                if subject_cell is None or subject_cell.value is None or average_value is None:
                    break
                subjects.append(str(subject_cell.value).strip())
                averages.append(float(average_value))
                colors.append(subject_cell.color)
                data_row += 1

            if subjects:
                blocks.append(TurmaGrades(turma_name, subjects, averages, colors))

    return blocks


def load_turma_grades(spreadsheet_path: Path) -> list[TurmaGrades]:
    """Parse every turma block out of a spreadsheet.

    Args:
        spreadsheet_path: Path to the input .xlsx, .xlsm, or .numbers file.

    Returns:
        One TurmaGrades entry per turma block found across all sheets.

    Raises:
        ValueError: If no turma blocks are found in any sheet.
    """
    grids = load_sheet_grids(spreadsheet_path)

    blocks: list[TurmaGrades] = []
    for grid in grids:
        blocks.extend(find_turma_blocks(grid))

    if not blocks:
        raise ValueError(
            f"No turma blocks found in {spreadsheet_path}. "
            f"Expected a '{HEADER_LABEL_COL}' column header starting each block."
        )

    return blocks


def build_subject_color_map(blocks: list[TurmaGrades]) -> dict[str, str]:
    """Build a global subject -> color map from the first color seen per subject.

    Ensures every turma's individual chart uses the same color for the
    same subject.

    Args:
        blocks: All turma blocks parsed from one spreadsheet.

    Returns:
        Map from normalized subject name to "#RRGGBB". Subjects with no
        discoverable color anywhere are omitted (callers fall back to
        CHART_DEFAULT_COLOR).
    """
    subject_colors: dict[str, str] = {}
    for block in blocks:
        for subject, color in zip(block.subjects, block.colors, strict=True):
            key = normalize_subject(subject)
            if color is not None and key not in subject_colors:
                subject_colors[key] = color
    return subject_colors


def apply_subject_color_map(blocks: list[TurmaGrades], subject_colors: dict[str, str]) -> None:
    """Overwrite each block's colors in place using the global subject color map.

    Args:
        blocks: Turma blocks to update, mutated in place.
        subject_colors: Map from normalized subject name to "#RRGGBB", as
            returned by build_subject_color_map.
    """
    for block in blocks:
        block.colors = [
            subject_colors.get(normalize_subject(subject), CHART_DEFAULT_COLOR)
            for subject in block.subjects
        ]


def clone_turma(turma: TurmaGrades) -> TurmaGrades:
    """Make an independent copy of a TurmaGrades, so sorting one doesn't affect the other.

    Args:
        turma: Turma to copy.

    Returns:
        A new TurmaGrades with copied lists.
    """
    return TurmaGrades(
        turma.turma_name, list(turma.subjects), list(turma.averages), list(turma.colors)
    )


def sort_by_average_desc(turma: TurmaGrades) -> None:
    """Reorder a turma's subjects, averages, and colors from highest to lowest average.

    Args:
        turma: Turma to reorder, mutated in place.
    """
    order = sorted(range(len(turma.averages)), key=lambda i: turma.averages[i], reverse=True)
    turma.subjects = [turma.subjects[i] for i in order]
    turma.averages = [turma.averages[i] for i in order]
    turma.colors = [turma.colors[i] for i in order]


def slugify(text: str) -> str:
    """Turn a turma name into a filesystem-safe slug.

    Args:
        text: The raw turma name, e.g. "8º ANO A".

    Returns:
        A slug like "8_ANO_A".
    """
    ascii_text = (
        text.replace("º", "")
        .replace("ª", "")
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
    )
    slug = re.sub(r"[^A-Za-z0-9]+", "_", ascii_text).strip("_")
    return slug


def plot_individual_chart(
    turma: TurmaGrades, titulo: str, bimestre: str, output_dir: Path
) -> Path:
    """Render and save a single-source bar chart for one turma (create-chart style).

    Args:
        turma: Grades for the turma to plot, already sorted highest to
            lowest average, with colors already resolved.
        titulo: One of CHART_TITLE_OPTIONS.
        bimestre: Normalized bimestre string, shown in the title.
        output_dir: Directory the PNG file is written to.

    Returns:
        Path to the saved PNG file.
    """
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE)
    bars = ax.bar(turma.subjects, turma.averages, color=turma.colors)
    ax.bar_label(bars, fmt="%.1f", padding=3)

    ax.set_title(
        INDIVIDUAL_TITLE_TEMPLATE.format(titulo=titulo, turma_name=turma.turma_name, bimestre=bimestre)
    )
    ax.set_xlabel("Área do Conhecimento")
    ax.set_ylabel(INDIVIDUAL_Y_LABEL)
    ax.set_ylim(0, CHART_VALUE_MAX)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()

    output_path = output_dir / f"{slugify(turma.turma_name)}.png"
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)
    return output_path


def generate_individual_pngs(
    blocks: list[TurmaGrades], titulo: str, bimestre: str, output_dir: Path
) -> list[Path]:
    """Resolve colors and render one individual chart per turma.

    Args:
        blocks: Turma blocks parsed from one spreadsheet. Not mutated —
            colors are resolved and sorting is applied to clones, so the
            caller's original order (needed for comparison matching) is
            preserved.
        titulo: One of CHART_TITLE_OPTIONS.
        bimestre: Normalized bimestre string.
        output_dir: Directory PNG files are written to. Created if missing.

    Returns:
        Paths to the generated PNGs, one per turma.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    subject_colors = build_subject_color_map(blocks)
    apply_subject_color_map(blocks, subject_colors)

    sorted_blocks = [clone_turma(block) for block in blocks]
    for block in sorted_blocks:
        sort_by_average_desc(block)

    return [plot_individual_chart(block, titulo, bimestre, output_dir) for block in sorted_blocks]


def match_turmas(
    simulado_blocks: list[TurmaGrades], bimestral_blocks: list[TurmaGrades]
) -> list[tuple[TurmaGrades, TurmaGrades]]:
    """Pair up turmas present in both spreadsheets by normalized name.

    Turmas found in only one spreadsheet are skipped, with a warning
    printed to stderr.

    Args:
        simulado_blocks: Turmas parsed from the simulado spreadsheet.
        bimestral_blocks: Turmas parsed from the bimestral spreadsheet.

    Returns:
        (simulado_turma, bimestral_turma) pairs, in simulado_blocks order.
    """
    bimestral_by_name = {normalize_subject(block.turma_name): block for block in bimestral_blocks}

    pairs: list[tuple[TurmaGrades, TurmaGrades]] = []
    matched_names: set[str] = set()
    for simulado_turma in simulado_blocks:
        key = normalize_subject(simulado_turma.turma_name)
        bimestral_turma = bimestral_by_name.get(key)
        if bimestral_turma is None:
            print(
                f"Aviso: turma '{simulado_turma.turma_name}' só encontrada na planilha de "
                f"simulado — pulando no gráfico comparativo.",
                file=sys.stderr,
            )
            continue
        matched_names.add(key)
        pairs.append((simulado_turma, bimestral_turma))

    for bimestral_turma in bimestral_blocks:
        key = normalize_subject(bimestral_turma.turma_name)
        if key not in matched_names:
            print(
                f"Aviso: turma '{bimestral_turma.turma_name}' só encontrada na planilha "
                f"bimestral — pulando no gráfico comparativo.",
                file=sys.stderr,
            )

    return pairs


def match_subjects(simulado_turma: TurmaGrades, bimestral_turma: TurmaGrades) -> TurmaComparison:
    """Pair up subjects present in both turma blocks by normalized name.

    Subjects found in only one side are skipped, with a warning printed to
    stderr. Order follows simulado_turma.subjects (original spreadsheet
    order, not sorted).

    Args:
        simulado_turma: Turma grades from the simulado spreadsheet.
        bimestral_turma: Same turma's grades from the bimestral spreadsheet.

    Returns:
        A TurmaComparison with only the subjects present on both sides.
    """
    bimestral_by_subject = {
        normalize_subject(subject): average
        for subject, average in zip(
            bimestral_turma.subjects, bimestral_turma.averages, strict=True
        )
    }

    subjects: list[str] = []
    simulado_averages: list[float] = []
    bimestral_averages: list[float] = []
    for subject, average in zip(simulado_turma.subjects, simulado_turma.averages, strict=True):
        key = normalize_subject(subject)
        if key not in bimestral_by_subject:
            print(
                f"Aviso: matéria '{subject}' da turma '{simulado_turma.turma_name}' só "
                f"encontrada na planilha de simulado — pulando essa matéria no comparativo.",
                file=sys.stderr,
            )
            continue
        subjects.append(subject)
        simulado_averages.append(average)
        bimestral_averages.append(bimestral_by_subject[key])

    return TurmaComparison(simulado_turma.turma_name, subjects, simulado_averages, bimestral_averages)


def plot_comparison_chart(comparison: TurmaComparison, bimestre: str, output_dir: Path) -> Path:
    """Render and save a vertical grouped bar chart for one turma.

    Args:
        comparison: Matched subjects/averages for the turma, as returned by
            match_subjects.
        bimestre: Normalized bimestre string, shown in the title.
        output_dir: Directory the PNG file is written to.

    Returns:
        Path to the saved PNG file.
    """
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE)

    positions = range(len(comparison.subjects))
    half_width = CHART_BAR_HEIGHT / 2
    simulado_bars = ax.bar(
        [p - half_width for p in positions],
        comparison.simulado_averages,
        width=CHART_BAR_HEIGHT,
        color=COLOR_SIMULADO,
        label=LABEL_SIMULADO,
    )
    bimestral_bars = ax.bar(
        [p + half_width for p in positions],
        comparison.bimestral_averages,
        width=CHART_BAR_HEIGHT,
        color=COLOR_BIMESTRAL,
        label=LABEL_BIMESTRAL,
    )
    ax.bar_label(simulado_bars, fmt="%.1f", padding=3)
    ax.bar_label(bimestral_bars, fmt="%.1f", padding=3)

    ax.set_xticks(list(positions), comparison.subjects)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    ax.set_ylim(0, CHART_VALUE_MAX)
    ax.set_xlabel("Área do Conhecimento")
    ax.set_ylabel(COMPARISON_VALUE_LABEL)
    ax.set_title(
        COMPARISON_TITLE_TEMPLATE.format(turma_name=comparison.turma_name, bimestre=bimestre)
    )
    ax.legend()
    fig.tight_layout()

    output_path = output_dir / f"{slugify(comparison.turma_name)}.png"
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)
    return output_path


def generate_comparison_pngs(
    simulado_blocks: list[TurmaGrades],
    bimestral_blocks: list[TurmaGrades],
    bimestre: str,
    output_dir: Path,
) -> list[Path]:
    """Match turmas/subjects across both spreadsheets and render comparison charts.

    Args:
        simulado_blocks: Turmas parsed from the simulado spreadsheet,
            original (unsorted) order.
        bimestral_blocks: Turmas parsed from the bimestral spreadsheet,
            original (unsorted) order.
        bimestre: Normalized bimestre string.
        output_dir: Directory PNG files are written to. Created if missing.

    Returns:
        Paths to the generated comparison PNGs, one per matched turma.

    Raises:
        ValueError: If no turma is present in both spreadsheets.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    turma_pairs = match_turmas(simulado_blocks, bimestral_blocks)
    if not turma_pairs:
        raise ValueError("No matching turma found in both spreadsheets.")

    comparisons = [
        match_subjects(simulado_turma, bimestral_turma) for simulado_turma, bimestral_turma in turma_pairs
    ]
    return [plot_comparison_chart(comparison, bimestre, output_dir) for comparison in comparisons]


def create_output_zip(
    simulado_pngs: list[Path],
    bimestral_pngs: list[Path],
    comparativo_pngs: list[Path],
    simulado_path: Path,
    bimestral_path: Path,
    output_dir: Path,
) -> Path:
    """Bundle all three sets of chart PNGs into one .zip, each under its own folder.

    Args:
        simulado_pngs: Individual simulado chart PNGs.
        bimestral_pngs: Individual bimestral chart PNGs.
        comparativo_pngs: Comparison chart PNGs.
        simulado_path: The simulado spreadsheet path — used in the .zip's
            filename.
        bimestral_path: The bimestral spreadsheet path — used in the .zip's
            filename.
        output_dir: Directory the .zip file is written to.

    Returns:
        Path to the created .zip file.
    """
    zip_path = output_dir / f"{simulado_path.stem}_vs_{bimestral_path.stem}.zip"
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for folder, png_paths in (
            ("simulado", simulado_pngs),
            ("bimestral", bimestral_pngs),
            ("comparativo", comparativo_pngs),
        ):
            for png_path in png_paths:
                archive.write(png_path, arcname=f"{folder}/{png_path.name}")
    return zip_path


def generate_all_charts(
    simulado_path: Path,
    bimestral_path: Path,
    bimestre: str,
    output_dir: Path,
) -> Path:
    """Generate individual simulado, individual bimestral, and comparison charts.

    Equivalent to running create-chart separately on each spreadsheet plus
    the turma-by-turma comparison, all in one call and one .zip.

    Args:
        simulado_path: Path to the simulado spreadsheet (.xlsx, .xlsm, or
            .numbers).
        bimestral_path: Path to the bimestral spreadsheet, same format
            requirements as simulado_path.
        bimestre: The bimestre these grades belong to. Any reasonable
            phrasing works ("3", "3 bimestre", "3º", "3º Bimestre") — it's
            normalized to "3º Bimestre" for every chart title. Always ask
            the user for this — never guess or default it.
        output_dir: Directory PNG and .zip files are written to. Created if
            missing.

    Returns:
        Path to the .zip file containing simulado/, bimestral/, and
        comparativo/ folders of charts.

    Raises:
        ValueError: If no turma is present in both spreadsheets.
    """
    bimestre = normalize_bimestre(bimestre)
    output_dir.mkdir(parents=True, exist_ok=True)

    simulado_blocks = load_turma_grades(simulado_path)
    bimestral_blocks = load_turma_grades(bimestral_path)

    simulado_pngs = generate_individual_pngs(
        simulado_blocks, CHART_TITLE_OPTIONS[0], bimestre, output_dir / "simulado"
    )
    bimestral_pngs = generate_individual_pngs(
        bimestral_blocks, CHART_TITLE_OPTIONS[1], bimestre, output_dir / "bimestral"
    )
    comparativo_pngs = generate_comparison_pngs(
        simulado_blocks, bimestral_blocks, bimestre, output_dir / "comparativo"
    )

    return create_output_zip(
        simulado_pngs, bimestral_pngs, comparativo_pngs, simulado_path, bimestral_path, output_dir
    )


def main() -> None:
    """CLI entry point: parse arguments and generate all charts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--simulado", type=Path, required=True, help="Path to the simulado grades spreadsheet"
    )
    parser.add_argument(
        "--bimestral",
        type=Path,
        required=True,
        help="Path to the bimestral (média geral) grades spreadsheet",
    )
    parser.add_argument(
        "--bimestre",
        required=True,
        help='Bimestre for the chart titles — any reasonable phrasing works '
        '("3", "3 bimestre", "3º"), normalized to "3º Bimestre"',
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("charts"),
        help="Directory PNG and .zip files are written to (default: ./charts)",
    )
    args = parser.parse_args()

    zip_path = generate_all_charts(args.simulado, args.bimestral, args.bimestre, args.output_dir)
    print(zip_path)


if __name__ == "__main__":
    main()
