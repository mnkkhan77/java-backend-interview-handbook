# -*- coding: utf-8 -*-
import os, re, glob, json, html
from _chapters_data import TRACK_FOLDER, TRACK_SLUG, TRACKS, GROUPS, TRACK_OF_GROUP, TITLES, find_file as _find_file

ROOT = os.path.dirname(os.path.abspath(__file__))


def find_file(folder, num):
    return _find_file(ROOT, folder, num)

def is_noise(text):
    t = text.strip().upper()
    if t.endswith("COMPLETE"): return True
    if t.startswith("END OF"): return True
    if t.startswith("END "): return True
    if t == "END": return True
    if t.startswith("TOPICS"): return True
    if t == "NEXT MAJOR SECTION": return True
    return False

def clean_text(raw):
    # strip any inner tags (replacing with a space so e.g. "<span>JUNIOR</span>Q1." doesn't
    # collapse into "JUNIORQ1."), collapse whitespace
    t = re.sub(r"<[^>]+>", " ", raw)
    t = html.unescape(t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

WORDS_PER_MIN = 200  # a commonly cited average adult silent-reading speed

def read_minutes(raw_html):
    # strip tags/entities, count word-ish tokens, convert to a rounded read time
    text = re.sub(r"<[^>]+>", " ", raw_html)
    text = html.unescape(text)
    words = re.findall(r"[A-Za-z0-9']+", text)
    return max(1, round(len(words) / WORDS_PER_MIN))

chapters = []
search_index = []

for group_idx, (group_name, nums) in enumerate(GROUPS):
    track_name = TRACK_OF_GROUP[group_idx]
    folder = TRACK_FOLDER[track_name]
    slug = TRACK_SLUG[track_name]
    for num in nums:
        fname = find_file(folder, num)
        path = os.path.join(ROOT, folder, fname)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()

        counter = {"n": 0}
        sections = []

        def repl(m):
            counter["n"] += 1
            hid = "h%d" % counter["n"]
            inner = m.group(1)
            sections.append({"id": hid, "text": clean_text(inner)})
            return '<h1 id="%s">%s</h1>' % (hid, inner)

        # match any <h1> (with or without existing attributes) and re-stamp a clean
        # sequential id -> fully idempotent: same output on every run.
        new_content = re.sub(r"<h1[^>]*>(.*?)</h1>", repl, content, flags=re.DOTALL)

        qcounter = {"n": 0}
        questions = []

        def qrepl(m):
            qcounter["n"] += 1
            qid = "q%d" % qcounter["n"]
            inner = m.group(1)
            questions.append({"id": qid, "text": clean_text(inner)})
            return '<div class="question" id="%s">%s</div>' % (qid, inner)

        # every chapter's "question" divs (the interview-handbook Q&A blocks, and the
        # embedded mini Q&A in the 16-section AI textbook chapters alike) get the same
        # sequential-id treatment, so the global search index can deep-link to one.
        # Match with or without an existing id (same idempotency trick as the <h1> pass
        # above) -- otherwise a second run, finding ids already stamped, matches nothing
        # and silently regenerates an empty search index.
        new_content = re.sub(r'<div class="question"[^>]*>(.*?)</div>', qrepl, new_content, flags=re.DOTALL)

        if new_content != content:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(new_content)

        # first h1 is the document title; the rest are navigable sub-sections (minus noise)
        chapter_title = TITLES[folder].get(num, sections[0]["text"] if sections else fname)
        subs = []
        for i, s in enumerate(sections):
            if i == 0:
                continue
            if is_noise(s["text"]):
                continue
            subs.append(s)

        chapter_idx = len(chapters)
        chapters.append({
            "num": num,
            "trackSlug": slug,
            "file": folder + "/" + fname,
            "title": chapter_title,
            "group": group_name,
            "track": track_name,
            "sections": subs,
            "readMins": read_minutes(content),
            "qCount": len(questions),
        })

        # global search index: one [chapterIdx, questionId, text] triple per question,
        # across every chapter/track -- compact arrays (not objects) keep the embedded
        # payload smaller than repeating key names ~3-4k times.
        for q in questions:
            text = q["text"]
            if len(text) > 240:
                text = text[:240].rstrip() + "…"
            search_index.append([chapter_idx, q["id"], text])

DATA = json.dumps(chapters, ensure_ascii=False)
SEARCH_DATA = json.dumps(search_index, ensure_ascii=False)

# ---- render handbook.html (shell only -- chapter content is fetched on demand) ----
# handbook.html used to inline every chapter's <body> at build time. Now it ships
# just the sidebar/shell + the CHAPTERS metadata (titles, sections, read time --
# still needed for search/routing), and the reader's own JS fetches a chapter's
# standalone file (namespacing its heading ids the same way this script used to)
# the first time it's actually opened. See ensureChapterLoaded() in the template.
with open(os.path.join(ROOT, "_handbook_template.html"), "r", encoding="utf-8") as fh:
    hb_template = fh.read()

hb = hb_template.replace("var CHAPTERS = [];", "var CHAPTERS = " + DATA + ";", 1)
hb = hb.replace("var SEARCH_INDEX = [];", "var SEARCH_INDEX = " + SEARCH_DATA + ";", 1)
hb = hb.replace("{{CHAPTER_COUNT}}", str(len(chapters)), 1)
with open(os.path.join(ROOT, "handbook.html"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(hb)

# ---- render quiz.html (randomized flashcard quiz shell) ----
# Same CHAPTERS metadata (now carrying qCount per chapter) drives the topic
# picker; quiz.html fetches each selected chapter's standalone file on demand
# at quiz time, the same lazy pattern handbook.html uses for reading, so the
# question/answer text itself is never duplicated into a build artifact.
with open(os.path.join(ROOT, "_quiz_template.html"), "r", encoding="utf-8") as fh:
    quiz_template = fh.read()

quiz_html = quiz_template.replace("var CHAPTERS = [];", "var CHAPTERS = " + DATA + ";", 1)
with open(os.path.join(ROOT, "quiz.html"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(quiz_html)

total_subs = sum(len(c["sections"]) for c in chapters)
print("Chapters: %d, total sub-sections: %d, indexed questions: %d" % (len(chapters), total_subs, len(search_index)))
print("Generated: handbook.html (single-file, mobile-friendly)")
print("Generated: quiz.html (randomized flashcard quiz)")
for c in chapters:
    print("  %s/%-2s  %-32s  %2d sections  [%s]" % (c["trackSlug"], c["num"], c["title"], len(c["sections"]), c["file"]))
