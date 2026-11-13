# Esqueleto de seções do README principal

Forma canônica, destilada de um README de referência real (projeto com múltiplos
módulos LangGraph + Streamlit). É a **forma**, não o conteúdo — cada seção existe
em qualquer tipo de projeto (microserviços FastAPI, frontend JS, pipeline único,
etc.), só muda o que entra dentro dela. Nunca pular uma seção sem justificar no
plano mostrado ao usuário antes de escrever.

Tente sempre nesta ordem:

## 1. Título + descrição de uma frase

Nome do projeto/time + o que ele faz, em uma frase densa (tecnologias-chave em
negrito, sem enrolação).

## 2. `**Integrantes:**`

Nomes da equipe, um por linha. Pegar de um README irmão do mesmo repositório,
do CLAUDE.md ou do que o usuário informar; se nenhuma dessas fontes existir,
perguntar com `AskUserQuestion`, nunca inventar nomes.

## 3. Sumário

Lista de links âncora para cada seção `##`/`###` do documento, na ordem em que
aparecem. Gerar por último, depois que a estrutura final estiver definida (os
slugs de âncora mudam se os títulos mudarem).

## 4. Visão geral

- Tabela: um módulo/serviço/componente por linha, com o que ele faz e (se
  aplicável) porta de API/frontend.
- Diagrama ASCII simples de como as peças se relacionam (setas de dependência,
  não um diagrama de sequência completo).
- Bullets de observações importantes de arquitetura (bancos isolados, quem fala
  com quem, invariantes que não são óbvias só olhando o diagrama).

## 5. Tecnologias

Tabela camada → tecnologia. Camadas típicas (usar só as que existirem de fato):
linguagem, orquestração de agente (LangGraph, um framework de agente, ou "n/a"),
API/backend, frontend (Streamlit, React, HTML/JS puro, CLI-only, etc.), banco de
dados, ORM/validação, LLM/gateway, embeddings, extração de PDF/OCR se houver,
testes, infraestrutura (Docker etc.). Linkar para `requirements.txt`/
`package.json` em vez de listar toda dependência transitiva.

## 6. Pré-requisitos

Linguagem + versão, ferramentas de sistema (Docker, Git, Tesseract, etc.),
chaves de API necessárias e o que quebra sem elas.

## 7. Instalação

Passo a passo de clone → venv/install de dependências → cópia de `.env.example`.
Se houver múltiplos `.env` (compartilhado + por módulo), explicar a distinção.

## 8. Executando o projeto

Todas as formas reais de rodar (Docker completo, Docker parcial + resto local,
scripts que sobem tudo de uma vez, rodar um módulo isolado) — só as que
existirem de verdade no código, cada uma com o comando exato. Fechar com "como
acessar" (URLs/portas).

## 9. Estrutura de pastas

Árvore ASCII gerada a partir de `ls`/`find` real da estrutura do projeto — nunca
inventada nem copiada de outro projeto.

## 10. Uma seção detalhada por módulo/serviço/fluxo

Uma por módulo real, idealmente dentro de um bloco `<details>` colapsável se
houver mais de 2-3 módulos (evita que o README fique gigante ao abrir). Dentro
de cada uma, o que existir de fato — adaptar o vocabulário ao que o módulo
realmente é:

| Se o módulo é... | "Como funciona o núcleo" vira... |
|---|---|
| Grafo LangGraph | Diagrama ASCII do grafo + tabela de nós e responsabilidades |
| API FastAPI/Flask/Express | Tabela de rotas/endpoints principais |
| Frontend React/Vue/JS puro | Árvore de componentes ou principais telas/interações |
| Pipeline/script único | Passo a passo do pipeline, sem forçar linguagem de "nó" |
| CLI-only | Tabela de subcomandos |

Sempre que existir, incluir: telas/rotas, variáveis de ambiente específicas
desse módulo, como rodar/testar esse módulo isolado.

## 11. Variáveis de ambiente

Separar: compartilhadas (na raiz, usadas por múltiplos módulos) vs. específicas
de cada módulo (linkar para a seção do módulo em vez de duplicar a tabela).

## 12. Testes

Comando de teste por módulo + o que cada suíte cobre (contagem de testes é um
bônus, não obrigatório — só incluir se for fácil de conferir e não ficar
desatualizado rápido demais). Separar testes offline (mockados) de testes de
integração que exigem serviços/chaves reais no ar.

## 13. Tipos de commit

Tabela padrão do manual Git do time (feat/fix/docs/test/refactor/perf/chore/ci, sem style/add, igual ao modelo de README do CLAUDE.md) — mesmo texto nos
dois idiomas, só a coluna de descrição muda.

## 14. Espelho completo em inglês

Segundo bloco `<details>` com TODAS as seções acima traduzidas — não só o
título e a tabela de commits. Ver `checklist-qualidade.md` para a verificação
de paridade.
