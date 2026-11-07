<details open>
<summary><b>🇧🇷 pt-br</b> — create-main-readme</summary>
<br>

# create-main-readme

Skill do Claude que cria ou corrige o `README.md` principal de um projeto, módulo ou pasta de time, seguindo um esqueleto fixo e adaptando o conteúdo ao que o projeto realmente tem.

## Por quê

Um README raiz completo (sumário, tecnologias, instalação, estrutura, uma seção por módulo, variáveis de ambiente, testes, tipos de commit, espelho em inglês) dá trabalho para manter igual em todo projeto. A skill aplica o mesmo esqueleto sem inventar o que não existe.

## Como funciona

1. Lê o projeto (código, configs, READMEs existentes) para saber o que ele realmente tem.
2. Mostra um plano: quais seções do esqueleto serão preenchidas, quais serão omitidas e por quê, e o que ainda falta saber.
3. Só escreve o README depois da sua confirmação explícita.
4. Escreve o README em português com o espelho em inglês, e confere com `references/checklist-qualidade.md`.

## Entrada esperada

O caminho do projeto. Se não for informado, a skill pergunta, nunca infere. A lista de integrantes vem de um README irmão, do `CLAUDE.md` ou do que você informar, e sem isso a skill pergunta.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md` mais arquivos de referência.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa as ferramentas `Read`, `Glob`, `Write`, `Edit` e `AskUserQuestion` do Claude Code.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — create-main-readme</summary>
<br>

# create-main-readme

A Claude skill that creates or fixes a project's, module's or team folder's main `README.md`, following a fixed skeleton and adapting the content to what the project really has.

## Why

A complete root README (table of contents, technologies, installation, structure, one section per module, environment variables, tests, commit types, English mirror) is tedious to keep the same across projects. The skill applies the same skeleton without inventing what does not exist.

## How it works

1. Reads the project (code, configs, existing READMEs) to learn what it really has.
2. Shows a plan: which sections of the skeleton will be filled in, which will be left out and why, and what is still unknown.
3. Writes the README only after your explicit confirmation.
4. Writes the README in Portuguese with an English mirror, and checks it against `references/checklist-qualidade.md`.

## Expected input

The project path. If it is not given, the skill asks, never infers. The member list comes from a sibling README, from `CLAUDE.md` or from what you tell it, and without any of those the skill asks.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` plus reference files.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Glob`, `Write`, `Edit` and `AskUserQuestion` tools.

</details>
