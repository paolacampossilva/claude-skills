---
name: explain-project
description: >-
  Writes a didactic .md explanation for the user in two layers, plain language first and technical terms in an advanced section, and saves it in a folder the user names. Two modes: "retrospective" (explains what the user did in a project, plus an overview of the whole project and its progress, for sprint meetings where they may speak for the whole team) and "new process" (explains what a newly arrived process is, so the user can decide what to do). Only use when the user explicitly invokes it by name (e.g. "usa a explain-project"), not just because they ask a question about a project. If the mode, source, speaking scope or output folder is missing, ask, never infer.
---

# Explain Project

Gera um documento `.md` didático, em português do Brasil, em duas camadas:
primeiro a explicação **sem jargão** (analogias, o que é e para quê), depois
uma **seção avançada** com os termos técnicos. A saída é só o arquivo, sem
despejar o documento no chat.

## Quando se aplica

**Só por invocação explícita**. O usuário chama pelo
nome (`/explain-project` ou "usa a explain-project"). Uma pergunta comum sobre
um projeto não dispara a skill.

## Inputs obrigatórios

Se não vierem na chamada, perguntar com `AskUserQuestion`. **Nunca inferir**
pelo contexto (pasta aberta, projeto da conversa) nem seguir sem a etapa que
dependia do input.

1. **Modo**: `retrospectivo` ou `processo novo`.
2. **Retrospectivo**:
   - qual projeto ou pasta;
   - de quem é a parte (a pessoa, a task ou o período);
   - **escopo da fala**: só a minha parte, pelo time todo, ou as duas.
3. **Processo novo**: a fonte do processo (caminho de task, PDF ou issue, ou
   texto colado).
4. **Pasta de destino** do `.md`. Só o nome do arquivo é sugerido pela skill,
   em `snake_case`, sem perguntar. Se a pasta não existir, criar.

## Passos

1. **Ler a fonte inteira antes de escrever.** Para volume grande, usar agentes
   Explore em paralelo (código, documentação, `git log`). Autoria vem do
   `git log` e dos relatórios, nunca de suposição.
2. **Escrever o `.md`** com o modelo do modo escolhido (abaixo).
3. **Gravar** na pasta de destino e avisar o caminho completo em uma ou duas
   linhas, mais os pontos que o usuário deve conferir antes de falar. Não colar o documento
   no chat.

## Regras de escrita

- Português do Brasil, vírgula em vez de travessão em qualquer parte.
- Camada simples primeiro: frase curta, analogia, nenhum termo técnico sem
  tradução ao lado. Termo técnico só na seção avançada.
- Emojis nos títulos de seção, tabelas e citações em bloco para destacar.
- Primeira pessoa é permitida quando o arquivo é pessoal. Se a pasta de destino
  for compartilhada com o time, escrever em terceira pessoa e neutro sobre os
  colegas.
- Números só com fonte e conferência. Dado de ferramenta ou git que não foi
  rodado é dito como tal (ex.: "contagem de funções, não rodei o pytest").
- Divergência entre fontes (ex.: commits do serviço x do repositório inteiro)
  vira nota no próprio documento.
- Separar o que é do usuário do que é de colegas, e o que está só planejado do que
  está feito.
- Nunca rodar `git add`, `git commit` nem `git push`.

## Modelo: modo retrospectivo

Seções, nesta ordem:

1. Título e sumário.
2. **O projeto em palavras simples**: problema, solução, regra de ouro, onde
   o usuário entra, uma analogia, e a tabela de tasks com responsável.
3. **Visão geral do projeto inteiro e andamento** (ver abaixo).
4. **O que eu fiz, em ordem**, em fases.
5. **Números para citar**, cada um com a fonte.
6. **Roteiro de fala** de 1 minuto sobre a parte do usuário.
7. **O que falta**: código, o que depende do usuário sem código, o que está
   bloqueado e o que levar ao scrum master.
8. **O que não é meu**: tabela por pessoa.
9. **Seção avançada: termos técnicos**.

### Seção "Visão geral do projeto inteiro e andamento"

Existe para as sprints em que o usuário fala por todos. Conteúdo:

- Mapa do projeto em tabela: cada frente ou task, responsável, estado (feito,
  em andamento, a fazer, bloqueado), PRs ou entregas e data do último avanço.
- Linha do tempo curta: o que entrou por semana ou por sprint.
- Como as partes se encaixam (quem depende de quem), em linguagem simples.
- Andamento honesto: contagem de entregas feitas sobre o total planejado, dita
  como contagem e não como porcentagem de esforço, com a fonte (plano, PRs).
- Riscos, bloqueios e decisões pendentes do projeto inteiro, e o que está sem
  dono.
- Roteiro de fala de 2 minutos "pelo time todo", além do individual.
- O que o usuário precisa confirmar com cada colega antes da reunião. Dado que não
  deu para verificar vira pergunta, nunca afirmação.

Escopo da fala:

- **só a minha parte**: a visão geral fica curta, só como contexto;
- **pelo time todo**: a visão geral vira o centro do documento e a parte
  individual encolhe;
- **as duas**: peso igual.

## Modelo: modo processo novo

Seções, nesta ordem:

1. Título e sumário.
2. **O que é este processo**, em palavras simples: quem pede, o que entra, o
   que sai, por que existe.
3. **Como funciona hoje, passo a passo.**
4. **Termos e siglas traduzidos.**
5. **Riscos e pontos de atenção.**
6. **Decisões que cabem a você**: cada uma com opções, o efeito de cada uma e
   uma recomendação.
7. **Perguntas em aberto** para quem trouxe o processo.
8. **Seção avançada: termos técnicos.**

Não explorar a base de código atrás de pontos de inserção. Explicar só o
processo e terminar com o próximo passo "mapear nos projetos". Mapear só se o usuário
pedir.
