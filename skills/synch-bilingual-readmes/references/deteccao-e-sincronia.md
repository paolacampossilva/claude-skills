# Detecção do padrão bilíngue e verificação de sincronia

Método compartilhado por `synch-bilingual-readmes` (escopo: `README.md`) e
`synch-bilingual-docs` (escopo: `docs/*.md`) — arquivo canônico único, as
duas skills apontam para ele.

## Convenção esperada

Cada arquivo bilíngue (`README.md` ou `docs/*.md`) segue este formato (o formato
que estas skills esperam):

```markdown
<details open>
<summary><b>🇧🇷 pt-br</b> — Título</summary>
<br>

# Título em português
... conteúdo em PT-BR ...

</details>

---

<details>
<summary><b>🇺🇸 en</b> — Title</summary>
<br>

# Title in English
... mirrored content in English ...

</details>
```

O bloco PT-BR vem primeiro e aberto (`<details open>`); o bloco EN vem depois
e fechado (`<details>`). Identificar os dois blocos localizando as linhas
`<summary>` que contêm 🇧🇷/pt-br e 🇺🇸/en, e tudo entre cada `<details>` e o
`</details>` correspondente é o conteúdo daquele idioma.

## Classificar o estado de um arquivo

1. **Nenhum bloco `<details>` bilíngue** — o arquivo é texto corrido, sem essa
   estrutura nenhuma. Tratar como "só PT-BR sem mirror": envolver o conteúdo
   existente no mesmo formato `<details>` acima (criando o resumo/summary a
   partir do título real do arquivo) antes de gerar o mirror EN — não inventar
   uma convenção de bilinguismo diferente da já usada no resto do projeto.
2. **Só bloco PT-BR** (tem `<details>` com 🇧🇷 mas nenhum com 🇺🇸) — falta o
   mirror EN inteiro.
3. **Os dois blocos existem** — seguir para a verificação de sincronia abaixo.

## Verificação estrutural (rápida)

Contar quantos títulos `##`/`###` existem dentro de cada bloco:

```bash
awk '/<summary>.*🇧🇷/,/<\/details>/' "$arquivo" | grep -c '^#'
awk '/<summary>.*🇺🇸/,/<\/details>/' "$arquivo" | grep -c '^#'
```

Os dois números têm que bater. Se não baterem, ir além da contagem: listar os
títulos de cada lado (`grep '^#'` em vez de `grep -c '^#'`) e comparar a
ordem/quantidade título a título — a seção que falta do lado mais curto é o
que precisa ser traduzido e inserido na posição certa.

## Verificação de conteúdo (por seção)

Depois que a estrutura bate (mesmo número/ordem de seções), comparar o
conteúdo de cada par de seções correspondentes (a N-ésima seção do PT-BR
contra a N-ésima seção do EN):

1. Ler o texto de cada lado.
2. Extrair as **entidades concretas** de cada um: comandos entre crases,
   nomes de variável de ambiente (`MAIÚSCULO_COM_UNDERSCORE`), paths de
   arquivo (incluindo paths para assets não-markdown referenciados, ex.
   `comparison.csv`, `results.json`,
   `flowchart.pdf`), números/versões, nomes de
   endpoint (`GET /algo`), URLs.
3. Comparar os dois conjuntos de entidades. Se o PT-BR menciona algo que o EN
   não menciona (ou vice-versa), a seção está dessincronizada — não é só
   questão de tradução literal, é informação faltando de um lado.
4. Frases parafraseadas de forma diferente mas com as mesmas entidades
   concretas **não** são um problema — o objetivo é paridade de informação,
   não tradução palavra-por-palavra.

## Corrigindo

- **PT-BR é sempre a fonte da verdade.** Nunca alterar o conteúdo do bloco
  PT-BR para "consertar" uma divergência — só ajustar o bloco EN para
  espelhar o que o PT-BR já diz.
- Ao traduzir uma seção nova (ou corrigir uma existente), preservar
  tom, nível de detalhe e formatação (tabelas continuam tabelas, blocos de
  código não são traduzidos, só comentários/texto explicativo).
- Comandos de shell, nomes de variável, nomes de arquivo e URLs nunca são
  traduzidos — só o texto explicativo ao redor. Isso vale também para paths
  de arquivos não-markdown (`.csv`, `.json`, `.pdf`, `.png`) citados no
  texto: eles apontam para artefatos reais ao lado do `.md` e devem
  permanecer exatamente iguais no bloco EN.
- Depois de editar, rodar a verificação estrutural de novo para confirmar que
  os dois lados agora batem.
