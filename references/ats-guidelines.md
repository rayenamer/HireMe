# ATS Formatting Checklist

Applicant Tracking Systems parse resumes into plain text before a human (or another algorithm) ever scores them. Anything that survives that parse as garbage or gets silently dropped costs the candidate a match, regardless of how good the content is. This checklist is what "make it ATS-friendly" means in practice.

## Structure
- **Single column.** Multi-column layouts get read left-to-right across columns by many parsers, scrambling the order (a skill from column 2 ends up mid-sentence in column 1's job description).
- **No tables.** Table cells are sometimes skipped entirely or read in the wrong order.
- **No text boxes, images, icons, or graphics** for content that matters (contact info, skill bars, logos-as-bullets). Parsers usually can't read text embedded in a text box or image at all.
- **No headers/footers** for anything essential (name, contact info) — many parsers never read the header/footer layer.
- **No columns of skill "pills" or graphical skill-level bars.** Use a plain comma-separated or bulleted list.

## Headings
Use standard, literal section headings the parser's dictionary recognizes:
- `Professional Summary` (or `Summary`)
- `Skills` (or `Core Skills` / `Technical Skills`)
- `Work Experience` (or `Experience` / `Professional Experience`)
- `Education`
- `Certifications`

Avoid cute/creative headings ("What I Bring to the Table") — parsers won't map them to a known field.

## Dates
Use a consistent, unambiguous format throughout: `Jan 2021 – Mar 2023`. Don't mix `01/2021`, `January 2021`, and `2021-01` in the same document. Use `Present` (not `Current` or a blank) for an ongoing role.

## Fonts and characters
- Stick to a standard, embedded-by-default font: Calibri, Arial, or Times New Roman, 10.5–12pt body text.
- Use a plain hyphen `-` or bullet `•` character for lists — not custom bullet glyphs, checkmarks, or emoji.
- Avoid special Unicode characters, symbols, or decorative dividers; they sometimes render as `?` or get stripped.

## File format
- `.docx` and text-based `.pdf` (not a scanned image) are the two safest formats. A `.pdf` exported from a scan or design tool with the text flattened to an image is invisible to an ATS.
- Filename should be plain and identifying: `FirstName_LastName_CV.docx` — avoid spaces-as-`%20`, version tags like `_FINAL_v3`, or special characters.

## Contact info
Put name, email, phone, location, and LinkedIn/portfolio as **plain text lines** at the top of the document body — not in a header, not in a text box, not as an image/logo link.

## Keywords
- Mirror the job description's own terminology where it's truthful to do so (if the CV says "customer facing analytics dashboards" and the JD says "customer-facing reporting tools," align the phrasing).
- Spell out acronyms at least once if the JD uses the long form, and vice versa (many ATS keyword matches are literal string matches — "Search Engine Optimization" and "SEO" are not automatically treated as the same token by every system).
- Don't keyword-stuff: a wall of skills with no supporting evidence in the experience section reads as padding to both ATS ranking heuristics and human reviewers.
