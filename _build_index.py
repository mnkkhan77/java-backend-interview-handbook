# -*- coding: utf-8 -*-
import os, re, glob, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))

# TRACKS is the top-level structure: one entry per "book" in the combined
# handbook, each holding its own GROUPS-style list of (group_name, nums).
# The sidebar renders a bold track heading above the first group of each
# track, so a technology switch (Java -> React -> AI) is visually obvious,
# not just implied by group names. Track/group ORDER controls display and
# reading order.
#
# Each track has its OWN chapter files in its own subfolder (java/, react/,
# ai-engineering/) and its OWN "num" sequence starting back at "01" -- a
# chapter's on-disk identity is (track, num), not num alone, since the same
# num string is reused across tracks. TRACK_FOLDER maps a track name to its
# subfolder; TRACK_SLUG gives the short id used internally by the reader's
# JS for routing/DOM ids (see chKey() in _handbook_template.html), since
# num alone is no longer globally unique.
TRACK_FOLDER = {
    "Java Backend Interview Handbook": "java",
    "React & Frontend Interview Handbook": "react",
    "AI Engineering & Production": "ai-engineering",
}
TRACK_SLUG = {
    "Java Backend Interview Handbook": "java",
    "React & Frontend Interview Handbook": "react",
    "AI Engineering & Production": "ai",
}

TRACKS = [
    ("Java Backend Interview Handbook", [
        ("Behavioural & HR", ["01", "02"]),
        ("Core Java", ["03", "04", "05", "06", "07", "08"]),
        ("Spring", ["09", "10", "11", "12", "13"]),
        ("Testing", ["14", "32"]),
        ("Design Patterns", ["15"]),
        ("APIs & Messaging", ["16", "17", "18"]),
        ("Architecture & Design", ["19", "20", "21"]),
        ("Database", ["22", "23"]),
        ("DevOps & Cloud", ["24", "25", "26", "31"]),
        ("Version Control & Build Tools", ["27", "28"]),
        ("Problem Solving (DSA)", ["29"]),
        ("Mock Interview", ["30"]),
    ]),
    ("React & Frontend Interview Handbook", [
        ("Behavioural & HR", ["01", "02"]),
        ("JavaScript & TypeScript", ["03", "04", "05"]),
        ("React Core", ["06", "07", "08", "09"]),
        ("State & Data", ["10", "11", "12", "13"]),
        ("Routing & Rendering", ["14", "15", "16"]),
        ("Performance & Internals", ["17", "18"]),
        ("Styling & UI", ["19", "20"]),
        ("Quality & Accessibility", ["21", "22", "23"]),
        ("Web Platform & Security", ["24", "25", "26", "27"]),
        ("Tooling & Architecture", ["28", "29"]),
        ("Problem Solving (DSA)", ["30"]),
    ]),
    ("AI Engineering & Production", [
        ("AI Foundations", ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25"]),
        ("Spring AI", ["26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40"]),
        ("Embeddings & RAG", ["41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53"]),
        ("AI Agents & MCP", ["54", "55", "56", "57", "58", "59", "60", "61", "62", "63"]),
        ("Enterprise AI Engineering", ["64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75"]),
        ("AI Production Projects", ["76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87"]),
        ("Advanced & Specialized Topics", ["88", "89", "90", "91", "92", "93"]),
        ("AI Engineer Interview Question Bank", ["94", "95", "96", "97", "98", "99", "100"]),
        ("Problem Solving (DSA)", ["101"]),
    ]),
]

# Flatten TRACKS into the GROUPS list the rest of the script expects, plus a
# lookup from group index -> the track it belongs to.
GROUPS = []
TRACK_OF_GROUP = {}
for _track_title, _groups in TRACKS:
    for _g in _groups:
        TRACK_OF_GROUP[len(GROUPS)] = _track_title
        GROUPS.append(_g)

TITLES = {
    "ai-engineering": {
        "01": "What Intelligence Really Means",
        "02": "History of AI",
        "03": "Machine Learning Fundamentals",
        "04": "Neural Networks",
        "05": "Deep Learning",
        "06": "Sequence Models",
        "07": "RNNs",
        "08": "LSTMs",
        "09": "Transformers",
        "10": "Attention",
        "11": "Query, Key, and Value",
        "12": "Multi-Head Attention",
        "13": "Positional Encoding",
        "14": "Decoder Architecture",
        "15": "Tokens",
        "16": "Embeddings",
        "17": "Vector Mathematics",
        "18": "Context Windows",
        "19": "Sampling",
        "20": "Hallucinations",
        "21": "Prompt Engineering",
        "22": "Context Engineering",
        "23": "Fine-Tuning",
        "24": "Reasoning Models",
        "25": "Introduction to RAG",
        "26": "Spring AI Architecture",
        "27": "ChatModel",
        "28": "ChatClient",
        "29": "Prompt",
        "30": "PromptTemplate",
        "31": "Advisors",
        "32": "Memory",
        "33": "Streaming",
        "34": "Structured Output",
        "35": "Tool Calling",
        "36": "Multi-model Support",
        "37": "MCP Integration",
        "38": "Observability",
        "39": "Testing",
        "40": "Performance Optimization",
        "41": "Embedding Models",
        "42": "Chunking",
        "43": "Vector Databases",
        "44": "pgvector",
        "45": "Pinecone",
        "46": "Qdrant",
        "47": "Weaviate",
        "48": "Hybrid Search",
        "49": "Reranking",
        "50": "Metadata Filtering",
        "51": "Retrieval Strategies",
        "52": "Enterprise RAG",
        "53": "Evaluation",
        "54": "Agent Fundamentals",
        "55": "Planning",
        "56": "Reflection",
        "57": "Agent Memory",
        "58": "Tool Usage",
        "59": "Agent Orchestration",
        "60": "Multi-Agent Systems",
        "61": "MCP Deep Dive",
        "62": "Agent Architectures",
        "63": "Enterprise Agents",
        "64": "Security",
        "65": "Guardrails",
        "66": "Prompt Injection",
        "67": "Evaluation at Enterprise Scale",
        "68": "Monitoring",
        "69": "Observability at Scale",
        "70": "Cost Optimization",
        "71": "Scaling",
        "72": "Kubernetes for AI Workloads",
        "73": "Distributed Systems for AI",
        "74": "Governance",
        "75": "Compliance",
        "76": "AI Chat Platform",
        "77": "Enterprise Knowledge Assistant",
        "78": "AI-Powered LMS",
        "79": "Resume Analyzer",
        "80": "SQL Copilot",
        "81": "Coding Assistant",
        "82": "Customer Support AI",
        "83": "Incident Analysis System",
        "84": "Document Intelligence Platform",
        "85": "Multi-Agent Research System",
        "86": "AI Voice Assistant",
        "87": "AI Workflow Automation Platform",
        "88": "Fine-Tuning Deep Dive (LoRA, QLoRA & PEFT)",
        "89": "Model Quantization & Local Deployment",
        "90": "Multi-Modal Models (Vision & Audio)",
        "91": "LLMOps & Model Lifecycle Management",
        "92": "Responsible AI, Safety & Ethics",
        "93": "AI Engineer Behavioural & Career Interview",
        "94": "AI & Machine Learning Fundamentals Interview Questions",
        "95": "Deep Learning, Transformers & Attention Interview Questions",
        "96": "Prompt Engineering, RAG & Embeddings Interview Questions",
        "97": "AI Agents, Tool Calling & MCP Interview Questions",
        "98": "Spring AI & Production AI Engineering Interview Questions",
        "99": "LLMOps, Fine-Tuning & Safety Interview Questions",
        "100": "AI Engineer Behavioural & Career Interview Questions",
        "101": "Data Structures & Algorithms for AI/ML Engineers",
    },
    "java": {
        "01": "Introduction & HR",
        "02": "Behavioural & Self-Intro",
        "03": "Core Java",
        "04": "Collections",
        "05": "Java 8 – 21",
        "06": "Concurrency & Multithreading",
        "07": "JVM & Garbage Collection",
        "08": "Modern Java Features (Records, Sealed Classes & Pattern Matching)",
        "09": "Spring Core",
        "10": "Spring Boot",
        "11": "Spring Data JPA & Hibernate",
        "12": "Spring Security, JWT & OAuth2",
        "13": "Reactive Programming (Project Reactor & WebFlux)",
        "14": "Unit Testing (JUnit & Mockito)",
        "15": "Design Patterns",
        "16": "REST API Design & Documentation",
        "17": "Messaging & Event Streaming",
        "18": "Kafka & Event-Driven Architecture Deep Dive",
        "19": "Microservices",
        "20": "System Design",
        "21": "Caching Strategies (Redis, Caffeine, Spring Cache)",
        "22": "SQL & Database Design",
        "23": "NoSQL & MongoDB",
        "24": "DevOps, Docker & Kubernetes",
        "25": "Cloud & AWS",
        "26": "Observability & Monitoring",
        "27": "Git & Version Control",
        "28": "Build Tools (Maven & Gradle)",
        "29": "Data Structures & Algorithms",
        "30": "Mock Interview — 1000 Questions",
        "31": "CI/CD Pipelines (Jenkins, GitHub Actions & GitLab CI)",
        "32": "Integration & Contract Testing (Testcontainers & Pact)",
    },
    "react": {
        "01": "Introduction & HR",
        "02": "Behavioural & Self-Introduction",
        "03": "JavaScript Fundamentals",
        "04": "Advanced JavaScript & Async",
        "05": "TypeScript for React",
        "06": "React Fundamentals",
        "07": "React Hooks",
        "08": "Advanced Hooks & Custom Hooks",
        "09": "Component Patterns",
        "10": "State Management",
        "11": "Data Fetching & Server State",
        "12": "Forms & Validation",
        "13": "GraphQL & Apollo Client",
        "14": "React Router & Navigation",
        "15": "Next.js, SSR & Server Components",
        "16": "React 19: Server Actions & Concurrent Features",
        "17": "Performance Optimization",
        "18": "React Internals (Fiber & Reconciliation)",
        "19": "Styling & CSS Architecture",
        "20": "Design Systems & Component Libraries",
        "21": "Testing (Jest & React Testing Library)",
        "22": "Accessibility (a11y)",
        "23": "End-to-End Testing (Cypress & Playwright)",
        "24": "Browser & Web Platform Fundamentals",
        "25": "Frontend Security",
        "26": "Progressive Web Apps & Service Workers",
        "27": "Internationalization (i18n)",
        "28": "Build Tools & Tooling",
        "29": "Frontend System Design",
        "30": "Data Structures & Algorithms (JavaScript)",
    },
}

def find_file(folder, num):
    # num-width-agnostic (java/react are <=99 chapters; ai-engineering has crossed into 3 digits)
    matches = glob.glob(os.path.join(ROOT, folder, num + "-*.html"))
    matches = [m for m in matches if os.path.basename(m)[:len(num)] == num]
    if not matches:
        raise SystemExit("No file for chapter %s in %s" % (num, folder))
    return os.path.basename(matches[0])

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
