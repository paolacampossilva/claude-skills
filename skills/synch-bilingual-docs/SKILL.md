---
name: synch-bilingual-docs
description: Audita todo arquivo *.md dentro de uma pasta docs/ informada explicitamente (qualquer profundidade, incluindo subpastas) atrás de paridade PT-BR/EN, e corrige diretamente o que faltar ou estiver dessincronizado — sem pausa de confirmação, porque só espelha conteúdo que já existe em português. Assets não-markdown (csv/json/pdf/png) referenciados por esses docs ficam fora do escopo. Use when the user asks to check, audit, sync, or fix bilingual docs inside a specific docs/ folder.
when_to_use: Irmã de synch-bilingual-readmes (mesma convenção <details>, mesmo comportamento "PT-BR é fonte da verdade, corrige direto"), mas com escopo em docs/*.md em vez de README.md — as duas skills nunca tocam o mesmo arquivo.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit, Agent
argument-hint: "[caminho da pasta docs/]"
arguments:
  - docs_path
context: inline
---

# Synch Bilingual Docs

Audita todo arquivo `*.md` dentro de uma pasta `docs/` específica (qualquer
profundidade, incluindo subpastas dentro dela) atrás de paridade PT-BR/EN, e
corrige diretamente o que faltar ou estiver dessincronizado — sem pausa de
confirmação, porque só espelha conteúdo que já existe em português, nunca
inventa fato novo. Arquivos não-markdown (csv/json/pdf/png) que esses docs
referenciam por path relativo estão fora do escopo desta skill.

## Inputs

- `$docs_path`: caminho da pasta `docs/` a auditar. Se não vier como
  argumento, perguntar ao usuário — esta skill nunca varre um projeto atrás
  de pastas `docs/` sozinha, sempre recebe o caminho explícito.

## Goal

Ao final, todo `*.md` dentro de `$docs_path` (exceto pastas de dependência)
tem um bloco PT-BR e um bloco EN de verdade, com o mesmo número/ordem de
seções e as mesmas entidades concretas (comandos, variáveis, endpoints,
números, paths de arquivo — incluindo paths para csv/json/pdf/png
referenciados) dos dois lados — e um relatório final lista o que foi
encontrado e o que foi corrigido em cada arquivo.

## Steps

### 1. Descobrir todo *.md dentro de $docs_path

Buscar recursivamente dentro da própria `$docs_path`, cobrindo subpastas
aninhadas (ex. `docs/benchmarks/`), excluindo `README.md` (isso é
trabalho de `synch-bilingual-readmes`, não desta skill) e pastas de
dependência/cache que não são documentação do próprio projeto: `.venv`,
`venv`, `node_modules`, `site-packages`, `.pytest_cache`, `.git`,
`__pycache__`, e qualquer padrão equivalente que aparecer.

```bash
find "$docs_path" -type f -iname "*.md" \
  -not -iname "README.md" \
  -not -path "*/.venv*/*" -not -path "*/venv/*" \
  -not -path "*/node_modules/*" -not -path "*/site-packages/*" \
  -not -path "*/.pytest_cache/*" -not -path "*/.git/*" \
  -not -path "*/__pycache__/*"
```

**Success criteria**: lista completa de arquivos `.md` reais dentro de
`$docs_path`, sem `README.md` misturado e sem nenhum arquivo de dependência
vendorizada.

### 2. Triar quem não tem bloco EN nenhum

Antes de abrir cada arquivo por completo, rodar uma triagem rápida sobre
todos os arquivos encontrados:

```bash
grep -rL '🇺🇸' <lista de arquivos do passo 1>
```

Todo arquivo que aparecer nessa saída já está classificado como **sem bloco
EN** — vai direto para o passo 4, sem precisar de leitura completa só para
classificar. Os que não aparecerem podem ter os dois blocos (sincronizados
ou não) e seguem para o passo 3.

**Success criteria**: nenhum arquivo sem bloco EN consumiu uma leitura
completa só para chegar a essa conclusão.

### 3. Classificar e verificar sincronia (estrutural + conteúdo)

Para cada arquivo que passou pela triagem do passo 2, ler o arquivo por
completo e seguir
`../synch-bilingual-readmes/references/deteccao-e-sincronia.md` (arquivo de
referência compartilhado com a skill irmã — classificação de estado,
verificação estrutural de seções e verificação de conteúdo por entidades
concretas, incluindo paths de assets não-markdown referenciados). Se
`$docs_path` tiver muitos arquivos (mais de ~5-6), lançar agentes em paralelo
(tool `Agent`, um grupo de arquivos por agente) em vez de processar tudo
sequencialmente.

**Success criteria**: cada arquivo tem um status final (já ok / fora de
sincronia) com evidência concreta e apontável (ex.: "seção 'Resultados':
PT-BR cita `results.json`, EN não cita") — nunca uma
impressão vaga de que "parece diferente".

### 4. Corrigir

Seguir a seção "Corrigindo" de
`../synch-bilingual-readmes/references/deteccao-e-sincronia.md` — PT-BR é
sempre a fonte da verdade; para arquivo sem bloco EN (passo 2), criar o
mirror completo; para arquivo dessincronizado (passo 3), editar só o bloco EN
para fechar a divergência encontrada.

**Success criteria**: depois da edição, rodar a verificação estrutural de novo
em cada arquivo tocado e confirmar que os dois lados batem.

### 5. Reportar

Listar cada arquivo encontrado (caminho relativo a `$docs_path`) com um
status final: ✅ já estava sincronizado / 🆕 mirror EN criado do zero / 🔧
sincronizado (e o que mudou, resumidamente). Esse relatório é o retorno desta
skill para a conversa que a invocou.

**Success criteria**: quem lê o relatório sabe exatamente quais arquivos foram
tocados e por quê, sem precisar abrir cada diff para entender o motivo.

## Regras gerais

- **Nunca inventar** conteúdo novo — esta skill só traduz/sincroniza o que já
  existe em PT-BR, nunca decide o que um arquivo "deveria" dizer.
- **Nunca reescrever ou mudar o sentido** do PT-BR original — ele é a fonte da
  verdade; a skill só ajusta o EN para acompanhá-lo.
- Comandos, nomes de variável, nomes de arquivo e URLs nunca são traduzidos —
  só o texto explicativo ao redor. Isso inclui paths para arquivos
  não-markdown referenciados no texto (`.csv`, `.json`, `.pdf`, `.png`, ex.
  `comparison.csv`, `results.json`) — esses
  arquivos nunca são lidos, validados ou alterados por esta skill; o único
  cuidado é preservar o path exatamente igual no bloco EN.
- Se um arquivo encontrado se chamar literalmente `README.md`, pular —
  sincronizar READMEs é trabalho da skill `synch-bilingual-readmes`, não
  desta. Mantém as duas skills com escopos disjuntos mesmo quando
  `$docs_path` tiver um `README.md` dentro dela.
- Excluir sempre pastas de dependência/cache da varredura (passo 1).
- Se um arquivo estiver claramente incompleto ou incorreto **em português**
  (não é uma questão de tradução, é o conteúdo original que está errado), isso
  fica fora do escopo desta skill — reportar no passo 5 como observação, mas
  não tentar consertar.
