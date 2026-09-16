# HireMe

A [Claude Code](https://claude.com/claude-code) skill that tailors an existing CV to a specific job description — reordering and rewording truthful content to speak the job posting's language and pass ATS (Applicant Tracking System) parsing — **without inventing a different work history.**

It will not add employers you never worked for, job titles you never held, dates that don't match, or skills you don't have. It rewrites the *presentation* of a real CV; it does not write a fictional one. See [`SKILL.md`](SKILL.md) for the full non-negotiable rules.

## What it does

Given a CV and a target job description, it:

1. Extracts plain text from either (PDF, DOCX, Markdown, or plain text).
2. Runs a keyword match to see which of the job description's requirements are already evidenced in the CV, and which aren't.
3. For any real gaps, asks you directly whether you actually have that skill — it never assumes.
4. Rewrites the summary, reorders/rewords bullet points, and reorders the skills section to mirror the job's terminology, using only truthful, existing content.
5. Reformats the result to be ATS-friendly (single column, standard headings, plain fonts, no tables/graphics — see [`references/ats-guidelines.md`](references/ats-guidelines.md)).
6. Outputs a tailored CV (`.md` and, if `python-docx` is installed, `.docx`) plus a match report explaining exactly what changed and why.

## Installation

This whole folder *is* the skill. Drop it into a Claude Code skills directory, either:

**As a personal skill (all your projects):**
```bash
git clone <this-repo-url> ~/.claude/skills/hireme
```

**As a project skill (this repo only):**
```bash
git clone <this-repo-url> path/to/your-project/.claude/skills/hireme
```

Or if you're not using git, just copy the folder to one of those two locations, keeping the name `hireme` (or any name — the skill picks up its trigger from `SKILL.md`'s frontmatter either way).

### Requirements
- Python 3 (used for keyword matching and DOCX conversion — no pip installs required for the basics).
- Optional: `pip install python-docx` — enables reading `.docx` CVs precisely and generating a tailored `.docx` output. Without it, the skill still works fully via Markdown/plain-text and PDF input, and always produces a clean `.md` output.

## Usage

Inside a Claude Code session:

```
/hireme --cv path/to/your_cv.pdf --job path/to/job_description.txt
```

You can also paste the job description directly instead of pointing to a file:

```
/hireme --cv path/to/your_cv.docx --job "Backend Engineer role requiring Python, Kubernetes, ..."
```

Or just run `/hireme` with no arguments — Claude will look for an obvious CV/job description file in the current directory, or ask you for one.

### Try it on the bundled example
```
cd hireme   # wherever you installed/cloned this skill
claude
> /hireme --cv examples/sample-cv.md --job examples/sample-job-description.txt
```

This produces, in `output/`:
- `tailored_cv_<Company>_<Role>.md` — the rewritten CV
- `tailored_cv_<Company>_<Role>.docx` — same, as a Word doc (if `python-docx` is installed)
- `match_report_<Company>_<Role>.md` — keyword match score, what changed, and what was intentionally left alone

## Why not just have an LLM write a "perfect match" CV from scratch?

Because that's how people end up with resumes that don't survive a background check or a follow-up interview question about a skill listed on page one. This skill is built around a narrower, more defensible idea: your real experience, described in the language the job posting uses, formatted so a parser doesn't mangle it. If the job wants something you genuinely don't have, the skill will tell you that's a gap instead of quietly inventing it.

## Repository layout

```
SKILL.md                        the skill definition Claude Code reads
README.md                       this file
scripts/
  docx_to_text.py                .docx -> plain text (python-docx, or a stdlib-only fallback)
  text_to_docx.py                structured Markdown -> ATS-friendly .docx (needs python-docx)
  keyword_match.py                extracts JD keywords, checks which are evidenced in the CV
references/
  ats-guidelines.md               ATS formatting checklist used by the skill
  skill-synonyms.json             alias table (JS/JavaScript, K8s/Kubernetes, etc.)
examples/
  sample-cv.md
  sample-job-description.txt
output/                          generated CVs and match reports land here (gitignored)
```

## License

MIT — use it, fork it, redistribute it.
# HireMe
