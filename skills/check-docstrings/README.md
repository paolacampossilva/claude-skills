# check-docstrings

A Claude skill that audits the docstrings and comments of a Python project for language and for staleness.

## Why

Checking by hand that every docstring and comment is in English, and that each one still matches the code it describes, means opening every file and comparing text against code. This skill does that pass for a whole project.

## How it works

1. Finds every `*.py` file under the project path, skipping `.venv*`, `venv`, `node_modules`, `site-packages`, `__pycache__`, `.git` and `.pytest_cache`.
2. Reads each file and classifies every docstring and `#` comment as Portuguese or English, using the rules in `references/deteccao-idioma.md`. Identifiers, example code, literal values and external contract names are not translated.
3. Compares each docstring with the code it documents, using the checks in `references/deteccao-desatualizado.md` (for example `Args:` that no longer match the signature, or a comment that refers to code that was removed). Only concrete, verifiable mismatches are flagged.
4. Translates Portuguese docstrings and comments to English right away.
5. Shows all staleness findings in one summary and asks which fixes to apply. It applies only the approved ones.
6. Prints a final report: files scanned, translations applied, staleness findings found, fixed and left out.

For large projects it can split the files across parallel agents.

## Expected input

The path to a Python project. If it is not given, the skill asks for it with `AskUserQuestion` instead of guessing.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file plus two reference files, and it has no command-line arguments other than the project path it receives from Claude.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Then ask Claude to check or audit the docstrings of a project, for example `/check-docstrings path/to/project`. The skill file does not restrict it to being called by name.

The instructions inside `SKILL.md` are written in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Grep`, `Glob`, `Bash`, `Write`, `Edit`, `Agent` and `AskUserQuestion` tools, and the shell command `find`. It only handles Python files.
