# Detectar relações entre skills sem tag `[Uses → x]`/`[Used by ← x]`

Usar este arquivo quando uma skill não tem a tag de relação no início da
`description`, ou quando é preciso confirmar se uma menção em prosa é handoff
real ou só relação de escopo.

## Varredura textual (fallback)

Skills também podem se referenciar por nome em prosa dentro do próprio
`SKILL.md` (corpo do arquivo, não só frontmatter) sem usar a tag ainda — é
assim que uma skill delega/repassa trabalho para outra. Detectar isso antes
de reportar, para não listar duas skills acopladas como se fossem
independentes:

```bash
grep -lE "$(ls -1 ~/.claude/skills/ .claude/skills/ 2>/dev/null | paste -sd'|')" ~/.claude/skills/*/SKILL.md .claude/skills/*/SKILL.md 2>/dev/null
```

Ou, mais preciso, para cada skill A: `grep -n "<nome-da-skill-B>"` no corpo de
`A/SKILL.md` para cada outra skill B da lista (ignorando autorreferência).

## Classificar cada ocorrência encontrada (tag ou prosa)

- **Handoff/dependência real** — linguagem como "hands off to", "repassa
  para", "invoca", "chama a skill", "follow the X skill's own instructions",
  "Only use this skill when Y hands off". Aqui rodar as duas skills
  separadamente para a mesma tarefa duplica trabalho: uma já aciona a outra.
- **Relação de escopo (não é duplicação)** — linguagem como "complementa",
  "irmã de", "escopo disjunto", "nunca tocam o mesmo arquivo". Aqui as duas
  skills são independentes e cobrem coisas diferentes — não é risco de rodar
  as duas.

Na dúvida sobre qual das duas categorias uma menção se encaixa, ler a frase
completa em vez de assumir pelo verbo isolado.
