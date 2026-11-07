---
name: suggest-commits
description: Suggests a sequence of logically-grouped git commits for whatever is uncommitted in a given git repository — one commit per type/scope from a fixed commit-type table, single-line Conventional Commits in Portuguese with mandatory scope (`tipo(escopo): descrição`, team Git manual), no body and no Claude co-author trailer — followed by the git push command, all printed as copy-pasteable commands for the user to run themselves. Never runs git commit or git push itself. Use when the user asks to suggest, organize, or split commits for pending changes in a git repo.
when_to_use: Also fires when pending changes mix concerns (e.g. a fix and a doc change together) that need splitting into separate commit groups.
allowed-tools: Bash, AskUserQuestion, Agent
argument-hint: "[caminho do repositório git]"
arguments:
  - repo_path
context: inline
---

# Suggest Commits

Analisa o que está pendente (não commitado) num repositório git apontado pelo
usuário e sugere uma sequência de commits organizados por tipo/escopo lógico,
seguindo a tabela de tipos fixa abaixo. Só imprime os comandos — nunca roda
`git commit` nem `git push` sozinha.

## Inputs

- `$repo_path`: caminho do repositório git a analisar. Se não vier como
  argumento, **sempre perguntar** com `AskUserQuestion` — nunca inferir do
  diretório de trabalho atual, mesmo que a sessão já esteja dentro de um
  repositório git.

## Tabela de tipos de commit (fixa)

Tabela de tipos do manual de Git do time (a mesma da seção `## Git`
do CLAUDE.md, se houver):

| Tipo       | Quando usar                                         | Exemplo                                                   |
|------------|-----------------------------------------------------|-----------------------------------------------------------|
| `feat`     | Funcionalidade nova                                 | `feat(app): adiciona exportação do relatório em PDF`          |
| `fix`      | Correção de erro                                    | `fix(auth): corrige permissão negada para admin`   |
| `docs`     | Só documentação                                     | `docs(api): descreve variáveis do .env.example`          |
| `test`     | Só testes                                           | `test(parser): cobre nota fiscal com itens mistos` |
| `refactor` | Reorganiza o código sem mudar o comportamento       | `refactor(search): separa cliente HTTP do serviço` |
| `perf`     | Melhora de desempenho                               | `perf(llm): cacheia resposta por processo`        |
| `chore`    | Manutenção: dependências, configuração, `.gitignore` | `chore(repo): ignora pastas saidas/ e results/`          |
| `ci`       | Automação no GitHub Actions                         | `ci(repo): roda pytest em cada PR`                        |

Nunca inventar um tipo fora desta lista (`style` e `add` não existem mais).

## Escopos

O escopo é obrigatório e vem da pasta de projeto dos arquivos do grupo,
relativa à raiz do repositório (ex.: `api`, `web`, `docs`). Arquivos da raiz
usam `repo`. Em monorepo com subpastas aninhadas, usar a pasta de primeiro
nível. Se o projeto tiver uma lista de escopos própria no CLAUDE.md, ela
prevalece.

## Goal

Ao final, o usuário recebe um bloco de comandos pronto para colar no
terminal: uma sequência de `git add` + `git commit -m "tipo(escopo): descrição"`
(um par por grupo lógico de mudança) seguida de um `git push` final — e nada
disso foi executado pela skill, só analisado e impresso.

## Steps

### 1. Obter o repositório

Se `$repo_path` não vier como argumento, perguntar explicitamente com
`AskUserQuestion` — nunca assumir o diretório atual.

**Success criteria**: tenho um caminho de repositório explícito, nunca
inferido silenciosamente.

### 2. Validar repositório e levantar estado

Numa única chamada (as três são independentes entre si):

```bash
git -C "$repo_path" rev-parse --is-inside-work-tree && \
git -C "$repo_path" branch --show-current && \
git -C "$repo_path" status --porcelain=v1
```

Se `rev-parse` falhar, avisar o usuário e pedir o caminho correto — nunca
seguir em frente com um caminho que não é um repositório git válido. Se
`status` vier vazio, reportar "nada pendente para commitar em `$repo_path`"
e parar — nunca inventar um commit para algo que não existe. Guardar a
branch retornada aqui — o passo 6 a reaproveita, sem chamada nova.

Se a branch atual for `dev` ou `main`, avisar que o manual proíbe commit
direto nelas e colocar no topo do bloco final a criação da branch de
trabalho: `git switch dev && git pull` → `git switch -c
<prefixo>/<tipo>/<descricao-curta>` (o prefixo vem do CLAUDE.md ou do manual do time, e se não houver, perguntar; minúsculas, hífen, sem acento, `<tipo>` ∈
feat/fix/docs/test/refactor/chore, tirado do grupo principal).

**Success criteria**: confirmação de que `$repo_path` é um repositório git
válido, a branch atual já em mãos, e a lista completa de arquivos pendentes
(staged, unstaged, untracked, deletados, renomeados).

### 3. Ler o conteúdo real das mudanças

Classificar pelo nome/extensão do arquivo sozinho não é confiável — ler o
diff de verdade, para o repositório inteiro de uma vez (não uma chamada por
arquivo):

```bash
git -C "$repo_path" diff
git -C "$repo_path" diff --staged
```

Extrair, a partir dessas duas saídas combinadas, o hunk correspondente a
cada arquivo pendente. Para arquivo novo/untracked (não aparece em nenhum
diff), ler o conteúdo do próprio arquivo.

**Success criteria**: para cada arquivo pendente, sei exatamente o que
mudou, não só que "algo mudou" — sem precisar de uma chamada de `git diff`
por arquivo.

### 4. Agrupar por escopo lógico e classificar

Agrupar arquivos relacionados (mesma feature/módulo/intenção) e atribuir um
único tipo da tabela por grupo, com base na mudança real (passo 3) — nunca só
pela extensão do arquivo. Um `.md` que documenta uma feature nova junto do
código relacionado pode pertencer ao grupo `feat`, não `docs`, por exemplo.

**Nunca misturar dois escopos no mesmo grupo/commit**: arquivos de
projetos diferentes (ex.: `api/` e `web/`) viram commits separados, mesmo
que a intenção seja parecida.

**Nunca misturar dois tipos no mesmo grupo/commit** (ex.: um `fix` e um
`feat` juntos), mesmo que estejam no mesmo arquivo. Se um único arquivo
mistura mudanças de tipos diferentes, sinalizar isso ao usuário em vez de
decidir sozinho como separar.

Se a classificação de algum grupo for genuinely ambígua (ex.: pode ser lido
como `fix` ou `refactor`), perguntar ao usuário com `AskUserQuestion` em vez
de assumir.

Se houver muitos arquivos pendentes (mais de ~5-6), lançar agentes em
paralelo (tool `Agent`, um grupo de arquivos por agente) para ler e
classificar em vez de processar um a um.

**Success criteria**: cada arquivo pendente pertence a exatamente um grupo, e
cada grupo tem um único tipo da tabela, com justificativa clara — nada
decidido "no chute".

### 5. Escrever a mensagem de cada commit

- Uma linha só, sem corpo/descrição (`git commit -m "tipo(escopo): descrição"`,
  nunca `-m "título" -m "corpo"` nem mensagem multi-parágrafo). O manual
  permite um corpo opcional, mas a preferência do usuário é uma linha.
- **Em português**, verbo no presente (`adiciona`, `corrige`, `remove`), em
  minúsculas, sem ponto final.
- Formato `tipo(escopo): descrição`, primeira linha com no máximo 72
  caracteres (ex.: `fix(llm): corrige resposta vazia do cliente
  OpenRouter`).
- Nunca mensagens vagas (`ajustes`, `update`, `wip`, `teste`).
- **Nunca incluir** trailer `Co-Authored-By: Claude...` — são commits que o
  próprio usuário vai rodar e assinar; a atribuição de coautoria do Claude
  não se aplica a comandos que a skill apenas sugere e nunca executa.

**Success criteria**: cada mensagem é uma linha só, com no máximo 72
caracteres, sem trailer de coautoria, no formato `tipo(escopo): descrição`
em português.

### 6. Montar os comandos finais

Para cada grupo, nesta ordem, com paths relativos à raiz de `$repo_path`
(nunca caminho absoluto do sistema):

```bash
git add <arquivo1> <arquivo2> ...
git commit -m "tipo(escopo): descrição"
```

Todos os arquivos de um mesmo grupo entram numa única linha de `git add`,
separados por espaço. Depois de todos os grupos, adicionar um `git push`
final, com a branch já obtida no passo 2 (sem chamada nova). Antes do push,
trazer a `dev` para a branch (o manual pede isso antes de abrir o PR):

```bash
git fetch origin && git merge origin/dev
git push -u origin <branch-atual>
```

Se o passo 2 mandou criar uma branch nova, usar o nome dela aqui no lugar da
branch atual.

**Success criteria**: bloco de comandos completo, na ordem certa, pronto
para colar no terminal sem edição.

### 7. Apresentar, nunca executar

Mostrar o bloco de comandos completo (todos os `git add`/`git commit` do
passo 6 + o `git push` final) num único bloco de código, com uma frase antes
de cada commit explicando o que aquele grupo contém.

**Success criteria**: o usuário recebe algo para copiar e colar — a skill
não rodou nenhum `git add`, `git commit` ou `git push` por conta própria.

## Regras gerais

- **Nunca executar** `git add`, `git commit` ou `git push` de verdade — só
  os comandos read-only dos passos 2-3 (`rev-parse`, `branch --show-current`,
  `status`, `diff`) podem ser rodados pela própria skill via `Bash`.
- Mensagem de commit é sempre uma linha só, sem corpo/descrição, no formato
  `tipo(escopo): descrição` em português.
- Nunca incluir `Co-Authored-By: Claude` (ou qualquer trailer de coautoria)
  nas mensagens sugeridas — contradiz a convenção geral de atribuição de
  commits porque aqui é sempre o usuário quem roda e assina o commit.
- Nunca inventar tipo fora da tabela fixa, nem inventar grupo/commit para
  algo que `git status` não mostrou como pendente.
- `$repo_path` é sempre perguntado explicitamente quando não vier como
  argumento — nunca inferido do diretório de trabalho atual, mesmo que ele
  já seja um repositório git.
