# Detecção de docstring/comentário desatualizado

Só sinalizar divergências **concretas e apontáveis** — algo que dá pra citar
lado a lado (o que a doc diz vs. o que o código faz) e qualquer pessoa
concordaria que é uma divergência de fato, não de opinião.

## Checagens concretas (o que SIM sinalizar)

1. **`Args:` desalinhado da assinatura real** — parâmetro documentado que não
   existe mais na função, parâmetro novo na função que não está documentado,
   ou nome documentado diferente do nome real (ex.: docstring diz `usuario_id`,
   assinatura tem `user_id`).
2. **`Returns:` não bate com o retorno real** — docstring promete um tipo/
   formato que o código não entrega mais (ex.: docstring diz "retorna uma
   lista", código agora tem `return None` em algum caminho não documentado, ou
   o `return` foi trocado por `yield`).
3. **`Raises:` incompleto ou errado** — a função levanta uma exceção que a
   docstring não menciona, ou a docstring menciona uma exceção que o código
   não levanta mais (ex.: um `try/except` que engolia o erro foi removido).
4. **Comentário `#` referenciando código que não existe mais** — ex.: `# skip
   if user is None` acima de uma linha que não tem mais esse `if`, ou um
   comentário citando o nome antigo de uma variável/função que foi renomeada.
5. **`# TODO`/`# FIXME` já resolvido** — o comentário descreve um problema que
   o código abaixo dele já trata (ex.: `# TODO: validar entrada` acima de um
   bloco que já valida).
6. **Descrição de comportamento condicional que mudou** — docstring descreve
   "quando X, faz Y" mas o código não tem mais esse branch, ou a condição
   mudou de forma que a descrição não é mais precisa.
7. **Docstring de módulo/classe descrevendo responsabilidade que migrou** —
   ex.: docstring de classe diz "também valida o schema" mas essa validação
   foi movida para outro lugar e a classe não faz mais isso.

## O que NÃO é motivo para sinalizar

- Paráfrase diferente da que você escreveria, mas com o mesmo sentido factual.
- Docstring correta porém curta/minimalista (falta de detalhe não é
  desatualização).
- Ausência de seção `Args`/`Returns`/`Raises` quando a função é simples o
  bastante para não precisar (isso é estilo, não staleness).
- Comentário de contexto histórico/decisão de design que continua válido
  mesmo depois de refatorações (ex.: "usamos X em vez de Y porque..." — a
  decisão pode continuar válida mesmo que o código ao redor tenha mudado de
  forma; só reescrever se referenciar algo especificamente removido).
- Qualquer coisa que exigiria julgamento de gosto/estilo para "corrigir".

## Como reportar cada achado

Para cada divergência concreta encontrada, montar uma entrada assim antes de
juntar no relatório do passo 6 do `SKILL.md`:

```
Arquivo: caminho/relativo/arquivo.py:linha_da_funcao
Função: nome_da_funcao
O que a doc diz: "..."
O que o código faz: "..." (com a linha/trecho relevante)
Correção proposta: "..."
```

Isso é o que aparece no resumo mostrado ao usuário antes de qualquer `Edit`.
