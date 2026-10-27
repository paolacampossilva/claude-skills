# claude-skills

A collection of personal Claude skills for working on code and documentation: auditing docstrings, keeping READMEs and docs bilingual (Portuguese and English), and listing your own skills. Each skill lives in its own folder under `skills/` with its own README. They are Markdown instructions for Claude, so there is nothing to install beyond copying a folder into `~/.claude/skills/` or uploading it as a custom skill.

## Skills

- [check-docstrings](skills/check-docstrings): finds Portuguese docstrings and comments in a Python project, translates them to English, and reports stale ones for you to approve.
- [check-skills](skills/check-skills): lists the skills you wrote yourself and shows which ones hand off to another.
- [synch-bilingual-docs](skills/synch-bilingual-docs): checks every Markdown file in a `docs/` folder for a Portuguese and English version and fixes the English side.
- [synch-bilingual-readmes](skills/synch-bilingual-readmes): checks every `README.md` in a project for a Portuguese and English version and fixes the English side.

`synch-bilingual-docs` reads a reference file from `synch-bilingual-readmes`, so keep the two together.
