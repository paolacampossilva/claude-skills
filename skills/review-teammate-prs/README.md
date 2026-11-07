<details open>
<summary><b>🇧🇷 pt-br</b> — review-teammate-prs</summary>
<br>

# review-teammate-prs

Skill do Claude que acha os PRs dos colegas (abertos ou já mergeados) que ainda não têm a sua aprovação, revisa cada um e entrega rascunhos de comentário e os comandos `gh pr review`.

## Por quê

PRs se acumulam, e alguns são mergeados sem revisão de colega. A skill faz o levantamento e uma revisão com o mesmo checklist em todos, para a aprovação deixar de ser "li por cima".

## Como funciona

1. Atualiza os repositórios (`git pull --ff-only`, pulando árvore suja) e lista os PRs dos handles informados em que o revisor não tem review `APPROVED`.
2. Revisa cada PR: o que o título diz, testes, segredo ou dado pessoal no diff, legibilidade, design e se o "Como testar" reproduz. Diff acima de 20 mil linhas é conferido por hash de árvore, e testes rodam só num worktree descartável.
3. Decide `APROVAR` ou `PEDIR MUDANÇAS`. Bloqueio vira pergunta, nunca aprovação em silêncio.
4. Entrega uma tabela-resumo, um rascunho de comentário por PR (impessoal, sem saudação nem `@menção`) e um bloco único de `gh pr review`. **Nunca posta, aprova nem faz merge sozinha.**

## Entrada esperada

`handles=` (handles do GitHub dos colegas), `repos=` (repositórios locais), `reviewer=` (padrão: o usuário do `gh`) e `desde=` (data inicial, opcional). Sem `handles` ou `repos`, a skill pergunta, nunca infere. Exemplo: `/review-teammate-prs handles=fulano,ciclana repos=~/Code/api,~/Code/web`.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md`.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa `Bash` (`gh` e `git` de leitura), `Read` e `AskUserQuestion`. Exige o GitHub CLI (`gh`) autenticado.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — review-teammate-prs</summary>
<br>

# review-teammate-prs

A Claude skill that finds teammates' PRs (open or already merged) that do not have your approval yet, reviews each one and delivers draft comments and the `gh pr review` commands.

## Why

PRs pile up, and some get merged without a teammate's review. The skill does the survey and reviews every PR with the same checklist, so an approval stops meaning "skimmed it".

## How it works

1. Updates the repositories (`git pull --ff-only`, skipping dirty trees) and lists the PRs of the given handles where the reviewer has no `APPROVED` review.
2. Reviews each PR: what the title says, tests, secrets or personal data in the diff, readability, design and whether the "Como testar" section reproduces. Diffs over 20 thousand lines are checked by tree hash, and tests run only in a disposable worktree.
3. Decides `APROVAR` or `PEDIR MUDANÇAS`. A blocker becomes a question, never a silent approval.
4. Delivers a summary table, one draft comment per PR (impersonal, no greeting or `@mention`) and a single block of `gh pr review`. **It never posts, approves or merges by itself.**

## Expected input

`handles=` (teammates' GitHub handles), `repos=` (local repositories), `reviewer=` (default: the `gh` user) and `desde=` (start date, optional). Without `handles` or `repos` the skill asks, never infers. Example: `/review-teammate-prs handles=fulano,ciclana repos=~/Code/api,~/Code/web`.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses `Bash` (read-only `gh` and `git`), `Read` and `AskUserQuestion`. Requires an authenticated GitHub CLI (`gh`).

</details>
