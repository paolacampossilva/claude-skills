"""Generate one bar chart per class (turma) from a simulado grade spreadsheet.

The spreadsheet is expected to contain repeating blocks laid out as:

    <TURMA NAME>
    ÁREAS DO CONHECIMENTO | <any value-column header>
    <subject>              | <average>
    <subject>              | <average>
    ...
    <blank row>

Blocks may be arranged in any number of column-groups (e.g. one group of
columns for Ensino Fundamental, another for Ensino Médio) and any number of
blocks stacked vertically within a group. The parser locates blocks by
searching for a first-column header of "ÁREAS DO CONHECIMENTO" rather than
assuming fixed rows or columns, so it tolerates spreadsheets with a
different number of turmas, a different column layout, or a differently
worded value-column header (e.g. "MÉDIA SIMULADO" vs "MÉDIA GERAL").

Supports .xlsx/.xlsm (via openpyxl) and .numbers (via numbers-parser).

Each subject's bar is colored using that subject's own cell background
color in the source spreadsheet, so the chart palette matches the
spreadsheet's own color coding. A subject with no discoverable color falls
back to CHART_DEFAULT_COLOR. Everything else about chart appearance (sizes,
fonts, labels) is fixed via the CHART_* constants below so that output
stays visually identical across calls.
"""

import argparse
import colorsys
import re
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

# Fixed chart style — do not vary these between calls, so charts generated
# in different runs look identical.
CHART_FIGSIZE = (10, 6)
CHART_DEFAULT_COLOR = "#4C72B0"
CHART_DPI = 150
CHART_Y_LABEL = "Média do Simulado"
CHART_Y_MAX = 10
CHART_TITLE_TEMPLATE = "{titulo} — {turma_name} — {bimestre}"

# The only two allowed values for the --titulo argument.
CHART_TITLE_OPTIONS = (
    "Média do Simulado por Área do Conhecimento",
    "Média Bimestral por Área do Conhecimento",
)


@dataclass
class Cell:
    """A single spreadsheet cell: its value and its background color."""

    value: object
    color: str | None  # "#RRGGBB", or None if no fill / unresolvable


@dataclass
class TurmaGrades:
    """Grades for a single turma (class), one average per knowledge area."""

    turma_name: str
    subjects: list[str]
    averages: list[float]
    colors: list[str | None]


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
    """Normalize a subject name for use as a color-map key.

    Args:
        name: Raw subject name, e.g. " Português ".

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
        One TurmaGrades entry per block found, in sheet order. The `colors`
        field holds each subject's raw cell color (possibly None); callers
        that want consistent colors across turmas should resolve a global
        subject -> color map instead of using these directly.
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


def build_subject_color_map(blocks: list[TurmaGrades]) -> dict[str, str]:
    """Build a global subject -> color map from the first color seen per subject.

    Ensures every turma's chart uses the same color for the same subject,
    even if a given subject's cell color happened to be missing in one
    block but present in another.

    Args:
        blocks: All turma blocks parsed from the spreadsheet.

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


def plot_turma_chart(turma: TurmaGrades, titulo: str, bimestre: str, output_dir: Path) -> Path:
    """Render and save a bar chart for one turma.

    Args:
        turma: Grades for the turma to plot. `colors` must already be
            resolved (see apply_subject_color_map) — no fallback is applied
            here. Bars are plotted in the order subjects/averages already
            have — sort with sort_by_average_desc beforehand if needed.
        titulo: One of CHART_TITLE_OPTIONS, shown as the chart's main title.
        bimestre: The bimestre these grades belong to (e.g. "1º Bimestre"),
            shown in the chart title.
        output_dir: Directory the PNG file is written to.

    Returns:
        Path to the saved PNG file.
    """
    fig, ax = plt.subplots(figsize=CHART_FIGSIZE)
    bars = ax.bar(turma.subjects, turma.averages, color=turma.colors)
    ax.bar_label(bars, fmt="%.1f", padding=3)

    chart_title = CHART_TITLE_TEMPLATE.format(
        titulo=titulo, turma_name=turma.turma_name, bimestre=bimestre
    )
    ax.set_title(chart_title)
    ax.set_xlabel("Área do Conhecimento")
    ax.set_ylabel(CHART_Y_LABEL)
    ax.set_ylim(0, CHART_Y_MAX)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()

    output_path = output_dir / f"{slugify(turma.turma_name)}.png"
    fig.savefig(output_path, dpi=CHART_DPI)
    plt.close(fig)
    return output_path


def create_output_zip(png_paths: list[Path], spreadsheet_path: Path, output_dir: Path) -> Path:
    """Bundle generated chart PNGs into a .zip named after the spreadsheet.

    Args:
        png_paths: PNG files to include in the archive.
        spreadsheet_path: The input spreadsheet the charts were built from —
            its filename stem is reused for the .zip file.
        output_dir: Directory the .zip file is written to.

    Returns:
        Path to the created .zip file.
    """
    zip_path = output_dir / f"{spreadsheet_path.stem}.zip"
    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for png_path in png_paths:
            archive.write(png_path, arcname=png_path.name)
    return zip_path


def generate_charts(spreadsheet_path: Path, titulo: str, bimestre: str, output_dir: Path) -> Path:
    """Generate one bar chart PNG per turma and bundle them into a .zip.

    Each subject is colored using its own background color from the source
    spreadsheet (consistent across every turma), falling back to
    CHART_DEFAULT_COLOR for subjects with no discoverable color. Within
    each chart, bars are sorted from highest to lowest average.

    Args:
        spreadsheet_path: Path to the input .xlsx, .xlsm, or .numbers file.
        titulo: One of CHART_TITLE_OPTIONS — always ask the user which one
            they want, never guess or default it.
        bimestre: The bimestre these grades belong to. Any reasonable
            phrasing works ("3", "3 bimestre", "3º", "3º Bimestre") — it's
            normalized to "3º Bimestre" for the chart title via
            normalize_bimestre. Always ask the user for this — never guess
            or default it.
        output_dir: Directory PNG and .zip files are written to. Created if
            missing.

    Returns:
        Path to the .zip file containing every generated chart.

    Raises:
        ValueError: If no turma blocks are found in any sheet, or titulo
            is not one of CHART_TITLE_OPTIONS.
    """
    if titulo not in CHART_TITLE_OPTIONS:
        raise ValueError(f"titulo must be one of {CHART_TITLE_OPTIONS!r}, got {titulo!r}")

    bimestre = normalize_bimestre(bimestre)

    output_dir.mkdir(parents=True, exist_ok=True)
    grids = load_sheet_grids(spreadsheet_path)

    all_blocks: list[TurmaGrades] = []
    for grid in grids:
        all_blocks.extend(find_turma_blocks(grid))

    if not all_blocks:
        raise ValueError(
            f"No turma blocks found in {spreadsheet_path}. "
            f"Expected a '{HEADER_LABEL_COL}' column header starting each block."
        )

    subject_colors = build_subject_color_map(all_blocks)
    apply_subject_color_map(all_blocks, subject_colors)
    for block in all_blocks:
        sort_by_average_desc(block)

    png_paths = [plot_turma_chart(turma, titulo, bimestre, output_dir) for turma in all_blocks]
    return create_output_zip(png_paths, spreadsheet_path, output_dir)


def main() -> None:
    """CLI entry point: parse arguments and generate charts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spreadsheet", type=Path, help="Path to the input .xlsx file")
    parser.add_argument(
        "--titulo",
        required=True,
        choices=CHART_TITLE_OPTIONS,
        help="Chart title shown on every chart",
    )
    parser.add_argument(
        "--bimestre",
        required=True,
        help='Bimestre for the chart title — any reasonable phrasing works '
        '("3", "3 bimestre", "3º"), normalized to "3º Bimestre"',
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("charts"),
        help="Directory PNG and .zip files are written to (default: ./charts)",
    )
    args = parser.parse_args()

    zip_path = generate_charts(args.spreadsheet, args.titulo, args.bimestre, args.output_dir)
    print(zip_path)


if __name__ == "__main__":
    main()
