# Detecção de idioma e tradução segura

## Heurística de "isto está em português"

Sinais suficientes para classificar um trecho de docstring/comentário como
português (não precisa de todos, um já é forte indício):

- Presença de caracteres acentuados típicos do português fora de string
  literal/exemplo de código: `ã õ ç é ê í ó ú à`.
- Stopwords/palavras-função comuns: `que`, `para`, `não`, `com`, `uma`, `dos`,
  `das`, `são`, `está`, `foi`, `quando`, `então`, `também`, `função`, `retorna`,
  `parâmetro`, `exceção`, `verifica`, `cria`, `atualiza`.
- Conjugação verbal em português reconhecível (`-ção`, `-mente`, `-ável`).

**Não confundir com português**:
- Nomes de variável/função/classe em português dentro de código de exemplo
  dentro da docstring (ex.: `>>> calcular_imposto(nota)`) — código de exemplo
  não é prosa, não traduzir identificadores nem chamadas de função.
- Trechos entre crases (`` `algo` ``) que são nomes literais de campo/endpoint
  vindos de um contrato de API em português (ex.: campos JSON do domínio,
  como `nome` ou `tipo_documento`, que são contrato, não prosa a traduzir).
- Nomes próprios, siglas, e valores de enum/constante.

## O que traduzir e o que nunca tocar

Traduzir: a prosa explicativa em si — a frase que descreve o que a função faz,
o que um parâmetro representa, o que uma exceção significa.

Nunca traduzir:
- Identificadores de código (nomes de variável, função, classe, parâmetro).
- Exemplos de código dentro da docstring (blocos `>>>` ou ``` ```` ```).
- Valores literais, chaves de dicionário, nomes de campo de contrato externo
  (JSON de API, nome de coluna de banco).
- Nomes de exceção (`ValueError`, `HTTPException`, etc.) — só o texto ao redor
  que os descreve.
- URLs, paths de arquivo, comandos de shell.

## Preservando o formato Google-style

Se a docstring já segue o formato Google (`Args:`, `Returns:`, `Raises:`),
manter a mesma estrutura na tradução — só trocar o texto em português por
inglês, sem reorganizar seções, sem adicionar seções que não existiam (isso é
enforcement de estilo, fora do escopo desta skill — ver `SKILL.md`).

## Exemplo

Antes:
```python
def calcular_iss(valor_base: float, aliquota: float) -> float:
    """Calcula o valor do ISS retido sobre um serviço.

    Args:
        valor_base: valor bruto do serviço, em reais.
        aliquota: alíquota do ISS do município, entre 0 e 1.

    Returns:
        O valor do imposto retido, arredondado para 2 casas decimais.
    """
```

Depois (só o texto traduzido, formato/identificadores intactos):
```python
def calcular_iss(valor_base: float, aliquota: float) -> float:
    """Calculates the ISS tax withheld on a service.

    Args:
        valor_base: gross value of the service, in reais.
        aliquota: the municipality's ISS rate, between 0 and 1.

    Returns:
        The withheld tax amount, rounded to 2 decimal places.
    """
```
