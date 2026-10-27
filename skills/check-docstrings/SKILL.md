---
name: check-docstrings
description: Audits a Python project's docstrings and comments for two things — (1) are they written in English, translating directly when they aren't, and (2) are they up to date with what the function/file/code actually does. Language fixes apply immediately; staleness fixes are only applied after user confirmation. Use when the user asks to check, audit, or fix docstrings/comments for language or staleness across a project.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent, AskUserQuestion
argument-hint: "[caminho do projeto]"
arguments:
  - project_path
context: inline
---

# Check Docstrings

Audita todo arquivo Python de um projeto atrás de duas coisas nas docstrings
e comentários: estão em inglês, e ainda descrevem corretamente o que o código
faz. Corrige idioma na hora; corrige desatualização só depois de confirmação.

## Inputs

- `$project_path`: caminho do projeto a auditar. Se não vier como argumento,
  **sempre perguntar** com `AskUserQuestion` — nunca inferir silenciosamente
  do contexto da conversa (arquivo aberto, diretório atual, etc.), mesmo
  quando parece óbvio.

## Goal

Ao final, toda docstring e comentário `#` de `$project_path` (exceto
dependências/cache) está em inglês, e todo problema concreto de desatualização
encontrado foi reportado e — para os aprovados pelo usuário — corrigido. Um
relatório final resume o que foi feito.

## Steps

### 1. Descobrir arquivos Python

Buscar recursivamente `*.py` a partir de `$project_path`, excluindo pastas de
dependência/cache: `.venv`, `.venv-*`, `venv`, `node_modules`, `site-packages`,
`__pycache__`, `.git`, `.pytest_cache`. Considerar excluir também
`migrations/`/`alembic/versions/` se existirem (código majoritariamente
gerado — confirmar com o usuário se não tiver certeza).

```bash
find "$project_path" -iname "*.py" \
  -not -path "*/.venv*/*" -not -path "*/venv/*" \
  -not -path "*/node_modules/*" -not -path "*/site-packages/*" \
  -not -path "*/__pycache__/*" -not -path "*/.git/*" \
  -not -path "*/.pytest_cache/*"
```

**Success criteria**: lista completa de arquivos Python autorais do projeto,
sem nenhuma dependência vendorizada misturada.

### 2. Extrair, classificar idioma e comparar com o código

Para cada arquivo, ler o conteúdo e identificar: docstrings de módulo, classe,
função/método (`"""..."""`/`'''...'''` logo após a assinatura), e comentários
de linha (`#`). Para projetos grandes, lançar agentes em paralelo (tool
`Agent`, um grupo de arquivos por agente) em vez de processar tudo
sequencialmente — mesmo padrão usado nas skills irmãs.

Sobre o mesmo conteúdo já lido, sem reabrir o arquivo: (a) aplicar a
heurística de `references/deteccao-idioma.md` em cada docstring/comentário
para classificar como português ou inglês; (b) comparar cada docstring com o
código real da função/classe que ela documenta, usando as checagens concretas
de `references/deteccao-desatualizado.md` (Args/Returns/Raises desalinhados,
comentário referenciando código removido, TODO já resolvido, etc.) — só
sinalizar divergência concreta e apontável, nunca preferência de estilo ou
paráfrase.

**Success criteria**: cada docstring/comentário está associado a arquivo,
linha e função/classe (se aplicável), com uma classificação de idioma (sem
confundir código de exemplo/identificadores em português com prosa a
traduzir) e, quando houver, uma divergência de desatualização com citação
lado a lado ("a doc diz X, o código faz Y") — tudo derivado de uma única
leitura do arquivo, nada baseado em impressão vaga.

### 3. Corrigir idioma (imediato, sem pausa)

Para cada docstring/comentário classificado como português, traduzir para
inglês preservando sentido, formato Google-style (se houver) e tudo que não
deve ser traduzido (identificadores, exemplos de código, valores literais —
ver `references/deteccao-idioma.md`), e aplicar com `Edit` direto.

**Success criteria**: nenhuma docstring/comentário do projeto continua em
português depois deste passo.

### 4. Reportar e confirmar

Juntar todos os achados de desatualização do passo 2 (de todos os arquivos)
num resumo único: arquivo, função/linha, divergência, correção proposta.
Mostrar ao usuário antes de tocar em qualquer um. Se a lista for grande, usar
`AskUserQuestion` para decidir o escopo (aplicar todas / revisar uma a uma /
nenhuma) em vez de assumir.

**Success criteria**: usuário aprovou explicitamente quais correções de
desatualização aplicar — nunca aplicar direto, mesmo quando a divergência
parece óbvia (diferente do passo 3, que é automático).

### 5. Aplicar as correções aprovadas

Editar (`Edit`) só as divergências que o usuário aprovou no passo 4.

**Success criteria**: cada edição aplicada corresponde exatamente a um item
que apareceu no resumo aprovado — nada além disso.

### 6. Relatório final

Resumir: quantos arquivos escaneados, quantas traduções de idioma aplicadas
(passo 3), quantas divergências de desatualização encontradas/corrigidas/
deixadas de fora (passos 2, 4 e 5).

**Success criteria**: quem lê o relatório sabe exatamente o que mudou no
código e por quê, sem precisar reabrir cada diff.

## Regras gerais

- **Nunca traduzir** identificadores, exemplos de código, valores literais ou
  nomes de contrato externo (campo de API/banco em português) — só a prosa
  explicativa (ver `references/deteccao-idioma.md`).
- **Nunca marcar divergência de estilo como desatualização** — só fatos
  concretos e verificáveis (ver `references/deteccao-desatualizado.md`).
- **Idioma corrige direto; desatualização sempre pede confirmação primeiro** —
  são níveis de risco diferentes, não tratar do mesmo jeito.
- Esta skill não cobre formatação/padrão Google-style em si (se toda função
  tem `Args`/`Returns`) nem linguagens além de Python — isso é convenção de
  estilo separada, fora do escopo aqui.
