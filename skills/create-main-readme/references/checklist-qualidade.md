# Checklist de qualidade — antes de considerar o README pronto

Rodar depois de escrever/editar, antes de reportar a tarefa como concluída.

## 1. Paridade PT-BR / EN

Achado real numa auditoria: um README tinha uma seção "EN" que só continha o
título e a tabela de tipos de commit traduzidos — todo o resto do conteúdo
(visão geral, como rodar, etc.) não tinha equivalente em inglês. Isso passa
despercebido numa checagem visual rápida porque o bloco `<details>` existe e
"parece" bilíngue.

Verificação obrigatória: contar quantos títulos `##`/`###` existem dentro do
bloco `<details>` PT-BR e quantos existem dentro do bloco `<details>` EN — os
números têm que bater (mesma quantidade de seções, ainda que os textos dos
títulos estejam traduzidos). Se não baterem, a tradução está incompleta.

```bash
awk '/<summary>.*🇧🇷/,/<\/details>/' README.md | grep -c '^##'
awk '/<summary>.*🇺🇸/,/<\/details>/' README.md | grep -c '^##'
# os dois números precisam ser iguais
```

## 2. Blocos de código e `<details>` balanceados

```bash
grep -c '^```' README.md      # tem que ser par (cada fence abre e fecha)
grep -n '<details\|</details>' README.md   # cada <details> tem que ter um </details> correspondente
```

## 3. Links internos resolvem

Todo link markdown `[texto](caminho/)` ou `[texto](caminho/arquivo.md)` tem que
apontar para algo que existe de verdade no repositório. Conferir cada um com
`ls`/`test -e` antes de finalizar — não assumir que um caminho "parece certo".

## 4. Âncoras do Sumário batem com os títulos reais

Se houver uma seção "Sumário" com links `#slug-do-titulo`, os slugs têm que
bater com o algoritmo de slug do GitHub (minúsculas, espaços viram hífen,
pontuação removida exceto hífen, acentos preservados). Regerar o Sumário por
último, depois que a estrutura final estiver fechada — um título que mudou
depois do Sumário ser escrito quebra a âncora silenciosamente.

## 5. Nenhuma seção foi inventada

Toda afirmação sobre comando, endpoint, variável de ambiente ou comportamento
tem que ter sido conferida contra o código real durante a investigação — não
contra a "impressão" do que o projeto provavelmente faz. Se uma seção do
esqueleto (ver `estrutura-readme.md`) não tem informação real disponível,
está tudo bem omiti-la — mas isso tem que estar explícito no plano mostrado ao
usuário antes de escrever, nunca preenchido com suposição.

## 6. Conteúdo próprio do README anterior foi preservado

Se o README já existia e tinha seções fora do esqueleto padrão (ex.: decisões
de engenharia narradas, troubleshooting específico, comparações de modelo),
confirmar que esse conteúdo sobreviveu — incorporado na seção mais próxima do
esqueleto, ou mantido como seção extra. Não é lixo a apagar só porque não bate
com o template.
