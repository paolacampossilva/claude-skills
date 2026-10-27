---
name: synch-bilingual-readmes
description: Audits every README.md in a project (any depth) for PT-BR/EN bilingual completeness and synchronization, then translates/fixes what's missing or out of sync directly — no confirmation pause, since it only mirrors existing PT-BR content into English rather than inventing new content. Use when the user asks to check, audit, sync, or fix bilingual READMEs across a project, or asks whether all READMEs have both a Portuguese and English version.
when_to_use: Audits and syncs translations across every README already in the project tree, and fixes directly. It does not write a README from scratch.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
argument-hint: "[caminho do projeto]"
arguments:
  - project_path
context: inline
---

# Synch Bilingual READMEs

Audita todo `README.md` de um projeto (qualquer profundidade) atrás de
paridade PT-BR/EN, e corrige diretamente o que faltar ou estiver
dessincronizado — sem pausa de confirmação, porque só espelha conteúdo que já
existe em português, nunca inventa fato novo.

## Inputs

- `$project_path`: caminho do projeto a auditar. Se não vier como argumento,
  **sempre perguntar** com `AskUserQuestion` — nunca inferir silenciosamente
  do contexto da conversa (arquivo aberto, diretório atual, etc.), mesmo
  quando parece óbvio.

## Goal

Ao final, todo `README.md` de `$project_path` (exceto pastas de dependência)
tem um bloco PT-BR e um bloco EN de verdade, com o mesmo número/ordem de
seções e as mesmas entidades concretas (comandos, variáveis, endpoints,
números) dos dois lados — e um relatório final lista o que foi encontrado e o
que foi corrigido em cada arquivo.

## Steps

### 1. Descobrir todos os README.md

Buscar recursivamente a partir de `$project_path` por qualquer `README.md`,
excluindo pastas de dependência/cache que não são documentação do próprio
projeto: `.venv`, `venv`, `node_modules`, `site-packages`, `.pytest_cache`,
`.git`, `__pycache__`, e qualquer padrão equivalente que aparecer (ex.: outros
ambientes virtuais nomeados `.venv-*`).

```bash
find "$project_path" -iname "README.md" \
  -not -path "*/.venv*/*" -not -path "*/venv/*" \
  -not -path "*/node_modules/*" -not -path "*/site-packages/*" \
  -not -path "*/.pytest_cache/*" -not -path "*/.git/*" \
  -not -path "*/__pycache__/*"
```

**Success criteria**: lista completa de READMEs reais do projeto, sem nenhum
arquivo de dependência vendorizada misturado.

### 2. Triar quem não tem bloco EN nenhum

Antes de abrir cada arquivo por completo, rodar uma triagem rápida sobre
todos os READMEs encontrados:

```bash
grep -rL '🇺🇸' <lista de READMEs do passo 1>
```

Todo README que aparecer nessa saída já está classificado como **sem bloco
EN** — vai direto para o passo 4, sem precisar de leitura completa só para
classificar. Os que não aparecerem podem ter os dois blocos (sincronizados
ou não) e seguem para o passo 3.

**Success criteria**: nenhum README sem bloco EN consumiu uma leitura
completa só para chegar a essa conclusão.

### 3. Classificar e verificar sincronia (estrutural + conteúdo)

Para cada README que passou pela triagem do passo 2, ler o arquivo por
completo e seguir `references/deteccao-e-sincronia.md` (classificação de
estado, verificação estrutural de seções e verificação de conteúdo por
entidades concretas). Se o projeto tiver muitos READMEs (mais de ~5-6),
lançar agentes em paralelo (tool `Agent`, um grupo de arquivos por agente)
em vez de processar tudo sequencialmente.

**Success criteria**: cada README tem um status final (já ok / fora de
sincronia) com evidência concreta e apontável (ex.: "seção 'Variáveis de
ambiente': PT-BR cita `STORAGE_PATH`, EN não cita") — nunca uma
impressão vaga de que "parece diferente".

### 4. Corrigir

Seguir a seção "Corrigindo" de `references/deteccao-e-sincronia.md` — PT-BR é
sempre a fonte da verdade; para README sem bloco EN (passo 2), criar o mirror
completo; para README dessincronizado (passo 3), editar só o bloco EN para
fechar a divergência encontrada.

**Success criteria**: depois da edição, rodar a verificação estrutural de novo
em cada arquivo tocado e confirmar que os dois lados batem.

### 5. Reportar

Listar cada README encontrado (caminho relativo a `$project_path`) com um
status final: ✅ já estava sincronizado / 🆕 mirror EN criado do zero / 🔧
sincronizado (e o que mudou, resumidamente). Esse relatório é o retorno desta
skill para a conversa que a invocou.

**Success criteria**: quem lê o relatório sabe exatamente quais arquivos foram
tocados e por quê, sem precisar abrir cada diff para entender o motivo.

## Regras gerais

- **Nunca inventar** conteúdo novo — esta skill só traduz/sincroniza o que já
  existe em PT-BR, nunca decide o que um README "deveria" dizer.
- **Nunca reescrever ou mudar o sentido** do PT-BR original — ele é a fonte da
  verdade; a skill só ajusta o EN para acompanhá-lo.
- Comandos, nomes de variável, nomes de arquivo e URLs nunca são traduzidos —
  só o texto explicativo ao redor.
- Excluir sempre pastas de dependência/cache da varredura (passo 1) — um
  `README.md` de uma lib de terceiros instalada não é documentação do projeto.
- Se um README estiver claramente incompleto ou incorreto **em português**
  (não é uma questão de tradução, é o conteúdo original que está errado), isso
  fica fora do escopo desta skill — reportar no passo 5 como observação, mas
  não tentar consertar (isso é edição manual direta).
