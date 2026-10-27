<details open>
<summary><b>🇧🇷 pt-br</b> — synch-bilingual-readmes</summary>
<br>

# synch-bilingual-readmes

Skill do Claude que confere se todo `README.md` de um projeto tem versão completa e sincronizada em português e inglês, e corrige o que faltar.

## Por quê

Manter um README em português e seu espelho em inglês em dia exige ler os dois lados de cada README e comparar seções, comandos e variáveis à mão. Esta skill faz a comparação e escreve o texto em inglês que faltar.

## Como funciona

1. Encontra todo `README.md` do caminho informado, ignorando `.venv*`, `venv`, `node_modules`, `site-packages`, `.pytest_cache`, `.git` e `__pycache__`.
2. Marca os READMEs sem bloco em inglês (sem o marcador 🇺🇸), sem lê-los por inteiro.
3. Nos demais, confere se os dois blocos têm as mesmas seções, na mesma ordem, e as mesmas entidades concretas (comandos, variáveis de ambiente, endpoints, números), seguindo `references/deteccao-e-sincronia.md`.
4. Corrige direto, sem etapa de confirmação. O português é a fonte da verdade: cria o espelho completo em inglês quando falta, ou edita só o bloco em inglês quando os dois divergiram.
5. Relata cada README como já sincronizado, espelho criado ou sincronizado, com uma nota curta do que mudou.

O formato esperado são dois blocos `<details>` recolhíveis, um com o resumo `🇧🇷 pt-br` e outro com `🇺🇸 en`.

Ela não inventa conteúdo e não altera o texto em português. Se um README estiver errado em português, apenas relata.

## Entrada esperada

O caminho de um projeto. Se não for informado, a skill pergunta em vez de adivinhar.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md` mais um arquivo de referência, compartilhado com `synch-bilingual-docs`.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. Depois peça ao Claude para checar ou sincronizar os READMEs bilíngues de um projeto. O arquivo da skill não a restringe a ser chamada pelo nome.

Se você também usa `synch-bilingual-docs`, mantenha as duas pastas lado a lado, porque aquela skill lê o arquivo de referência desta.

As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa as ferramentas `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit` e `Agent` do Claude Code, e os comandos de shell `find` e `grep`.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — synch-bilingual-readmes</summary>
<br>

# synch-bilingual-readmes

A Claude skill that checks every `README.md` in a project for a complete, synchronized Portuguese and English version, and fixes what is missing.

## Why

Keeping a Portuguese README and its English mirror in step means reading both sides of every README and comparing sections, commands and variables by hand. This skill does the comparison and writes the missing English text.

## How it works

1. Finds every `README.md` under the project path, skipping `.venv*`, `venv`, `node_modules`, `site-packages`, `.pytest_cache`, `.git` and `__pycache__`.
2. Marks the READMEs that have no English block (no 🇺🇸 marker) without reading them in full.
3. For the others, checks that both blocks have the same sections in the same order and the same concrete entities (commands, environment variables, endpoints, numbers), following `references/deteccao-e-sincronia.md`.
4. Fixes directly, with no confirmation step. Portuguese is the source of truth: it creates the full English mirror when it is missing, or edits only the English block when the two have drifted apart.
5. Reports each README as already in sync, mirror created, or synchronized, with a short note on what changed.

The expected format is two collapsible `<details>` blocks, one with the `🇧🇷 pt-br` summary and one with the `🇺🇸 en` summary.

It does not invent content and does not change the Portuguese text. If a README is wrong in Portuguese, it only reports that.

## Expected input

The path to a project. If it is not given, the skill asks for it instead of guessing.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file plus one reference file, which is shared with `synch-bilingual-docs`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Then ask Claude to check or sync the bilingual READMEs of a project. The skill file does not restrict it to being called by name.

If you also use `synch-bilingual-docs`, keep both folders side by side, because that skill reads this one's reference file.

The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit` and `Agent` tools, and the shell commands `find` and `grep`.

</details>
