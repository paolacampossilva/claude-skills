<details open>
<summary><b>🇧🇷 pt-br</b> — suggest-commits</summary>
<br>

# suggest-commits

Skill do Claude que analisa o que está pendente num repositório git e sugere uma sequência de commits agrupados por tipo e escopo, em Conventional Commits.

## Por quê

Quando as mudanças misturam assuntos (um `fix` junto com `docs`), separar em commits pequenos e bem nomeados dá trabalho. A skill lê o diff de verdade, agrupa e imprime os comandos prontos.

## Como funciona

1. Valida que o caminho é um repositório git e levanta a branch atual e os arquivos pendentes.
2. Lê o diff real de cada arquivo, em vez de classificar pela extensão.
3. Agrupa por escopo e por tipo (`feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`), sem misturar dois tipos nem dois escopos num commit.
4. Escreve a mensagem de cada commit em uma linha (`tipo(escopo): descrição`, em português) e imprime um bloco com `git add`, `git commit` e `git push`. **Nunca executa** `git add`, `git commit` nem `git push`.

## Entrada esperada

O caminho do repositório git. Se não for informado, a skill pergunta, nunca infere pelo diretório atual.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md`.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa `Bash` (só `git` de leitura), `AskUserQuestion` e `Agent`.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — suggest-commits</summary>
<br>

# suggest-commits

A Claude skill that analyzes what is pending in a git repository and suggests a sequence of commits grouped by type and scope, as Conventional Commits.

## Why

When changes mix concerns (a `fix` together with `docs`), splitting them into small, well-named commits is tedious. The skill reads the real diff, groups it and prints ready-to-run commands.

## How it works

1. Checks that the path is a git repository and collects the current branch and the pending files.
2. Reads the real diff of each file instead of classifying by extension.
3. Groups by scope and type (`feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`), never mixing two types or two scopes in one commit.
4. Writes each commit message on one line (`type(scope): description`, in Portuguese) and prints a block with `git add`, `git commit` and `git push`. **It never runs** `git add`, `git commit` or `git push`.

## Expected input

The git repository path. If it is not given, the skill asks, never infers it from the current directory.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses `Bash` (read-only `git`), `AskUserQuestion` and `Agent`.

</details>
