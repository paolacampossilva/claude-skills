<details open>
<summary><b>🇧🇷 pt-br</b> — check-skills</summary>
<br>

# check-skills

Skill do Claude que lista as skills que você mesmo escreveu e mostra quais delegam trabalho a outra skill.

## Por quê

Saber à mão quais skills pessoais existem, o que cada uma faz e quais chamam outras exige abrir cada `SKILL.md`. Esta skill monta esse inventário.

## Como funciona

1. Encontra as pastas de skills em `~/.claude/skills/` (globais) e em `.claude/skills/` do projeto atual (do projeto).
2. Descarta as pastas que batem com skills embutidas da Anthropic (`pptx`, `docx`, `xlsx`, `pdf` e semelhantes). Se tiver dúvida sobre uma pasta, pergunta.
3. Procura relações entre skills: primeiro as tags `[Uses → x]` e `[Used by ← x]` no início da `description`, depois menções no corpo de cada `SKILL.md`, classificadas com `references/relacoes-entre-skills.md` como delegação real ou apenas escopo relacionado.
4. Imprime um resumo curto por skill, agrupado em globais e do projeto. A skill que aciona outra é marcada, para você não rodar as duas na mesma tarefa. Skill que existe nos dois lugares é sinalizada como duplicata.

## Entrada esperada

Nenhuma. Ela lê os dois diretórios de skills acima.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md` mais um arquivo de referência.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. Depois pergunte ao Claude quais skills você tem ou criou. O arquivo da skill não a restringe a ser chamada pelo nome.

As instruções dentro do `SKILL.md` estão em português, e os resumos que ela produz também.

## Stack

Arquivos Markdown de skill. Em execução usa as ferramentas `Read`, `Glob`, `Bash` e `Agent` do Claude Code, e os comandos de shell `find` e `grep`.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — check-skills</summary>
<br>

# check-skills

A Claude skill that lists the skills you wrote yourself and shows which ones hand off to another skill.

## Why

Keeping track by hand of which personal skills exist, what each one does, and which ones call each other means opening every `SKILL.md`. This skill produces that inventory.

## How it works

1. Finds the skill folders in `~/.claude/skills/` (global) and in the current project's `.claude/skills/` (project-level).
2. Drops folders that match Anthropic's bundled skills (`pptx`, `docx`, `xlsx`, `pdf` and similar). If it is unsure about a folder, it asks.
3. Looks for relations between skills: first the `[Uses → x]` and `[Used by ← x]` tags at the start of a `description`, then mentions in the body of each `SKILL.md`, classified with `references/relacoes-entre-skills.md` as a real handoff or only a related scope.
4. Prints a short summary per skill, grouped into global and project-level. A skill that triggers another one is marked, so you do not run both for the same task. A skill that exists in both places is flagged as a duplicate.

## Expected input

None. It reads the two skill directories above.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file plus one reference file.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Then ask Claude which skills you have or created. The skill file does not restrict it to being called by name.

The instructions inside `SKILL.md` are written in Portuguese, and the summaries it produces are in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Glob`, `Bash` and `Agent` tools, and the shell commands `find` and `grep`.

</details>
