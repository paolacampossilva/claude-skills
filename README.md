<details open>
<summary><b>🇧🇷 pt-br</b> — claude-skills</summary>
<br>

# claude-skills

Coleção de skills pessoais do Claude para trabalhar com código e documentação, mais algumas que geram arquivos: auditar docstrings, manter READMEs e docs bilíngues (português e inglês), listar as próprias skills, sugerir commits, revisar PRs de colegas, explicar projetos, planejar e gerar apresentações de sprint, gerar gráficos de notas escolares e montar PDFs de estudo. Cada skill fica em uma pasta própria dentro de `skills/`, com README próprio. Cada skill é um conjunto de instruções para o Claude, então usar uma significa copiar a pasta dela para `~/.claude/skills/` ou enviá-la como skill personalizada. As skills que incluem scripts Python precisam dos pacotes do `requirements.txt`.

## Skills

- [check-docstrings](skills/check-docstrings): encontra docstrings e comentários em português num projeto Python, traduz para inglês e aponta os desatualizados para você aprovar.
- [check-skills](skills/check-skills): lista as skills que você escreveu e mostra quais delegam trabalho a outra.
- [create-main-readme](skills/create-main-readme): cria ou corrige o `README.md` principal de um projeto num esqueleto fixo, bilíngue, adaptando o conteúdo ao que o projeto tem e mostrando um plano antes de escrever.
- [explain-project](skills/explain-project): escreve um `.md` didático em duas camadas (sem jargão e avançada), no modo retrospectivo ou de processo novo.
- [review-teammate-prs](skills/review-teammate-prs): acha os PRs de colegas sem a sua aprovação, abertos ou mergeados, revisa com um checklist e entrega rascunhos de comentário e os comandos `gh pr review`, sem postar nada.
- [sprint-slides](skills/sprint-slides): planeja o conteúdo de uma apresentação de fim de sprint para um público não técnico e, aprovado o roteiro, passa para a `template-slides`.
- [suggest-commits](skills/suggest-commits): sugere commits agrupados por tipo e escopo para o que está pendente num repositório, sem executar nada.
- [template-slides](skills/template-slides): gera o deck `.pptx` numa identidade visual fixa, a partir de conteúdo pronto.
- [create-chart](skills/create-chart): transforma uma planilha de notas escolares em um gráfico de barras por turma, entregue num .zip.
- [merge-charts](skills/merge-charts): gera os gráficos do simulado, os bimestrais e a comparação por turma a partir de duas planilhas, numa execução só.
- [colorful-summary-pdf](skills/colorful-summary-pdf): transforma anotações, slides ou documentos longos num PDF de estudo colorido.
- [synch-bilingual-docs](skills/synch-bilingual-docs): confere se cada arquivo Markdown de uma pasta `docs/` tem versão em português e inglês e corrige o lado em inglês.
- [synch-bilingual-readmes](skills/synch-bilingual-readmes): confere se cada `README.md` de um projeto tem versão em português e inglês e corrige o lado em inglês.

`synch-bilingual-docs` lê um arquivo de referência de `synch-bilingual-readmes`, então mantenha as duas juntas. O mesmo vale para `sprint-slides` e `template-slides`: a primeira passa o roteiro aprovado para a segunda. Nome do time, integrantes, orientadores e logos da `template-slides` não vêm na skill, e ela os pede quando faltam.

## Configuração dos scripts

```bash
pip install -r requirements.txt
```

O `openpyxl` é usado por `create-chart` e `merge-charts` para ler arquivos `.xlsx`. Ler arquivos `.numbers` exige também o pacote opcional `numbers-parser`.

Pacotes de sistema opcionais: `colorful-summary-pdf` renderiza fórmulas com `pdflatex` quando LaTeX e poppler estão instalados, por exemplo `apt-get install -y texlive-latex-base texlive-latex-extra poppler-utils`. Sem eles, usa o matplotlib como alternativa.

</details>

---

<details>
<summary><b>🇺🇸 en</b> — claude-skills</summary>
<br>

# claude-skills

A collection of personal Claude skills for working on code and documentation, plus a few that generate files: auditing docstrings, keeping READMEs and docs bilingual (Portuguese and English), listing your own skills, suggesting commits, reviewing teammates' PRs, explaining projects, planning and generating sprint presentations, charting school grades and building study-guide PDFs. Each skill lives in its own folder under `skills/` with its own README. Each skill is a set of instructions for Claude, so using one means copying its folder into `~/.claude/skills/` or uploading it as a custom skill. The skills that include Python scripts need the packages in `requirements.txt`.

## Skills

- [check-docstrings](skills/check-docstrings): finds Portuguese docstrings and comments in a Python project, translates them to English, and reports stale ones for you to approve.
- [check-skills](skills/check-skills): lists the skills you wrote yourself and shows which ones hand off to another.
- [create-main-readme](skills/create-main-readme): creates or fixes a project's main `README.md` in a fixed, bilingual skeleton, adapting the content to what the project has and showing a plan before writing.
- [explain-project](skills/explain-project): writes a didactic `.md` in two layers (plain and advanced), in retrospective or new-process mode.
- [review-teammate-prs](skills/review-teammate-prs): finds teammates' PRs without your approval, open or merged, reviews them with a checklist and delivers draft comments and the `gh pr review` commands, without posting anything.
- [sprint-slides](skills/sprint-slides): plans the content of an end-of-sprint presentation for a non-technical audience and, once the outline is approved, hands off to `template-slides`.
- [suggest-commits](skills/suggest-commits): suggests commits grouped by type and scope for what is pending in a repository, without running anything.
- [template-slides](skills/template-slides): generates the `.pptx` deck in a fixed visual identity from finished content.
- [create-chart](skills/create-chart): turns a school grades spreadsheet into one bar chart per class, delivered as a .zip.
- [merge-charts](skills/merge-charts): builds the simulado charts, the bimonthly charts and a per-class comparison from two spreadsheets in one run.
- [colorful-summary-pdf](skills/colorful-summary-pdf): turns notes, slides or long documents into a colorful study-guide PDF.
- [synch-bilingual-docs](skills/synch-bilingual-docs): checks every Markdown file in a `docs/` folder for a Portuguese and English version and fixes the English side.
- [synch-bilingual-readmes](skills/synch-bilingual-readmes): checks every `README.md` in a project for a Portuguese and English version and fixes the English side.

`synch-bilingual-docs` reads a reference file from `synch-bilingual-readmes`, so keep the two together. The same goes for `sprint-slides` and `template-slides`: the first hands the approved outline to the second. The team name, members, advisors and logos of `template-slides` do not ship with the skill, and it asks for them when missing.

## Setup for the scripts

```bash
pip install -r requirements.txt
```

`openpyxl` is needed by `create-chart` and `merge-charts` to read `.xlsx` files. Reading `.numbers` files also needs the optional `numbers-parser` package.

Optional system packages: `colorful-summary-pdf` renders formulas with `pdflatex` when LaTeX and poppler are installed, for example `apt-get install -y texlive-latex-base texlive-latex-extra poppler-utils`. Without them it falls back to matplotlib.

</details>
