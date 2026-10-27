<details open>
<summary><b>🇧🇷 pt-br</b> — check-docstrings</summary>
<br>

# check-docstrings

Skill do Claude que audita as docstrings e os comentários de um projeto Python quanto ao idioma e à desatualização.

## Por quê

Conferir à mão se toda docstring e todo comentário estão em inglês, e se ainda batem com o código que descrevem, exige abrir cada arquivo e comparar texto com código. Esta skill faz essa passada no projeto inteiro.

## Como funciona

1. Encontra todos os arquivos `*.py` do caminho informado, ignorando `.venv*`, `venv`, `node_modules`, `site-packages`, `__pycache__`, `.git` e `.pytest_cache`.
2. Lê cada arquivo e classifica cada docstring e comentário `#` como português ou inglês, com as regras de `references/deteccao-idioma.md`. Identificadores, código de exemplo, valores literais e nomes de contratos externos não são traduzidos.
3. Compara cada docstring com o código que ela documenta, com as checagens de `references/deteccao-desatualizado.md` (por exemplo, `Args:` que não bate mais com a assinatura, ou comentário que cita código removido). Só divergências concretas e verificáveis são sinalizadas.
4. Traduz para inglês, na hora, as docstrings e comentários em português.
5. Mostra todos os achados de desatualização num resumo único e pergunta quais correções aplicar. Aplica só as aprovadas.
6. Imprime um relatório final: arquivos analisados, traduções aplicadas, achados de desatualização encontrados, corrigidos e deixados de fora.

Em projetos grandes, pode dividir os arquivos entre agentes em paralelo.

## Entrada esperada

O caminho de um projeto Python. Se não for informado, a skill pergunta com `AskUserQuestion` em vez de adivinhar.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md` mais dois arquivos de referência, e o único argumento é o caminho do projeto, recebido do Claude.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. Depois peça ao Claude para checar ou auditar as docstrings de um projeto, por exemplo `/check-docstrings caminho/do/projeto`. O arquivo da skill não a restringe a ser chamada pelo nome.

As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa as ferramentas `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit`, `Agent` e `AskUserQuestion` do Claude Code, e o comando de shell `find`. Só trata arquivos Python.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — check-docstrings</summary>
<br>

# check-docstrings

A Claude skill that audits the docstrings and comments of a Python project for language and for staleness.

## Why

Checking by hand that every docstring and comment is in English, and that each one still matches the code it describes, means opening every file and comparing text against code. This skill does that pass for a whole project.

## How it works

1. Finds every `*.py` file under the project path, skipping `.venv*`, `venv`, `node_modules`, `site-packages`, `__pycache__`, `.git` and `.pytest_cache`.
2. Reads each file and classifies every docstring and `#` comment as Portuguese or English, using the rules in `references/deteccao-idioma.md`. Identifiers, example code, literal values and external contract names are not translated.
3. Compares each docstring with the code it documents, using the checks in `references/deteccao-desatualizado.md` (for example `Args:` that no longer match the signature, or a comment that refers to code that was removed). Only concrete, verifiable mismatches are flagged.
4. Translates Portuguese docstrings and comments to English right away.
5. Shows all staleness findings in one summary and asks which fixes to apply. It applies only the approved ones.
6. Prints a final report: files scanned, translations applied, staleness findings found, fixed and left out.

For large projects it can split the files across parallel agents.

## Expected input

The path to a Python project. If it is not given, the skill asks for it with `AskUserQuestion` instead of guessing.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file plus two reference files, and the only argument is the project path it receives from Claude.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Then ask Claude to check or audit the docstrings of a project, for example `/check-docstrings path/to/project`. The skill file does not restrict it to being called by name.

The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit`, `Agent` and `AskUserQuestion` tools, and the shell command `find`. It only handles Python files.

</details>
