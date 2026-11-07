---
name: create-main-readme
description: Creates or fixes a project's main/root README.md, following the section skeleton of a rich reference README (Sumário, Tecnologias, Pré-requisitos, Instalação, Executando, Estrutura de pastas, one detailed section per module/service, Variáveis de ambiente, Testes, Tipos de commit, full PT-BR/EN bilingual mirror) while adapting each section's content to whatever the target project actually is (LangGraph, Streamlit, FastAPI, JS frontend, etc. — never inventing what doesn't exist). Use when the user asks to create, write, fix, update, or review the main/root README.md of a project, module, or squad folder.
when_to_use: Not for per-service READMEs inside a project — that's a narrower task; only repeat per folder if explicitly asked.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent, AskUserQuestion
argument-hint: "[caminho do projeto]"
arguments:
  - project_path
context: inline
---

# Create Main README

Cria ou corrige o README principal (raiz) de um projeto — sempre investigando
primeiro, sempre mostrando um plano antes de escrever, nunca inventando conteúdo
que não existe no código.

## Inputs

- `$project_path`: caminho do projeto/pasta cujo README principal deve ser
  criado ou corrigido. Se não vier como argumento, **sempre perguntar** com
  `AskUserQuestion` — nunca inferir silenciosamente do contexto da conversa
  (arquivo aberto no IDE, diretório de trabalho atual), mesmo quando parece
  óbvio qual projeto é.

## Goal

Produzir um README principal completo, preciso (nada inventado, tudo conferido
contra o código real) e bilíngue (PT-BR/EN, mirror completo — ver
`references/checklist-qualidade.md`), seguindo o esqueleto de seções descrito
em `references/estrutura-readme.md`, com o *conteúdo* de cada seção adaptado
à stack real de `$project_path` (LangGraph, Streamlit, FastAPI, frontend JS,
CLI, pipeline único, etc. — o esqueleto é fixo, o conteúdo não).

## Steps

### 1. Localizar, ler o que já existe e decidir o que preservar

Encontrar o README raiz de `$project_path` (`README.md` na raiz da pasta —
não confundir com READMEs de submódulos/serviços dentro dela). Se existir,
ler por completo.

Sobre o mesmo conteúdo já lido: se já existirem seções fora do esqueleto
padrão (decisões de engenharia narradas, troubleshooting específico,
comparações de modelo, qualquer coisa que documente uma escolha real do
projeto), essas seções **não são lixo a descartar** só por não baterem com o
template. Decidir, para cada uma: incorporar dentro da seção do esqueleto
mais próxima, ou manter como seção extra fora do esqueleto.

**Success criteria**: sei se estou criando do zero, corrigindo lacunas pontuais,
ou lidando com algo fora do padrão (arquivo corrompido/ilegível, stub muito
curto, seção "EN" que na verdade não traduz nada — ver checklist item 1); e
nada que documentava uma decisão real do projeto foi perdido silenciosamente
na reescrita.

### 2. Investigar o projeto

Ler o que for necessário para preencher cada seção do esqueleto com precisão:
manifests de dependência (`requirements.txt`, `package.json`, `pyproject.toml`,
etc.), `docker-compose.yml`/`Dockerfile`(s), `.env.example`, estrutura real de
pastas (`ls`/`find`/`Glob`), scripts/entrypoints executáveis, suíte de testes,
CLIs. Para um projeto grande (muitos módulos/serviços), lançar agentes Explore
em paralelo por área em vez de ler tudo sequencialmente — mesmo padrão de
investigação usado para revisar README de multi-serviço.

**Success criteria**: para cada seção do esqueleto (`references/estrutura-readme.md`),
sei se tenho informação real suficiente para escrevê-la ou preciso perguntar ao
usuário — nunca decido "provavelmente é assim" sobre comando, endpoint ou
variável de ambiente sem ter lido o código correspondente.

### 3. Montar o plano e confirmar com o usuário

Antes de escrever qualquer coisa, apresentar um resumo: quais seções do
esqueleto serão preenchidas/corrigidas, quais serão omitidas (e por quê — ex.:
"esse projeto não tem múltiplos módulos, então não haverá seção 'Fluxo N' por
módulo, só uma visão geral única"), e o que ainda falta saber (alguma decisão
que não dá pra inferir do código — usar `AskUserQuestion` para isso). A seção
"Integrantes" vem de um README irmão, do CLAUDE.md ou do que o usuário
informar; sem nenhuma dessas fontes, perguntar com `AskUserQuestion`. Só prosseguir depois de
confirmação explícita.

**Success criteria**: o usuário aprovou o plano antes de qualquer `Write`/`Edit`
no README de verdade — nunca escrever direto, mesmo quando a lacuna parece
óbvia.

### 4. Escrever

Escrever (`Write` para um README novo, `Edit` com diffs pontuais para corrigir
um existente) seguindo o esqueleto de `references/estrutura-readme.md` e o
formato bilíngue de dois blocos `<details>` (PT-BR aberto por padrão, EN
fechado), com a tabela de tipos de commit ao final de cada bloco de idioma —
mesmo padrão já usado nos READMEs deste ecossistema.

### 5. Verificar

Rodar o checklist completo de `references/checklist-qualidade.md` (paridade
PT/EN por contagem de seções, blocos de código e `<details>` balanceados,
links internos resolvendo, âncoras do Sumário batendo com os títulos finais,
nenhuma seção inventada, conteúdo próprio preservado) antes de reportar a
tarefa como concluída.

**Success criteria**: um programador novo lendo o README em qualquer um dos
dois idiomas tem a mesma informação, e nenhuma afirmação nele foi inventada.

## Regras gerais

- **Nunca inventar** seção, comando, endpoint ou variável de ambiente sem fonte
  no código. Se não tiver certeza, perguntar em vez de supor.
- Todo comando citado no README precisa ter sido conferido contra o código real
  (script, `Dockerfile`, `cli/main.py`, etc.) antes de entrar no texto — nunca
  copiado de outro projeto por analogia.
- Se já existe um README, preferir **consertar/completar com diffs pontuais** a
  reescrever do zero — preserva histórico de git e conteúdo bespoke (ver Step 1).
- Escopo é sempre um README principal por vez, o de `$project_path` — esta
  skill não varre o repositório inteiro nem mexe em READMEs de módulo/serviço
  dentro do projeto, a menos que explicitamente pedido de novo para cada um.
