# synch-bilingual-readmes

A Claude skill that checks every `README.md` in a project for a complete, synchronized Portuguese and English version, and fixes what is missing.

## Why

Keeping a Portuguese README and its English mirror in step means reading both sides of every README and comparing sections, commands and variables by hand. This skill does the comparison and writes the missing English text.

## How it works

1. Finds every `README.md` under the project path, skipping `.venv*`, `venv`, `node_modules`, `site-packages`, `.pytest_cache`, `.git` and `__pycache__`.
2. Marks the READMEs that have no English block (no 🇺🇸 marker) without reading them in full.
3. For the others, checks that both blocks have the same sections in the same order and the same concrete entities (commands, environment variables, endpoints, numbers), following `references/deteccao-e-sincronia.md`.
4. Fixes directly, with no confirmation step. Portuguese is the source of truth: it creates the full English mirror when it is missing, or edits only the English block when the two have drifted apart.
5. Reports each README as already in sync, mirror created, or synchronized, with a short note on what changed.

The expected format is two collapsible `<details>` blocks, one with the `🇧🇷 pt-br` summary and one with the `🇺🇸 en` summary.

It does not invent content and does not change the Portuguese text. If a README is wrong in Portuguese, it only reports that.

## Expected input

The path to a project. If it is not given, the skill asks for it instead of guessing.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file plus one reference file, which is shared with `synch-bilingual-docs`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Then ask Claude to check or sync the bilingual READMEs of a project. The skill file does not restrict it to being called by name.

If you also use `synch-bilingual-docs`, keep both folders side by side, because that skill reads this one's reference file.

The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit` and `Agent` tools, and the shell commands `find` and `grep`.
