---
name: review-teammate-prs
description: Finds the pull requests (open or already merged) from the user's teammates that the user has not approved yet, reviews each one against a fixed checklist (what the title says, tests, secrets/personal data/generated files, readability, design, "Como testar") and delivers a summary table, one review draft per PR and a single block of `gh pr review` commands for the user to run. It also checks that each PR carries the process label in use, has its author as assignee and has every expected reviewer, and delivers the `gh pr edit` commands that fix what is missing. The GitHub handles of the teammates, the repositories, the reviewer and the label are parameters; if the handles, the repositories or the label are missing, ask, never infer. Never posts a review, edits a PR, approves or merges by itself. Use when the user asks to review, approve or catch up on teammates' PRs, including PRs that were merged without review.
when_to_use: Also fires on phrases like "quais PRs estão sem aprovação", "revisa os PRs dos meus colegas", "aprova os PRs do fulano", "revisão a posteriori dos PRs mergeados".
allowed-tools: Bash, Read, AskUserQuestion
argument-hint: "[handles=a,b,c] [repos=pasta1,pasta2] [reviewer=handle] [label=\"nome da label\"] [desde=AAAA-MM-DD]"
arguments:
  - handles
  - repos
  - reviewer
  - label
  - desde
context: inline
---

# Review Teammate PRs

Acha os PRs dos colegas que ainda não têm a aprovação do usuário (abertos ou já
mergeados), revisa cada um com o mesmo checklist e entrega rascunhos de
comentário mais os comandos `gh pr review` prontos. Confere também, em cada PR,
a label do processo, o autor como assignee e os reviewers, e entrega os
`gh pr edit` que corrigem o que faltar. **Nunca posta nem edita nada**: o
comentário chega a um colega em nome do usuário, então quem dispara é ele.

## Inputs

Todos aceitam `chave=valor` separados por espaço, em qualquer ordem. Se um
input obrigatório não for informado e não tiver default fixo aplicável,
**perguntar com `AskUserQuestion`, nunca inferir** (pelo arquivo aberto, pela
pasta atual ou por "só tem um repositório aqui").

| Input | O que é | Default |
|-------|---------|---------|
| `handles` | Handles do GitHub dos colegas, separados por vírgula | nenhum: obrigatório |
| `repos` | Repositórios git locais a varrer, separados por vírgula | nenhum: obrigatório |
| `reviewer` | Handle de quem revisa (o que já aprovou não entra) | o usuário do `gh` (`gh api user --jq .login`) |
| `label` | Label do processo em uso no momento, que todo PR precisa ter (ex.: a do processo que o time está tocando) | nenhum: **se não for informada, perguntar, nunca inferir** (nem pelas labels dos PRs recentes) |
| `desde` | Só PRs criados ou mergeados a partir desta data | sem filtro: os últimos 100 por repositório |

- `handles` e `repos` são obrigatórios: se não vierem, perguntar com
  `AskUserQuestion`. Se o CLAUDE.md do projeto já traz a lista do time (tabela
  de integrantes com handles), oferecê-la como opção, sem assumir.
- Handle informado é usado exatamente como veio. Nunca deduzir o handle pelo
  nome da pessoa.
- `label` com espaço ou acento vai entre aspas (`label="Nome da label"`). Sem
  ela, listar as labels do repositório (`gh label list -R <org>/<repo>`) e
  perguntar com `AskUserQuestion`, com as labels de processo como opções.
- Reviewers esperados em cada PR: `handles` mais o `reviewer`, menos o autor do
  PR (ninguém revisa o próprio PR). Assignee esperado: o próprio autor.
- Cada repositório precisa ter remoto no GitHub (`gh repo view` responde).
  Se não tiver, avisar e pular esse repositório.

Exemplos:

```
/review-teammate-prs handles=fulano,ciclana repos=~/Code/api,~/Code/web label="Nome da label"
/review-teammate-prs handles=fulano repos=~/Code/api reviewer=beltrana label=backend desde=2026-11-01
```

## Goal

Ao final, o usuário tem: uma tabela-resumo dos PRs encontrados com o veredito
de cada um, o que foi conferido e os pontos achados por PR, um rascunho de
comentário por PR, a situação de label, assignee e reviewers de cada um, um
único bloco de comandos `gh pr review` e outro de `gh pr edit` para colar no
terminal. A skill não executou nenhum deles.

## Steps

### 1. Obter os inputs

Resolver `handles`, `repos`, `reviewer`, `label` e `desde` conforme a tabela
acima. Perguntar o que faltar e não tiver default (a `label` nunca tem
default).

**Success criteria**: tenho a lista explícita de handles e de repositórios, a
label a conferir, e sei de onde veio cada valor (argumento, resposta ou
CLAUDE.md).

### 2. Atualizar os repositórios

Em cada repositório, `git status --porcelain` e, se a árvore estiver limpa,
`git pull --ff-only`. Árvore suja: pular o pull e avisar, sem mexer. Nunca
`git add`, `git commit`, `git push` nem trocar a branch do usuário.

**Success criteria**: cada repositório está atualizado ou avisado como
desatualizado, e a branch dele continua a mesma.

### 3. Achar os PRs sem aprovação do `reviewer`

Por repositório, abertos e mergeados (fechados sem merge ficam de fora):

```bash
gh pr list --state all --limit 100 --json number,title,author,state,isDraft,mergedAt,createdAt,additions,deletions,reviews,headRefName,labels,assignees,reviewRequests
```

Ficam os PRs cujo `author.login` está em `handles` e que não têm review
`APPROVED` do `reviewer`. Aplicar `desde` se veio. Nunca listar PR do próprio
`reviewer`. PR draft entra marcado como draft (a revisão serve de feedback,
mas não gerar `--approve` para ele).

Mostrar a tabela-resumo antes de revisar (repositório, número, autor, estado,
tamanho em linhas). Se não houver nenhum, dizer isso e parar.

Para saber se um PR já foi corrigido por outro posterior (ex.: um `fix` que
cita os números dos PRs revisados), procurar nos PRs mergeados do mesmo autor
pelo número no título ou no corpo. O comentário do PR original cita o PR
corretor, e não repete o que ele já resolve.

**Success criteria**: lista explícita e completa dos PRs a revisar, sem PR do
próprio `reviewer`, com a relação de correção posterior anotada quando existir.

### 4. Revisar cada PR

Buscar metadados e diff de cada PR (um `gh pr view` e um `gh pr diff` por PR,
gravando o diff em arquivo no scratchpad quando for grande). PRs independentes
podem ser lidos em paralelo.

Checklist (se o CLAUDE.md do projeto tiver uma seção de revisão de PR, ela
prevalece):

1. Faz o que o título e a descrição dizem?
2. Há testes para a mudança, cobrindo também o caminho de erro? Os existentes
   continuam passando?
3. Algum segredo, dado pessoal, arquivo grande ou saída gerada no diff
   (`.env`, chaves, CPF, logs, caches, `.venv`)?
4. Legibilidade: nomes claros, sem código comentado nem print de debug
   esquecido?
5. Design: isso já existe em outro lugar? Dá para testar sem rede e sem LLM?
6. Contrato mudou (modelo público, exceção, prompt versionado, config)? Então
   README, `.env.example`, ADR e `prompts.lock` precisam acompanhar.
7. O "Como testar" do PR reproduz e o resultado bate?
8. O checklist do PR bate com o que de fato foi feito (item marcado sem
   evidência, item desmarcado sem explicação)?

Técnicas que já se mostraram necessárias:

- **Diff acima de 20 mil linhas**: `gh pr diff` devolve 406 `too_large`. Se o
  PR é cópia de uma pasta, conferir por hash de árvore
  (`git rev-parse <ref>:<pasta>`) contra a origem que o PR declara, varrer a
  árvore com `git ls-tree -r --name-only` e `git grep` atrás de `.env`,
  chaves, CPF, logs e caches, e dizer no relatório que foi por hash, não linha
  a linha.
- **Rodar testes**: só em worktree descartável dentro do scratchpad
  (`git fetch origin pull/<n>/head:refs/remotes/origin/pr-<n>` e
  `git worktree add --detach <scratchpad>/pr<n>wt origin/pr-<n>`), usando o
  `.venv` do projeto, nunca o Python global. Ao terminar,
  `git worktree remove --force` e `git update-ref -d refs/remotes/origin/pr-<n>`.
  Nunca trocar a branch do usuário. Dependência ou ferramenta ausente
  (Node, Docker, Postgres) vai para o usuário como `AskUserQuestion` com as
  saídas possíveis, nunca é pulada em silêncio.
- **zsh**: em `for r in ...; do git rev-parse $r:pasta`, o `:p` vira
  modificador do zsh. Escrever `${r}:pasta`.
- **Comparar pastas copiadas**: comparar nomes por caminho e, se divergirem,
  por `basename`, antes de afirmar que um arquivo "não existe no destino".

Gravidade de cada ponto achado:

- **Bloqueia**: segredo ou dado pessoal no diff, teste quebrado, comportamento
  diferente do descrito, contrato mudado sem documentação.
- **Não bloqueia**: melhoria, ressalva ou pendência que cabe em outro PR.

PR já mergeado não pode ser bloqueado: ponto que bloquearia vira "ponto
encontrado" com sugestão de PR de correção, e a aprovação registra a revisão.

**Success criteria**: para cada PR sei o que foi conferido (e como: linha a
linha, por hash ou rodando testes), os pontos com a gravidade e o que ficou
sem verificar.

### 4b. Conferir label, assignee e reviewers

Para cada PR, com os campos que o passo 3 já trouxe (`labels`, `assignees`,
`reviewRequests`, `reviews`):

1. **Label**: o PR tem a `label` informada? Se não, o comando é
   `gh pr edit <n> --add-label "<label>"`.
2. **Assignee**: o autor do PR está em `assignees`? Se não,
   `gh pr edit <n> --add-assignee <autor>`.
3. **Reviewers**: cada reviewer esperado (ver Inputs) está em
   `reviewRequests` ou entre os autores de `reviews`? Quem não está entra em
   `gh pr edit <n> --add-reviewer a,b`. Quem já revisou conta como colocado.

Os comandos do mesmo PR podem ser um só `gh pr edit` com as flags juntas.

PR mergeado: o GitHub não aceita pedir reviewer depois do merge, então só
reportar quem faltou, sem gerar `--add-reviewer`. Label e assignee continuam
valendo e geram comando. PR draft segue a mesma conferência.

Falha nesta conferência nunca bloqueia a aprovação: entra como "ponto que não
bloqueia" no comentário do review e como linha da tabela-resumo.

**Success criteria**: cada PR tem a situação de label, assignee e reviewers
(`ok` ou o que falta) e, quando faltar algo corrigível, o `gh pr edit`
correspondente.

### 5. Decidir o veredito

- `APROVAR`: nenhum ponto que bloqueia. Pontos que não bloqueiam entram no
  comentário.
- `PEDIR MUDANÇAS`: há ponto que bloqueia num PR aberto. **Não** gerar
  `--approve` para ele: trazer o impasse numa `AskUserQuestion`, com as
  saídas possíveis (pedir mudanças, aprovar mesmo assim, só comentar).

**Success criteria**: cada PR tem exatamente um veredito, e nenhum bloqueio
virou aprovação em silêncio.

### 6. Entregar no padrão de resposta

Abrir a mensagem com uma linha curta dizendo para quem o texto foi escrito
(ex.: "Escrito para: o usuário, que cola os comandos no GitHub"). Depois, nesta
ordem:

1. **Tabela-resumo**: repositório, PR, autor, estado, veredito, label,
   assignee e reviewers (`ok` ou o que falta em cada um).
2. **Verificação**: o que foi conferido em geral (hash, testes rodados com o
   resultado, varredura de segredos) e o que não deu para conferir.
3. **Por PR**, em poucas linhas: o que foi conferido, pontos encontrados com a
   gravidade e o rascunho do comentário.
4. **Blocos de comandos**, ao fim da mensagem, em dois blocos separados e
   numerados (o dos reviews e, só se algo faltar, o dos ajustes de metadado):

```bash
cd <pasta local do repositório> && gh pr review <n> -R <org>/<repo> --approve --body "$(cat <<'EOF'
<comentário em markdown, com seções e listas>
EOF
)"
```

```bash
cd <pasta local do repositório> && gh pr edit <n> -R <org>/<repo> --add-label "<label>" --add-assignee <autor> --add-reviewer <a>,<b>
```

Regras do rascunho do comentário (vai ser colado no GitHub):

- Técnico e impessoal. **Sem saudação, elogio ou mensagem pessoal** ("Ótimo
  trabalho", "Parabéns", "Valeu") e sem o nome do autor. Pontos positivos só de
  forma impessoal sobre o código ("A cópia confere: ...").
- Estrutura, em markdown (o GitHub renderiza), com cada parte sob um título em
  negrito e itens em lista, nunca um bloco de texto corrido:
  - `**Verificado**`: lista curta (diff lido, testes rodados com o resultado,
    ruff e pyright, o que não deu para conferir).
  - `**O que bate com a descrição**`: lista do que o PR faz e está certo, em
    forma impessoal. Pode ser omitido quando a lista acima já diz o essencial.
  - `**Pontos que não bloqueiam**` (ou `**Pontos a corrigir**` quando há
    bloqueio): lista numerada, cada ponto com sugestão concreta e gentil.
    Omitir a seção se não houver ponto.
  - `**Pendência fora do PR**`: só se houver.
  Manter cada item curto, com o código entre crases.
- Sem `@menção` no texto. Se uma menção for realmente necessária, avisar o
  usuário antes e usar só handle confirmado. As flags `--add-assignee` e
  `--add-reviewer` do `gh pr edit` não são menção: usam só os handles dos
  inputs, nunca deduzidos.
- Sem linha de atribuição ao Claude.
- Português do Brasil, vírgula no lugar de travessão ("—").
- O comentário vai num heredoc com delimitador entre aspas simples
  (`<<'EOF'`), então não precisa escapar aspas nem crases. Nenhuma linha do
  comentário pode ser só `EOF`.

Regras do bloco de comandos:

- Um único bloco de código, sem linhas de comentário `#` (o usuário cola o
  bloco inteiro de uma vez no zsh).
- `-R <org>/<repo>` lido do remoto de cada repositório
  (`gh repo view --json nameWithOwner`). Todo comando do bloco também começa
  com `cd <pasta local do repositório> && ` (a pasta vem do input `repos`), na
  mesma linha, para o usuário nunca rodar no lugar errado
  por acidente. O `-R` continua, e os dois juntos valem para cada repositório.
- Comandos de conferência que o usuário vai colar (ex.: ver se o review entrou)
  ficam em outro bloco, numerado, nunca misturados aos que escrevem no GitHub,
  e também começam com o `cd`. O comando do passo 7, que a própria skill roda,
  não precisa dele.
- Para reescrever um review já postado (só quando o usuário pedir), entregar,
  com o `cd <pasta local do repositório> && ` na frente,
  `gh api -X PUT repos/<org>/<repo>/pulls/<n>/reviews/<review_id> -f body="$(cat <<'EOF' ... EOF
)"`, com o `review_id` lido por
  `gh api repos/<org>/<repo>/pulls/<n>/reviews --jq '.[]|select(.user.login=="<reviewer>")|.id'`.
  Também é um comando que o usuário roda, nunca a skill.

**Success criteria**: o usuário recebe tabela, verificação, rascunhos, o bloco
de `gh pr review` e, se faltar metadado, o de `gh pr edit`, tudo pronto para
colar, e nada foi postado nem editado.

### 7. Acompanhar depois

Quando o usuário disser que rodou, conferir sozinho, sem perguntar:

```bash
gh pr view <n> -R <org>/<repo> --json reviews,labels,assignees,reviewRequests --jq '{reviews:[.reviews[]|"\(.author.login):\(.state)"],labels:[.labels[].name],assignees:[.assignees[].login],pending:[.reviewRequests[]|.login]}'
```

Reportar o que entrou (aprovações, label, assignee, reviewers) e o que falta. Seguir lembrando o que não foi rodado
até o usuário dizer explicitamente que fez.

**Success criteria**: sei, por consulta ao GitHub, quais aprovações entraram.

## Regras gerais

- **Nunca executar** `gh pr review`, `gh pr edit`, `gh pr merge`, `gh pr comment`,
  `git add`, `git commit` ou `git push`. Só leitura (`gh pr list/view/diff`,
  `git fetch`, `git pull --ff-only`, `git ls-tree`, `git grep`, `git rev-parse`)
  e o worktree descartável no scratchpad.
- Nunca revisar nem listar PR do próprio `reviewer`.
- Nunca mexer em arquivos do repositório revisado nem em
  pastas de documentação do time por conta da revisão.
- Qualquer coisa que a skill não consiga fazer (ferramenta ausente, comando
  que falha, verificação impossível) vai para o usuário numa `AskUserQuestion`
  com as saídas possíveis. Nada passa em branco.
- Se um input obrigatório não foi informado, **perguntar, nunca inferir**.
- Esta skill não chama outra skill.
