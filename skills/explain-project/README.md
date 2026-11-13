<details open>
<summary><b>🇧🇷 pt-br</b> — explain-project</summary>
<br>

# explain-project

Skill do Claude que escreve um `.md` didático em duas camadas: primeiro a explicação sem jargão, depois uma seção avançada com os termos técnicos.

## Por quê

Para uma reunião de sprint ou para decidir o que fazer com um processo novo, é preciso entender e explicar o assunto para quem não é da área. A skill produz esse material a partir do projeto ou do processo.

## Como funciona

1. Escolhe o modo: **retrospectivo** (o que você fez, mais uma visão geral do projeto e do andamento, com roteiro de fala individual ou pelo time todo) ou **processo novo** (o que é o processo, riscos e as decisões que cabem a você, com opções e recomendação).
2. Lê a fonte inteira antes de escrever, com agentes em paralelo quando o volume é grande. Autoria vem do `git log` e dos relatórios, nunca de suposição.
3. Grava o `.md` na pasta de destino e avisa o caminho e os pontos a conferir, sem despejar o documento no chat.

## Entrada esperada

Modo, fonte (projeto, pasta, task ou texto), no retrospectivo a parte de quem e o escopo da fala, e o destino (a pasta e se o documento é só pessoal ou compartilhado com o time). O texto sai sempre em terceira pessoa, exceto o roteiro de fala. O que faltar, a skill pergunta, nunca infere. Só roda quando chamada pelo nome.

## Rodando os scripts diretamente

Não há scripts. A skill é um `SKILL.md`.

## Usando como skill do Claude

Copie esta pasta para `~/.claude/skills/` (ou para `.claude/skills/` de um projeto), ou envie como skill personalizada. As instruções dentro do `SKILL.md` estão em português.

## Stack

Arquivos Markdown de skill. Em execução usa `Read`, `Glob`, `Bash` (leitura de `git log`), `Write`, `AskUserQuestion` e `Agent`.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — explain-project</summary>
<br>

# explain-project

A Claude skill that writes a didactic `.md` in two layers: plain language first, then an advanced section with the technical terms.

## Why

For a sprint meeting or to decide what to do with a newly arrived process, you need to understand the subject and explain it to people outside the field. The skill produces that material from the project or the process.

## How it works

1. Picks the mode: **retrospective** (what you did, plus an overview of the project and its progress, with a speaking script for you alone or for the whole team) or **new process** (what the process is, risks and the decisions that are yours, with options and a recommendation).
2. Reads the whole source before writing, with parallel agents when the volume is large. Authorship comes from `git log` and reports, never from assumption.
3. Saves the `.md` in the destination folder and reports the path and the points to check, without dumping the document in the chat.

## Expected input

Mode, source (project, folder, task or text), in retrospective whose part it is and the speaking scope, and the destination (the folder, and whether the document is private or shared with the team). The text is always written in third person, except the speaking script. Anything missing is asked, never inferred. It only runs when called by name.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses `Read`, `Glob`, `Bash` (reading `git log`), `Write`, `AskUserQuestion` and `Agent`.

</details>
