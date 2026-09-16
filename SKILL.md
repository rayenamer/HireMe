---
name: hireme
description: "Use when the user gives a CV/resume plus a target job description and wants the CV tailored to that job — rewording bullets, reordering skills, and mirroring the job description's language so it reads as an ATS-friendly match. Never invents employers, job titles, dates, degrees, or skills the candidate doesn't have — it only reorders and rewords truthful content. Trigger: /hireme"
---

# /hireme

Tailor an existing CV to a specific job description: match terminology, reorder content by relevance, and format for ATS parsing — without changing the candidate's actual work history.

## Usage

```
/hireme --cv path/to/cv.pdf --job path/to/job_description.txt
/hireme --cv path/to/cv.docx --job "<paste the job description text directly>"
/hireme                                    # auto-detect cv/job files in the current directory, or ask for them
/hireme --cv path/to/cv.md --job path/to/job.txt --out ./output
```

`--cv` and `--job` each accept a file path (`.pdf`, `.docx`, `.md`, `.txt`) or literal pasted text. `--out` is optional (defaults to `./output`).

## What this skill is — and is not

This skill **rewrites the presentation of a real CV**, it does not write a fictional one. It:

- Rewords existing bullet points using the job description's terminology, when that rewording stays truthful to what the bullet already says.
- Reorders bullets and skills so the most relevant-to-this-job items lead.
- Rewrites the professional summary/headline to mirror the target role's language, grounded in the candidate's actual background.
- Restructures formatting so an ATS parser reads it cleanly.

It never invents anything. See **Non-negotiable rules** below — these override any instinct to "make the match look better."

## Non-negotiable rules

1. **Never change employers, job titles held, employment dates, education, certifications, or their order.** These are copied verbatim from the original CV. Do not add, remove, merge, split, or reorder positions/degrees.
2. **Never fabricate or exaggerate a skill, tool, metric, or accomplishment.** If the job description wants a skill the CV doesn't evidence, do not add it silently.
3. **Never invent numbers.** Existing metrics (%, $, team size, counts) are copied exactly; never adjusted upward or invented where none existed.
4. **The candidate's actual most recent job title is never changed to match the target job title.** The summary/headline may echo the target role's language ("Backend Engineer with 4 years building distributed systems") if that's a truthful characterization — it must never claim they *held* a title they didn't.
5. **When in doubt, ask.** If a job description lists a requirement (e.g. "Kubernetes") that isn't clearly evidenced anywhere in the CV, do not add it on the CV's behalf — ask the user in one batched question whether they actually have that experience, and only include it if they confirm.

Everything else in this document is process; these five rules are the point of the skill.

## Step-by-step process

### 1. Resolve inputs
Parse `--cv` and `--job` from the invocation. If either is missing, look in the current directory for an obvious candidate (`cv.*`, `resume.*`, `job*.txt`, `jd*.*`, `job_description.*`); if still ambiguous or absent, ask the user to provide or paste it. Don't guess silently.

### 2. Extract plain text
- `.pdf` → read directly with the Read tool (native PDF support).
- `.docx` → run `python3 scripts/docx_to_text.py <path>`, capture stdout.
- `.md` / `.txt` → read directly with the Read tool.
- Pasted text → use as-is.

Save the extracted CV text and job description text to two temp files in the scratchpad (e.g. `cv.txt`, `job.txt`) — the next step's script needs file paths.

### 3. Run the keyword match
```
python3 scripts/keyword_match.py --cv <cv.txt> --job <job.txt>
```
This returns JSON: `matched` keywords (already present in the CV, in the JD's vocabulary), `missing` keywords (JD wants them, CV text doesn't evidence them), and a `match_score_percent`. Treat this as a starting signal, not ground truth — use your own reading of the CV to catch synonyms the script missed (e.g. CV says "led a squad of 6 engineers," JD wants "team leadership" — that's a match even if the script didn't catch the phrasing).

### 4. Resolve gaps honestly
For each item in `missing`, re-read the CV's actual bullet content (not just keyword presence) to judge if it's truly absent or just worded differently:
- If genuinely evidenced under different words → note it as a match, plan to reword that bullet toward the JD's phrasing.
- If not evidenced at all → do **not** add it. Collect these as open questions.

If there are unresolved gaps for skills that plausibly matter (i.e., not throwaway nice-to-haves), ask the user in a single batched question (e.g. via AskUserQuestion) — "The job asks for X, Y, Z — do you have hands-on experience with any of these?" — before finalizing. Only incorporate what they confirm. If they don't confirm or don't answer, leave the CV as-is on that point and mention the gap in the match report instead of guessing.

### 5. Rewrite the CV
Applying the Non-negotiable rules above:
- Rewrite the summary/headline to foreground the target role and the top 3-5 truthful, matched keywords.
- Within each job, reorder bullets so JD-relevant achievements lead; reword bullets to use the JD's terms where the underlying fact matches (e.g. CV says "wrote automated tests," JD says "test automation" → align the phrasing).
- Reorder the Skills section so JD-matching skills are listed first; keep every original skill, just reordered/regrouped (e.g. group into "Languages," "Tools," "Other").
- Do not touch the employment history's facts, order, dates, employers, or titles.
- Keep length roughly the same as the original — this is a re-tailoring, not an expansion.

### 6. Format for ATS
Follow `references/ats-guidelines.md`. In short: single column, standard section headers, no tables/text boxes/images/columns/headers-footers, standard font, consistent `Mon YYYY` dates, plain `- ` or `• ` bullets (not decorative icons).

Write the rewritten CV as a structured Markdown file using this convention (consumed by the docx generator in the next step):
```
# Full Name
contact line: email · phone · location · linkedin (plain text, one line)

## Professional Summary
...paragraph...

## Skills
- Category: item, item, item

## Work Experience
### Job Title — Company (Mon YYYY – Mon YYYY)
- bullet
- bullet

## Education
### Degree — Institution (Year)

## Certifications
- item
```

### 7. Generate outputs
- Always write the Markdown version: `<out>/tailored_cv_<Company>_<Role>.md`.
- Try to also generate a `.docx`: `python3 scripts/text_to_docx.py <markdown_file> <out>/tailored_cv_<Company>_<Role>.docx`. If it reports `python-docx` isn't installed, tell the user how to get the `.docx` (`pip install python-docx`, or open the `.md` and paste into Word/Google Docs) — don't treat it as a hard failure.
- Write a match report: `<out>/match_report_<Company>_<Role>.md` containing: match score before/after, keywords matched, keywords intentionally left out (and why), the specific rewording/reordering changes made, and any open questions the user should confirm.

### 8. Summarize for the user
In chat, give a short summary: match score improvement, what changed, what was intentionally left untouched, and any gaps flagged for the user's own honest confirmation. Don't restate the whole match report — point to the file.

## Files in this skill
- `scripts/docx_to_text.py` — extract plain text from a `.docx` CV (uses `python-docx` if available, falls back to a stdlib-only OOXML reader).
- `scripts/text_to_docx.py` — generate an ATS-friendly `.docx` from the structured Markdown convention above (requires `python-docx`).
- `scripts/keyword_match.py` — extract candidate keywords from a job description and check which are already evidenced in the CV text.
- `references/ats-guidelines.md` — full ATS formatting checklist.
- `references/skill-synonyms.json` — alias table so "JS" matches "JavaScript," "K8s" matches "Kubernetes," etc.
- `examples/` — a sample CV and job description to try the skill on.
