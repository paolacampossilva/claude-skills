<details open>
<summary><b>🇧🇷 pt-br</b> — colorful-summary-pdf</summary>
<br>

# colorful-summary-pdf

Skill do Claude que transforma slides de aula, anotações ou documentos longos num PDF de estudo colorido.

## Por quê

Exportações simples de markdown para PDF eram difíceis de estudar. Esta skill produz uma capa com índice colorido, uma cor de destaque por seção, selos numerados, caixas de definição, etiquetas, tabelas estilizadas e listas de passos. Material com muita matemática ganha cartões de fórmula: equações compostas em LaTeX com uma legenda explicando cada termo.

## Como funciona

1. O Claude lê o material de origem e o organiza em seções numeradas.
2. `scripts/palette.py` gera uma paleta de cores bem espaçadas para esse número de seções.
3. O Claude preenche `assets/template.html` com o conteúdo, estilizado por `assets/style.css`.
4. `scripts/mathify.py` troca as fórmulas por SVGs gerados pelo pdflatex, ou pelo matplotlib como alternativa.
5. O WeasyPrint converte o HTML no PDF final.

## Entrada esperada

Anotações de estudo, slides ou qualquer material de referência longo que o Claude consiga ler, como texto colado no chat ou arquivos anexados.

## Rodando os scripts diretamente

A partir da raiz do repositório:

```bash
pip install -r requirements.txt

python3 skills/colorful-summary-pdf/scripts/palette.py 6
python3 skills/colorful-summary-pdf/scripts/mathify.py pagina.html pagina_math.html
```

Argumentos de `palette.py`: `count` (posicional, número de seções), `--start-hue`, `--sat`, `--light`.

Argumentos de `mathify.py`: `src` e `dst` (posicionais, HTML de entrada e de saída), `--fx-dir` (padrão `fx`), `--display-scale`, `--inline-scale`, `--engine` (`auto`, `latex` ou `mpl`), `--max-width`.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` ou envie como skill personalizada. Depois peça ao Claude um PDF-resumo colorido do material que você anexar.

## Pacotes de sistema

As fórmulas em LaTeX são opcionais. Para renderizar com `pdflatex`, instale LaTeX e poppler, por exemplo em Debian ou Ubuntu:

```bash
apt-get install -y texlive-latex-base texlive-latex-extra poppler-utils
```

Sem eles, o `mathify.py` pode usar o motor do matplotlib (`--engine mpl`).

## Stack

Python, WeasyPrint, matplotlib, HTML e CSS, e opcionalmente LaTeX com poppler.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — colorful-summary-pdf</summary>
<br>

# colorful-summary-pdf

A Claude skill that turns lecture slides, notes or long documents into a colorful study-guide PDF.

## Why

Plain markdown-to-PDF exports were hard to study from. This skill produces a cover with a color-coded index, one accent color per section, numbered badges, definition callouts, tag chips, styled tables and step lists. Math-heavy material gets formula cards: equations typeset with LaTeX plus a legend explaining every term.

## How it works

1. Claude reads the source material and outlines it into numbered sections.
2. `scripts/palette.py` generates an evenly spaced color palette for that number of sections.
3. Claude fills `assets/template.html` with the content, styled by `assets/style.css`.
4. `scripts/mathify.py` replaces formulas with SVGs rendered by pdflatex, or by matplotlib as a fallback.
5. WeasyPrint renders the HTML into the final PDF.

## Expected input

Study notes, slides or any long reference material that Claude can read, such as text pasted in the chat or attached files.

## Running the scripts directly

From the repository root:

```bash
pip install -r requirements.txt

python3 skills/colorful-summary-pdf/scripts/palette.py 6
python3 skills/colorful-summary-pdf/scripts/mathify.py page.html page_math.html
```

`palette.py` arguments: `count` (positional, number of sections), `--start-hue`, `--sat`, `--light`.

`mathify.py` arguments: `src` and `dst` (positional, HTML in and out), `--fx-dir` (default `fx`), `--display-scale`, `--inline-scale`, `--engine` (`auto`, `latex` or `mpl`), `--max-width`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/`, or upload it as a custom skill. Then ask Claude for a colorful summary PDF of the material you attach.

## System packages

LaTeX formulas are optional. For `pdflatex` rendering, install LaTeX and poppler, for example on Debian or Ubuntu:

```bash
apt-get install -y texlive-latex-base texlive-latex-extra poppler-utils
```

Without them, `mathify.py` can use the matplotlib engine (`--engine mpl`).

## Stack

Python, WeasyPrint, matplotlib, HTML and CSS, and optionally LaTeX with poppler.

</details>
