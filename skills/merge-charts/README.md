<details open>
<summary><b>🇧🇷 pt-br</b> — merge-charts</summary>
<br>

# merge-charts

Skill do Claude que gera os gráficos do simulado, os gráficos bimestrais e a comparação entre os dois numa única chamada.

## Por quê

Além dos gráficos por turma de cada planilha, comparar a média do simulado com a média bimestral por turma é mais uma etapa manual de montagem de gráficos. Esta skill produz tudo numa execução só.

## Como funciona

O script lê uma planilha do simulado e uma planilha bimestral e grava um .zip com três pastas:

- `simulado/`: um gráfico de barras por turma, do maior para o menor, como em `create-chart`.
- `bimestral/`: o mesmo para a planilha bimestral.
- `comparativo/`: um gráfico de barras agrupadas por turma presente nas duas planilhas, comparando a média do simulado com a média bimestral de cada disciplina, na ordem de disciplinas da planilha do simulado.

O script não detecta qual arquivo é qual: ele confia nos caminhos passados a `--simulado` e `--bimestral`.

## Entrada esperada

Dois arquivos `.xlsx`, `.xlsm` ou `.numbers` com o mesmo layout do `create-chart`: cada turma é um bloco com o nome da turma, o cabeçalho "ÁREAS DO CONHECIMENTO" logo abaixo e uma linha por disciplina com a média.

## Rodando os scripts diretamente

A partir da raiz do repositório:

```bash
pip install -r requirements.txt

python3 skills/merge-charts/scripts/merge_charts.py \
  --simulado simulado.xlsx \
  --bimestral bimestral.xlsx \
  --bimestre "1º Bimestre" \
  --output-dir charts
```

Argumentos:

- `--simulado` (obrigatório): caminho da planilha do simulado.
- `--bimestral` (obrigatório): caminho da planilha bimestral (média geral).
- `--bimestre` (obrigatório): qualquer forma como `3`, `3 bimestre` ou `3º`, normalizada para `3º Bimestre`.
- `--output-dir`: onde os PNG e o .zip são gravados (padrão `charts`).

O script imprime o caminho do .zip.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` ou envie como skill personalizada. Ela só roda quando chamada pelo nome e pergunta qual arquivo é o simulado e qual é o bimestral, e o bimestre, antes de gerar qualquer coisa.

## Stack

Python, matplotlib e openpyxl para ler arquivos `.xlsx` e `.xlsm`. Ler arquivos `.numbers` exige o pacote opcional `numbers-parser`. As cores de tema do .xlsx são lidas com `zipfile` e `ElementTree` da biblioteca padrão.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — merge-charts</summary>
<br>

# merge-charts

A Claude skill that builds the simulado charts, the bimonthly charts and a comparison between the two in one call.

## Why

Besides the per-class charts for each spreadsheet, comparing the simulado average with the bimonthly average per class is another manual chart-making step. This skill produces all of it in a single run.

## How it works

The script reads a simulado spreadsheet and a bimonthly spreadsheet and writes one .zip with three folders:

- `simulado/`: one bar chart per turma, sorted from highest to lowest, as in `create-chart`.
- `bimestral/`: the same for the bimonthly spreadsheet.
- `comparativo/`: one grouped bar chart per turma present in both spreadsheets, comparing each subject's simulado average with its bimonthly average, in the simulado spreadsheet's subject order.

The script does not detect which file is which; it trusts the paths given to `--simulado` and `--bimestral`.

## Expected input

Two `.xlsx`, `.xlsm` or `.numbers` files with the same layout as in `create-chart`: each turma is a block with the turma name, an "ÁREAS DO CONHECIMENTO" header right below it, then one row per subject with its average.

## Running the scripts directly

From the repository root:

```bash
pip install -r requirements.txt

python3 skills/merge-charts/scripts/merge_charts.py \
  --simulado simulado.xlsx \
  --bimestral bimestral.xlsx \
  --bimestre "1º Bimestre" \
  --output-dir charts
```

Arguments:

- `--simulado` (required): path to the simulado spreadsheet.
- `--bimestral` (required): path to the bimonthly (média geral) spreadsheet.
- `--bimestre` (required): any phrasing such as `3`, `3 bimestre` or `3º`, normalized to `3º Bimestre`.
- `--output-dir`: where the PNG files and .zip are written (default `charts`).

The script prints the path of the .zip.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/`, or upload it as a custom skill. It only runs when invoked by name, and it asks which file is the simulado and which is the bimonthly, and for the bimester, before generating anything.

## Stack

Python, matplotlib, and openpyxl to read `.xlsx` and `.xlsm` files. Reading `.numbers` files needs the optional `numbers-parser` package. The .xlsx theme colors are read with the standard library's `zipfile` and `ElementTree`.

</details>
