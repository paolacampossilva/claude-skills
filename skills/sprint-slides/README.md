<details open>
<summary><b>🇧🇷 pt-br</b> — sprint-slides</summary>
<br>

# sprint-slides

Skill do Claude que planeja o *conteúdo* de uma apresentação de fim de sprint a partir de uma pasta de projeto, em linguagem que um público misto, não técnico, acompanha.

## Por quê

Transformar "tudo o que fizemos" em slides que quem não é de computação entende exige cortar detalhe de implementação sem perder precisão. A skill monta o roteiro slide a slide e só depois passa para a geração do arquivo.

## Como funciona

1. Lê tudo da pasta (código, `.md` de tasks, PDFs, imagens), com agentes em paralelo quando há muitos arquivos.
2. Escreve o roteiro slide a slide, rico o bastante para a `template-slides` montar o deck quase só com ele.
3. Mostra o roteiro no chat e só segue depois da sua aprovação.
4. Passa o roteiro aprovado para a `template-slides`, que gera o `.pptx`.

## Entrada esperada

O caminho da pasta. Se não for informado, a skill pergunta, nunca infere. O número da sprint, se não aparecer na pasta, também é perguntado. Só roda quando chamada pelo nome.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md`.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa `Read`, `Glob`, `Bash`, `AskUserQuestion` e `Agent`. Depende da skill `template-slides` para gerar o arquivo, então use as duas juntas.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — sprint-slides</summary>
<br>

# sprint-slides

A Claude skill that plans the *content* of an end-of-sprint presentation from a project folder, in language a mixed, non-technical audience can follow.

## Why

Turning "everything we did" into slides that non-computing people understand means cutting implementation detail without losing accuracy. The skill builds a slide-by-slide outline and only then hands off to file generation.

## How it works

1. Reads everything in the folder (code, task `.md` files, PDFs, images), with parallel agents when there are many files.
2. Writes the slide-by-slide outline, rich enough for `template-slides` to build the deck almost entirely from it.
3. Shows the outline in the chat and continues only after your approval.
4. Hands the approved outline to `template-slides`, which generates the `.pptx`.

## Expected input

The folder path. If it is not given, the skill asks, never infers. The sprint number, if it is not in the folder, is also asked. It only runs when called by name.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses `Read`, `Glob`, `Bash`, `AskUserQuestion` and `Agent`. It depends on the `template-slides` skill to generate the file, so use the two together.

</details>
