<details open>
<summary><b>🇧🇷 pt-br</b> — synch-bilingual-docs</summary>
<br>

# synch-bilingual-docs

Skill do Claude que confere se todo arquivo Markdown de uma pasta `docs/` tem versão completa e sincronizada em português e inglês, e corrige o que faltar.

## Por quê

Manter cada documento de uma pasta `docs/` bilíngue exige ler os dois lados de cada arquivo e compará-los à mão. Esta skill faz a comparação e escreve o texto em inglês que faltar.

## Como funciona

1. Encontra todo `*.md` do caminho `docs/` informado, em qualquer profundidade, exceto arquivos chamados `README.md` (esses são de `synch-bilingual-readmes`) e pastas de dependência ou cache.
2. Marca os arquivos sem bloco em inglês (sem o marcador 🇺🇸), sem lê-los por inteiro.
3. Nos demais, confere se os dois blocos têm as mesmas seções, na mesma ordem, e as mesmas entidades concretas (comandos, variáveis, endpoints, números, caminhos de arquivo), com o método de `../synch-bilingual-readmes/references/deteccao-e-sincronia.md`.
4. Corrige direto, sem etapa de confirmação. O português é a fonte da verdade: cria o espelho completo em inglês quando falta, ou edita só o bloco em inglês quando os dois divergiram.
5. Relata cada arquivo como já sincronizado, espelho criado ou sincronizado, com uma nota curta do que mudou.

Arquivos que não são Markdown e que os docs referenciam (`.csv`, `.json`, `.pdf`, `.png`) não são lidos nem alterados. Seus caminhos só são mantidos idênticos no bloco em inglês.

Ela não inventa conteúdo e não altera o texto em português. Se um documento estiver errado em português, apenas relata.

## Entrada esperada

O caminho de uma pasta `docs/`. Se não for informado, a skill pergunta. Ela nunca procura pastas `docs/` num projeto por conta própria.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md`. Ela não tem arquivo de referência próprio e usa o de `synch-bilingual-readmes`.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. Copie `synch-bilingual-readmes` ao lado dela, porque o arquivo de referência é obrigatório. Depois peça ao Claude para checar ou sincronizar os docs bilíngues de uma pasta `docs/`. O arquivo da skill não a restringe a ser chamada pelo nome.

As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa as ferramentas `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit` e `Agent` do Claude Code, e os comandos de shell `find` e `grep`.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — synch-bilingual-docs</summary>
<br>

# synch-bilingual-docs

A Claude skill that checks every Markdown file inside a `docs/` folder for a complete, synchronized Portuguese and English version, and fixes what is missing.

## Why

Keeping each document in a `docs/` folder bilingual means reading both sides of every file and comparing them by hand. This skill does the comparison and writes the missing English text.

## How it works

1. Finds every `*.md` file under the given `docs/` path, at any depth, except files named `README.md` (those belong to `synch-bilingual-readmes`) and dependency or cache folders.
2. Marks the files that have no English block (no 🇺🇸 marker) without reading them in full.
3. For the others, checks that both blocks have the same sections in the same order and the same concrete entities (commands, variables, endpoints, numbers, file paths), using the method in `../synch-bilingual-readmes/references/deteccao-e-sincronia.md`.
4. Fixes directly, with no confirmation step. Portuguese is the source of truth: it creates the full English mirror when it is missing, or edits only the English block when the two have drifted apart.
5. Reports each file as already in sync, mirror created, or synchronized, with a short note on what changed.

Non-Markdown files that the docs reference (`.csv`, `.json`, `.pdf`, `.png`) are not read or changed. Their paths are only kept identical in the English block.

It does not invent content and does not change the Portuguese text. If a document is wrong in Portuguese, it only reports that.

## Expected input

The path to a `docs/` folder. If it is not given, the skill asks for it. It never searches a project for `docs/` folders on its own.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file. It has no reference file of its own and uses the one from `synch-bilingual-readmes`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Copy `synch-bilingual-readmes` next to it, because its reference file is required. Then ask Claude to check or sync the bilingual docs in a given `docs/` folder. The skill file does not restrict it to being called by name.

The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit` and `Agent` tools, and the shell commands `find` and `grep`.

</details>
