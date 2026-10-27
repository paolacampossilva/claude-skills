# check-skills

A Claude skill that lists the skills you wrote yourself and shows which ones hand off to another skill.

## Why

Keeping track by hand of which personal skills exist, what each one does, and which ones call each other means opening every `SKILL.md`. This skill produces that inventory.

## How it works

1. Finds the skill folders in `~/.claude/skills/` (global) and in the current project's `.claude/skills/` (project-level).
2. Drops folders that match Anthropic's bundled skills (`pptx`, `docx`, `xlsx`, `pdf` and similar). If it is unsure about a folder, it asks.
3. Looks for relations between skills: first the `[Uses → x]` and `[Used by ← x]` tags at the start of a `description`, then mentions in the body of each `SKILL.md`, classified with `references/relacoes-entre-skills.md` as a real handoff or only a related scope.
4. Prints a short summary per skill, grouped into global and project-level. A skill that triggers another one is marked, so you do not run both for the same task. A skill that exists in both places is flagged as a duplicate.

## Expected input

None. It reads the two skill directories above.

## Running the scripts directly

There are no scripts. The skill is a `SKILL.md` file plus one reference file.

## Using it as a Claude skill

Copy this folder into `~/.claude/skills/` (or into a project's `.claude/skills/`), or upload it as a custom skill. Then ask Claude which skills you have or created. The skill file does not restrict it to being called by name.

The instructions inside `SKILL.md` are written in Portuguese, and the summaries it produces are in Portuguese.

## Stack

Markdown skill files. At run time it uses Claude Code's `Read`, `Glob`, `Bash` and `Agent` tools, and the shell commands `find` and `grep`.
