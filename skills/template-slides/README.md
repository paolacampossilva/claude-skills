<details open>
<summary><b>🇧🇷 pt-br</b> — template-slides</summary>
<br>

# template-slides

Skill do Claude que gera um deck PowerPoint (`.pptx`) numa identidade visual fixa de apresentação de time: azul-marinho e verde-água, cards numerados e destaque "Resultado".

## Por quê

Manter o mesmo visual em todo deck de sprint à mão é repetitivo. A skill só cuida do visual, e o conteúdo vem pronto (de você ou da skill `sprint-slides`).

## Como funciona

1. Recebe o conteúdo pronto e confere o que falta: número da sprint, nome do time, integrantes, orientadores e logos.
2. Gera um script de build (com `pptxgenjs`, ou `python-pptx` se a skill `pptx` não estiver instalada) seguindo `references/design-system.md`. Capa e agradecimentos têm layout fixo e nunca são redesenhados.
3. Valida o arquivo, confere estouro de texto e colisão de cards, e salva o `.pptx` junto do script de build, para ajustes futuros regenerarem no lugar.

## Entrada esperada

Conteúdo dos slides, número da sprint, nome do time, integrantes, orientadores e até três logos (caminhos de arquivo que você fornece, não vêm na skill). O que faltar, a skill pergunta, nunca infere. Só roda quando chamada pelo nome ou por um handoff aprovado da `sprint-slides`.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md` mais arquivos de referência.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill mais `references/design-system.md`. Em execução usa `pptxgenjs` (ou `python-pptx` como alternativa) e a skill `pptx`, quando instalada.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — template-slides</summary>
<br>

# template-slides

A Claude skill that generates a PowerPoint deck (`.pptx`) in a fixed team-presentation visual identity: navy and teal, numbered cards and a "Resultado" callout.

## Why

Keeping the same look in every sprint deck by hand is repetitive. The skill only handles the visuals, and the content arrives ready (from you or from the `sprint-slides` skill).

## How it works

1. Takes the finished content and checks what is missing: sprint number, team name, members, advisors and logos.
2. Generates a build script (with `pptxgenjs`, or `python-pptx` if the `pptx` skill is not installed) following `references/design-system.md`. The cover and the closing slide have a fixed layout and are never redesigned.
3. Validates the file, checks for text overflow and card collisions, and saves the `.pptx` next to its build script so later tweaks regenerate it in place.

## Expected input

Slide content, sprint number, team name, members, advisors and up to three logos (file paths you provide, they do not ship with the skill). Anything missing is asked, never inferred. It only runs when called by name or through an approved handoff from `sprint-slides`.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` plus reference files.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files plus `references/design-system.md`. At run time it uses `pptxgenjs` (or `python-pptx` as a fallback) and the `pptx` skill, when installed.

</details>
