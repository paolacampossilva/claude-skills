---
name: check-skills
description: Lists the user's personal skills — the ones they authored themselves, in ~/.claude/skills/ (global) and in the current project's .claude/skills/ (project-level) — with a one-line summary of what each one does, excluding Anthropic's own built-in/bundled skills, and flags when one skill hands off to another so the user doesn't run both manually for the same task. Use when the user asks what skills they have, which skills they made/created (e.g. "quais são minhas skills", "que skills eu tenho/criei"), or wants an inventory of their custom skills.
allowed-tools: Read, Glob, Bash, Agent
context: inline
---

# Check Skills

Lista as skills pessoais do usuário (globais e/ou do projeto atual), com um
resumo curto do que cada uma faz — sem misturar com as skills embutidas da
Anthropic (`pptx`, `docx`, `xlsx`, `pdf`, `dataviz`, `code-review`,
`artifact-design`, etc.), que não são criações do usuário.

## Goal

Ao final, o usuário recebe uma lista organizada (globais vs. deste projeto)
de só as skills que ele mesmo escreveu, cada uma com um resumo de 1-2 linhas
do que faz — nada de skill embutida do Claude Code misturada na lista.

## Steps

### 1. Descobrir skills globais e do projeto atual

Numa única chamada (as duas listas são independentes entre si), e já em
paralelo com o `grep` de tags de relação do passo 3, já que nenhum dos dois
depende do outro:

```bash
find ~/.claude/skills .claude/skills -mindepth 1 -maxdepth 1 -type d 2>/dev/null
```

Isso já separa por prefixo de caminho o que é global (`~/.claude/skills/...`)
do que é deste projeto (`.claude/skills/...`, só existe se a sessão estiver
dentro de um projeto com essa pasta). Para cada subpasta encontrada, ler
`<caminho>/<nome>/SKILL.md`.

**Success criteria**: lista completa de pastas com `SKILL.md`, já separada
entre globais e deste projeto.

### 2. Filtrar skills embutidas (built-in)

Excluir das duas listas qualquer pasta cujo nome bata com uma skill padrão
da Anthropic que às vezes é materializada localmente ao ser usada, mesmo sem
o usuário tê-la criado: `pptx`, `docx`, `xlsx`, `pdf`, e qualquer outra que
aparecer claramente como skill oficial de manipulação de arquivo de escritório
(mesmo padrão de nome curto + descrição genérica de formato de arquivo, sem
nada específico do usuário/projeto). Na dúvida sobre uma pasta específica,
perguntar ao usuário em vez de incluir ou excluir por conta própria.

**Success criteria**: a lista final não contém nenhuma skill que o usuário
não tenha escrito — só as autorais.

### 3. Detectar relações entre skills

Primeiro, checar a tag `[Uses → x]` / `[Used by ← x]` no início da
`description` de cada skill (convenção de marcação de relações) —
quando existe, já é a resposta, não precisa inferir nada:

```bash
grep -noE "\[(Uses → |Used by ← )[a-z0-9-]+\]" ~/.claude/skills/*/SKILL.md .claude/skills/*/SKILL.md 2>/dev/null
```

(sem âncora `^` — a tag fica indentada dentro do bloco YAML `description: >-`,
não no início literal da linha.)

Para skills sem essa tag, ou para confirmar se uma menção em prosa é handoff
real ou só relação de escopo, seguir `references/relacoes-entre-skills.md`.

**Success criteria**: para cada par de skills que se mencionam, sei se é uma
cadeia de handoff (A aciona B) ou uma relação de escopo/irmandade (A e B são
independentes) — nenhuma menção cruzada fica sem classificar.

### 4. Resumir e reportar

Para cada skill pessoal restante, extrair do frontmatter (`name` e
`description`/`when_to_use`) um resumo de 1-2 linhas em português do que ela
faz. Se houver muitas skills pessoais (mais de ~5-6), lançar agentes em
paralelo (tool `Agent`, um grupo de skills por agente) em vez de ler os
`SKILL.md` um a um. Agrupar o relatório em duas seções:

- **Globais** (`~/.claude/skills/`) — disponíveis em qualquer projeto.
- **Deste projeto** (`<caminho>/.claude/skills/`) — só aqui.

Se a mesma skill (mesmo nome) existir nos dois lugares ao mesmo tempo,
sinalizar isso explicitamente como duplicata em vez de listar as duas
silenciosamente.

Para toda cadeia de handoff encontrada no passo 3, anotar isso junto da skill
"de entrada" (a que o usuário chamaria primeiro), no formato: "aciona
automaticamente `<skill-B>` ao final — não precisa rodar `<skill-B>`
separadamente para a mesma tarefa". Não é necessário repetir o aviso do lado
da skill "de saída" (`<skill-B>`), só sinalizar lá que ela normalmente roda
via handoff de `<skill-A>`, e também pode ser chamada direto quando o
conteúdo já está pronto.

**Success criteria**: o usuário consegue ver, em poucas linhas por skill, o
que cada uma faz, onde ela mora (global vs. projeto), e — quando existir —
que ela faz parte de uma cadeia com outra skill, sem precisar abrir nenhum
arquivo nem correr o risco de rodar as duas manualmente para a mesma tarefa.

## Regras gerais

- Nunca listar skills embutidas do Claude Code (as que não têm pasta em
  lugar nenhum do disco, como `dataviz`, `code-review`, `artifact-design`,
  `security-review`, etc.) — elas não aparecem em `~/.claude/skills/` nem em
  `.claude/skills/` do projeto, então já ficam fora naturalmente.
- Não abrir nem resumir arquivos de referência/scripts internos da skill
  (`references/`, `scripts/`, `assets/`) — só o `SKILL.md` é necessário para
  o resumo.
- Resumo é sempre condensado (1-2 linhas) — não copiar a `description`
  inteira do frontmatter, que costuma ser longa e voltada para o mecanismo de
  descoberta de skills, não para leitura humana direta.
- Nunca reportar duas skills em cadeia de handoff (passo 3) como se fossem
  totalmente independentes — o ponto de detectar a relação é evitar que o
  usuário rode manualmente as duas para a mesma tarefa e duplique trabalho.
