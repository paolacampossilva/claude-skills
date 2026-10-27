# synch-bilingual-docs

A Claude skill that checks every Markdown file inside a `docs/` folder for a complete, synchronized Portuguese and English version, and fixes what is missing.

## Why

Keeping each document in a `docs/` folder bilingual means reading both sides of every file and comparing them by hand. This skill does the comparison and writes the missing English text.

## How it works

1. Finds every `*.md` file under the given `docs/` path, at any depth, except files named `README.md` (those belong to `synch-bilingual-readmes`) and dependency or cache folders.
2. Marks the files that have no English block (no 🇺🇸 marker) without reading them in full.
3. For the others, checks that both blocks have the same sections in the same order and the same concrete entities (commands, variables, endpoints, numbers, file paths), using the method in `../synch-bilingual-readmes/references/deteccao-e-sincronia.md`.
4. Fixes directly, with no confirmation step. Portuguese is the source of truth: it creates the full English mirror when it is missing, or edits only the English block when the two have drifted apart.
5. Reports each file as already in sync, mirror created, or synchronized, with a short note on what changed.

Non-Markdown files that the docs reference (`.csv`, `.json`, `.pdf`, `.png`) are not read or changed. Their paths are only kept identical in the English block.

It does not invent content and does not change the Portuguese text. If a document is wrong in Portuguese, it only reports that.

## Expected input

The path to a `docs/` folder. If it is not given, the skill asks for it. It never searches a project for `docs/` folders on its own.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file. It has no reference file of its own and uses the one from `synch-bilingual-readmes`.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Copy `synch-bilingual-readmes` next to it, because its reference file is required. Then ask Claude to check or sync the bilingual docs in a given `docs/` folder. The skill file does not restrict it to being called by name.

The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit` and `Agent` tools, and the shell commands `find` and `grep`.
