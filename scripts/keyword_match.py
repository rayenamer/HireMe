#!/usr/bin/env python3
"""Extract candidate keywords from a job description and check which ones
are already evidenced in a CV's plain text.

Usage: python3 keyword_match.py --cv cv.txt --job job.txt [--synonyms path]

Prints JSON to stdout:
  {
    "total_keywords": int,
    "matched": [str, ...],
    "missing": [str, ...],
    "match_score_percent": float
  }

This is a heuristic signal, not ground truth - deliberately dependency-free
(stdlib only) so it always runs. The calling skill is expected to re-check
"missing" entries against the CV's actual wording before treating them as
real gaps (see SKILL.md step 4).
"""
import argparse
import json
import os
import re

STOPWORDS = {
    "the", "and", "or", "with", "for", "a", "an", "to", "of", "in", "on",
    "is", "are", "will", "you", "we", "our", "your", "this", "that", "as",
    "be", "have", "has", "at", "by", "from", "us", "job", "role", "team",
    "years", "year", "experience", "skills", "ability", "strong", "work",
    "working", "including", "such", "etc", "using", "who", "what", "not",
    "all", "can", "may", "should", "must", "about", "into", "per",
    "requirements", "requirement", "qualifications", "qualification",
    "responsibilities", "responsibility", "nice", "familiarity",
    "knowledge", "background", "overview", "looking", "join", "join us",
    "preferred", "bonus", "plus", "you'll", "you will",
}

TRIGGER_PHRASES = [
    r"experience with ([^.\n]+)",
    r"experience in ([^.\n]+)",
    r"familiarity with ([^.\n]+)",
    r"proficien(?:cy|t) (?:in|with) ([^.\n]+)",
    r"knowledge of ([^.\n]+)",
    r"skilled in ([^.\n]+)",
    r"expertise in ([^.\n]+)",
    r"background in ([^.\n]+)",
]

DEFAULT_SYNONYMS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "references",
    "skill-synonyms.json",
)


def load_synonyms(path):
    if not path or not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    lookup = {}
    for canonical, aliases in data.items():
        variants = [canonical] + list(aliases)
        for v in variants:
            lookup.setdefault(v.lower(), set()).update(x.lower() for x in variants)
    return lookup


def split_candidates(chunk):
    parts = re.split(r",| and | or |/|;", chunk)
    out = []
    for p in parts:
        p = p.strip(" .()-")
        if p:
            out.append(p)
    return out


def extract_keywords(job_text):
    candidates = set()

    for pattern in TRIGGER_PHRASES:
        for m in re.finditer(pattern, job_text, flags=re.IGNORECASE):
            for c in split_candidates(m.group(1)):
                if 1 <= len(c.split()) <= 4:
                    candidates.add(c.strip())

    for line in job_text.splitlines():
        stripped = line.strip(" \t-*•")
        if re.match(r"^(skills?|requirements?|qualifications?|tech(?:nical)? stack)\s*[:\-]", stripped, re.IGNORECASE):
            after_colon = re.split(r"[:\-]", stripped, maxsplit=1)
            if len(after_colon) == 2:
                for c in split_candidates(after_colon[1]):
                    if 1 <= len(c.split()) <= 4:
                        candidates.add(c.strip())

    for m in re.finditer(r"\b([A-Z][A-Za-z0-9+.#]{1,15}(?:\s[A-Z][A-Za-z0-9+.#]{1,15}){0,2})\b", job_text):
        term = m.group(1).strip()
        low = term.lower()
        if low in STOPWORDS or len(term) < 2:
            continue
        candidates.add(term)

    cleaned = set()
    for c in candidates:
        c = re.sub(r"\s+", " ", c).strip()
        if not c or c.lower() in STOPWORDS:
            continue
        if len(c) < 2 or len(c) > 60:
            continue
        cleaned.add(c)
    return cleaned


def is_evidenced(keyword, cv_text_lower, synonyms):
    kw_lower = keyword.lower()
    if kw_lower in cv_text_lower:
        return True
    for variant in synonyms.get(kw_lower, set()):
        if variant in cv_text_lower:
            return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cv", required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--synonyms", default=DEFAULT_SYNONYMS_PATH)
    args = parser.parse_args()

    with open(args.cv, "r", encoding="utf-8") as f:
        cv_text = f.read()
    with open(args.job, "r", encoding="utf-8") as f:
        job_text = f.read()

    synonyms = load_synonyms(args.synonyms)
    keywords = extract_keywords(job_text)
    cv_text_lower = cv_text.lower()

    matched, missing = [], []
    for kw in sorted(keywords, key=str.lower):
        if is_evidenced(kw, cv_text_lower, synonyms):
            matched.append(kw)
        else:
            missing.append(kw)

    total = len(keywords)
    score = round((len(matched) / total) * 100, 1) if total else 0.0

    print(json.dumps({
        "total_keywords": total,
        "matched": matched,
        "missing": missing,
        "match_score_percent": score,
    }, indent=2))


if __name__ == "__main__":
    main()
