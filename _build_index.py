# -*- coding: utf-8 -*-
import os, re, glob, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))

# TRACKS is the top-level structure: one entry per "book" in the combined
# handbook, each holding its own GROUPS-style list of (group_name, nums).
# The sidebar renders a bold track heading above the first group of each
# track, so a technology switch (Java -> React -> AI) is visually obvious,
# not just implied by group names. Track/group ORDER controls display and
# reading order only — chapter "num" values are untouched, so existing
# links (e.g. #105-h5) keep working no matter where a track sits here.
TRACKS = [
    ("Java Backend Interview Handbook", [
        ("Behavioural & HR",       ["01", "14"]),
        ("Core Java",              ["02", "03", "04", "05", "06"]),
        ("Spring",                 ["07", "08", "09", "10"]),
        ("Testing",                ["16"]),
        ("Design Patterns",        ["18"]),
        ("APIs & Messaging",       ["21", "22"]),
        ("Architecture & Design",  ["11", "13"]),
        ("Database",               ["12", "23"]),
        ("DevOps & Cloud",         ["19", "20"]),
        ("Version Control",        ["24"]),
        ("Problem Solving (DSA)",  ["17"]),
        ("Mock Interview",         ["15"]),
    ]),
    # --- React / Frontend Interview Handbook (chapter numbers 112-135,
    # ported from react/*.html) — its own track between the Java interview
    # handbook above and the AI Engineering track below. ---
    ("React & Frontend Interview Handbook", [
        ("Behavioural & HR",        ["112", "135"]),
        ("JavaScript & TypeScript", ["113", "114", "115"]),
        ("React Core",              ["116", "117", "118", "119"]),
        ("State & Data",            ["120", "121", "122"]),
        ("Routing & Rendering",     ["123", "124"]),
        ("Performance & Internals", ["125", "126"]),
        ("Styling & UI",            ["127"]),
        ("Quality & Accessibility", ["128", "129"]),
        ("Web Platform & Security", ["130", "131"]),
        ("Tooling & Architecture",  ["132", "133"]),
        ("Problem Solving (DSA)",   ["134"]),
    ]),
    # --- Mastering AI Engineering with Java & Spring AI (chapter numbering
    # continues from 25 onward; one GROUPS entry per volume). Add a chapter's
    # number to a group only once its file actually exists. ---
    ("AI Engineering & Production", [
        ("AI Foundations",             ["25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49"]),
        ("Spring AI",                  ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64"]),
        ("Embeddings & RAG",           ["65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77"]),
        ("AI Agents & MCP",            ["78", "79", "80", "81", "82", "83", "84", "85", "86", "87"]),
        ("Enterprise AI Engineering",  ["88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99"]),
        ("AI Production Projects",     ["100", "101", "102", "103", "104", "105", "106", "107", "108", "109", "110", "111"]),
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
    "01": "Introduction & HR",
    "02": "Core Java",
    "03": "Collections",
    "04": "Java 8 – 21",
    "05": "Concurrency & Multithreading",
    "06": "JVM & Garbage Collection",
    "07": "Spring Core",
    "08": "Spring Boot",
    "09": "Spring Data JPA & Hibernate",
    "10": "Spring Security, JWT & OAuth2",
    "11": "Microservices",
    "12": "SQL & Database Design",
    "13": "System Design",
    "14": "Behavioural & Self-Intro",
    "15": "Mock Interview — 1000 Questions",
    "16": "Unit Testing (JUnit & Mockito)",
    "17": "Data Structures & Algorithms",
    "18": "Design Patterns",
    "19": "DevOps, Docker & Kubernetes",
    "20": "Cloud & AWS",
    "21": "REST API Design & Documentation",
    "22": "Messaging & Event Streaming",
    "23": "NoSQL & MongoDB",
    "24": "Git & Version Control",
    "25": "What Intelligence Really Means",
    "26": "History of AI",
    "27": "Machine Learning Fundamentals",
    "28": "Neural Networks",
    "29": "Deep Learning",
    "30": "Sequence Models",
    "31": "RNNs",
    "32": "LSTMs",
    "33": "Transformers",
    "34": "Attention",
    "35": "Query, Key, and Value",
    "36": "Multi-Head Attention",
    "37": "Positional Encoding",
    "38": "Decoder Architecture",
    "39": "Tokens",
    "40": "Embeddings",
    "41": "Vector Mathematics",
    "42": "Context Windows",
    "43": "Sampling",
    "44": "Hallucinations",
    "45": "Prompt Engineering",
    "46": "Context Engineering",
    "47": "Fine-Tuning",
    "48": "Reasoning Models",
    "49": "Introduction to RAG",
    "50": "Spring AI Architecture",
    "51": "ChatModel",
    "52": "ChatClient",
    "53": "Prompt",
    "54": "PromptTemplate",
    "55": "Advisors",
    "56": "Memory",
    "57": "Streaming",
    "58": "Structured Output",
    "59": "Tool Calling",
    "60": "Multi-model Support",
    "61": "MCP Integration",
    "62": "Observability",
    "63": "Testing",
    "64": "Performance Optimization",
    "65": "Embedding Models",
    "66": "Chunking",
    "67": "Vector Databases",
    "68": "pgvector",
    "69": "Pinecone",
    "70": "Qdrant",
    "71": "Weaviate",
    "72": "Hybrid Search",
    "73": "Reranking",
    "74": "Metadata Filtering",
    "75": "Retrieval Strategies",
    "76": "Enterprise RAG",
    "77": "Evaluation",
    "78": "Agent Fundamentals",
    "79": "Planning",
    "80": "Reflection",
    "81": "Agent Memory",
    "82": "Tool Usage",
    "83": "Agent Orchestration",
    "84": "Multi-Agent Systems",
    "85": "MCP Deep Dive",
    "86": "Agent Architectures",
    "87": "Enterprise Agents",
    "88": "Security",
    "89": "Guardrails",
    "90": "Prompt Injection",
    "91": "Evaluation at Enterprise Scale",
    "92": "Monitoring",
    "93": "Observability at Scale",
    "94": "Cost Optimization",
    "95": "Scaling",
    "96": "Kubernetes for AI Workloads",
    "97": "Distributed Systems for AI",
    "98": "Governance",
    "99": "Compliance",
    "100": "AI Chat Platform",
    "101": "Enterprise Knowledge Assistant",
    "102": "AI-Powered LMS",
    "103": "Resume Analyzer",
    "104": "SQL Copilot",
    "105": "Coding Assistant",
    "106": "Customer Support AI",
    "107": "Incident Analysis System",
    "108": "Document Intelligence Platform",
    "109": "Multi-Agent Research System",
    "110": "AI Voice Assistant",
    "111": "AI Workflow Automation Platform",
    "112": "Introduction & HR",
    "113": "JavaScript Fundamentals",
    "114": "Advanced JavaScript & Async",
    "115": "TypeScript for React",
    "116": "React Fundamentals",
    "117": "React Hooks",
    "118": "Advanced Hooks & Custom Hooks",
    "119": "Component Patterns",
    "120": "State Management",
    "121": "Data Fetching & Server State",
    "122": "Forms & Validation",
    "123": "React Router & Navigation",
    "124": "Next.js, SSR & Server Components",
    "125": "Performance Optimization",
    "126": "React Internals (Fiber & Reconciliation)",
    "127": "Styling & CSS Architecture",
    "128": "Testing (Jest & React Testing Library)",
    "129": "Accessibility (a11y)",
    "130": "Browser & Web Platform Fundamentals",
    "131": "Frontend Security",
    "132": "Build Tools & Tooling",
    "133": "Frontend System Design",
    "134": "Data Structures & Algorithms (JavaScript)",
    "135": "Behavioural & Self-Introduction",
}

def find_file(num):
    # num-width-agnostic: works for "07" (2-digit, chs 01-99) and, once the
    # AI Engineering track passes chapter 99, "100" (3-digit) alike.
    matches = glob.glob(os.path.join(ROOT, num + "-*.html"))
    matches = [m for m in matches if os.path.basename(m)[:len(num)] == num]
    if not matches:
        raise SystemExit("No file for chapter " + num)
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
    # strip any inner tags, collapse whitespace
    t = re.sub(r"<[^>]+>", "", raw)
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

for group_idx, (group_name, nums) in enumerate(GROUPS):
    track_name = TRACK_OF_GROUP[group_idx]
    for num in nums:
        fname = find_file(num)
        path = os.path.join(ROOT, fname)
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

        if new_content != content:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(new_content)

        # first h1 is the document title; the rest are navigable sub-sections (minus noise)
        chapter_title = TITLES.get(num, sections[0]["text"] if sections else fname)
        subs = []
        for i, s in enumerate(sections):
            if i == 0:
                continue
            if is_noise(s["text"]):
                continue
            subs.append(s)

        chapters.append({
            "num": num,
            "file": fname,
            "title": chapter_title,
            "group": group_name,
            "track": track_name,
            "sections": subs,
            "readMins": read_minutes(content),
        })

DATA = json.dumps(chapters, ensure_ascii=False)

# ---- render handbook.html (shell only -- chapter content is fetched on demand) ----
# handbook.html used to inline every chapter's <body> at build time. Now it ships
# just the sidebar/shell + the CHAPTERS metadata (titles, sections, read time --
# still needed for search/routing), and the reader's own JS fetches a chapter's
# standalone file (namespacing its heading ids the same way this script used to)
# the first time it's actually opened. See ensureChapterLoaded() in the template.
with open(os.path.join(ROOT, "_handbook_template.html"), "r", encoding="utf-8") as fh:
    hb_template = fh.read()

hb = hb_template.replace("var CHAPTERS = [];", "var CHAPTERS = " + DATA + ";", 1)
with open(os.path.join(ROOT, "handbook.html"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(hb)

total_subs = sum(len(c["sections"]) for c in chapters)
print("Chapters: %d, total sub-sections: %d" % (len(chapters), total_subs))
print("Generated: handbook.html (single-file, mobile-friendly)")
for c in chapters:
    print("  %s  %-32s  %2d sections  [%s]" % (c["num"], c["title"], len(c["sections"]), c["file"]))
