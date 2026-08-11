# Java Backend Interview Handbook

A mobile-friendly handbook covering three tracks in one single app, one reader: **Senior Java Backend Engineer** interview prep, a **React / Frontend Engineer** interview handbook, and a full **AI Engineering with Java & Spring AI** track. The sidebar reads Java → React → AI Engineering, in that order, even though chapter numbers are not contiguous across tracks (see the numbering note in each section below). Interview chapters (Java: 01–24, React: 112–135) carry high-ROI questions, sample answers, code, and "interview gold point" follow-ups; the AI Engineering chapters (25–111) are deep, book-style chapters (motivation → theory → internals → math → production architecture → Spring AI mapping → interview questions) covering everything from ML foundations through Spring AI, RAG, agents, and enterprise AI systems.

### 🌐 Live site: **[inter-lyart.vercel.app](https://inter-lyart.vercel.app)**

> The live site is [`handbook.html`](handbook.html) — a searchable, dark-mode-enabled reader shell (~150 KB) that fetches each chapter's HTML on demand the first time you open it, then caches it in memory for the rest of the session, instead of shipping all 135 chapters (~8 MB) up front. Each chapter also exists as its own standalone HTML file in this repo — that standalone file *is* what gets fetched, so there's no separate "lazy" copy to keep in sync. Requires a network connection (or the browser's disk cache) to open a chapter you haven't already visited this session — the previous single-file, fully-offline version traded that off for a much smaller initial download; see `git log` if you need that version back.

---

## 📚 What's inside

| # | Chapter | # | Chapter |
|---|---------|---|---------|
| 01 | Introduction & HR | 14 | Behavioural & Self-Intro |
| 02 | Core Java | 15 | Mock Interview — 1000 Questions |
| 03 | Collections | 16 | Unit Testing (JUnit & Mockito) |
| 04 | Java 8 – 21 | 17 | Data Structures & Algorithms |
| 05 | Concurrency & Multithreading | 18 | Design Patterns |
| 06 | JVM & Garbage Collection | 19 | DevOps, Docker & Kubernetes |
| 07 | Spring Core | 20 | Cloud & AWS |
| 08 | Spring Boot | 21 | REST API Design & Documentation |
| 09 | Spring Data JPA & Hibernate | 22 | Messaging & Event Streaming |
| 10 | Spring Security, JWT & OAuth2 | 23 | NoSQL & MongoDB |
| 11 | Microservices | 24 | Git & Version Control |
| 12 | SQL & Database Design | | |
| 13 | System Design | | |

### 🤖 Mastering AI Engineering with Java & Spring AI (chapters 25+, in progress)

Same handbook, continuing the numbering — a book-length series for Java/Spring engineers moving into AI Engineering, organized into six volumes:

| Volume | Focus |
|---|---|
| 1 | AI Foundations — intelligence, ML/DL, transformers, embeddings, prompting, RAG intro |
| 2 | Spring AI — ChatClient, Advisors, memory, streaming, tool calling, MCP, observability |
| 3 | Embeddings & RAG — vector DBs, pgvector, chunking, hybrid search, reranking, evaluation |
| 4 | AI Agents & MCP — planning, reflection, tool use, multi-agent orchestration |
| 5 | Enterprise AI Engineering — security, guardrails, evaluation, cost, scaling, governance |
| 6 | Production Projects — chat platforms, RAG assistants, SQL/coding copilots, multi-agent systems |

Currently published:

| # | Chapter |
|---|---------|
| 25 | What Intelligence Really Means |
| 26 | History of AI |
| 27 | Machine Learning Fundamentals |
| 28 | Neural Networks |
| 29 | Deep Learning |
| 30 | Sequence Models |
| 31 | RNNs |
| 32 | LSTMs |
| 33 | Transformers |
| 34 | Attention |
| 35 | Query, Key, and Value |
| 36 | Multi-Head Attention |
| 37 | Positional Encoding |
| 38 | Decoder Architecture |
| 39 | Tokens |
| 40 | Embeddings |
| 41 | Vector Mathematics |
| 42 | Context Windows |
| 43 | Sampling |
| 44 | Hallucinations |
| 45 | Prompt Engineering |
| 46 | Context Engineering |
| 47 | Fine-Tuning |
| 48 | Reasoning Models |
| 49 | Introduction to RAG |
| 50 | Spring AI Architecture |
| 51 | ChatModel |
| 52 | ChatClient |
| 53 | Prompt |
| 54 | PromptTemplate |
| 55 | Advisors |
| 56 | Memory |
| 57 | Streaming |
| 58 | Structured Output |
| 59 | Tool Calling |
| 60 | Multi-model Support |
| 61 | MCP Integration |
| 62 | Observability |
| 63 | Testing |
| 64 | Performance Optimization |
| 65 | Embedding Models |
| 66 | Chunking |
| 67 | Vector Databases |
| 68 | pgvector |
| 69 | Pinecone |
| 70 | Qdrant |
| 71 | Weaviate |
| 72 | Hybrid Search |
| 73 | Reranking |
| 74 | Metadata Filtering |
| 75 | Retrieval Strategies |
| 76 | Enterprise RAG |
| 77 | Evaluation |
| 78 | Agent Fundamentals |
| 79 | Planning |
| 80 | Reflection |
| 81 | Agent Memory |
| 82 | Tool Usage |
| 83 | Agent Orchestration |
| 84 | Multi-Agent Systems |
| 85 | MCP Deep Dive |
| 86 | Agent Architectures |
| 87 | Enterprise Agents |
| 88 | Security |
| 89 | Guardrails |
| 90 | Prompt Injection |
| 91 | Evaluation at Enterprise Scale |
| 92 | Monitoring |
| 93 | Observability at Scale |
| 94 | Cost Optimization |
| 95 | Scaling |
| 96 | Kubernetes for AI Workloads |
| 97 | Distributed Systems for AI |
| 98 | Governance |
| 99 | Compliance |
| 100 | AI Chat Platform |
| 101 | Enterprise Knowledge Assistant |
| 102 | AI-Powered LMS |
| 103 | Resume Analyzer |
| 104 | SQL Copilot |
| 105 | Coding Assistant |
| 106 | Customer Support AI |
| 107 | Incident Analysis System |
| 108 | Document Intelligence Platform |
| 109 | Multi-Agent Research System |
| 110 | AI Voice Assistant |
| 111 | AI Workflow Automation Platform |

## ✨ Features

- **Single-file reader** — `handbook.html` works offline; just open it in any browser.
- **Dark mode** — toggle in the top bar; preference is remembered and follows your OS theme by default.
- **Mobile-adaptive** — collapsible sidebar and responsive layout.
- **Searchable** — filter chapters and sub-sections instantly.
- **400+ questions** with ROI ratings, frequency, sample answers, code snippets, and revision sheets across the interview chapters.

## 🚀 Usage

Visit the [live site](https://inter-lyart.vercel.app), or serve this folder locally (e.g. `python -m http.server`) and open `handbook.html` through that server. Opening `handbook.html` directly as a `file://` path loads the shell but **not** any chapter content — chapters are fetched with `fetch()`, which browsers block against `file://` origins for security, so a real HTTP server (local or deployed) is required. Regenerate the handbook after adding or editing any chapter with `python _build_index.py`; CI re-checks this on every push.

---

## ⚛️ React / Frontend Interview Handbook

Same format and depth as the Java interview chapters, now **merged into the single combined handbook** as chapters 112–135 (previously a standalone reader under `react/`, which has been folded in and removed). The sidebar shows this track as its own "React & Frontend Interview Handbook" block, positioned right after the Java interview chapters and before the AI Engineering track — chapter numbers are 112–135 rather than contiguous with the Java chapters purely so that existing AI Engineering chapter links (25 onward) never had to change.

| # | Chapter | # | Chapter |
|---|---------|---|---------|
| 112 | Introduction & HR | 124 | Next.js, SSR & Server Components |
| 113 | JavaScript Fundamentals | 125 | Performance Optimization |
| 114 | Advanced JavaScript & Async | 126 | React Internals (Fiber & Reconciliation) |
| 115 | TypeScript for React | 127 | Styling & CSS Architecture |
| 116 | React Fundamentals | 128 | Testing (Jest & RTL) |
| 117 | React Hooks | 129 | Accessibility (a11y) |
| 118 | Advanced Hooks & Custom Hooks | 130 | Browser & Web Platform Fundamentals |
| 119 | Component Patterns | 131 | Frontend Security |
| 120 | State Management | 132 | Build Tools & Tooling |
| 121 | Data Fetching & Server State | 133 | Frontend System Design |
| 122 | Forms & Validation | 134 | Data Structures & Algorithms (JS) |
| 123 | React Router & Navigation | 135 | Behavioural & Self-Introduction |

Regenerate the handbook after editing any chapter (Java, React, or AI Engineering) with `python _build_index.py` — one script, one combined `handbook.html`. CI (`.github/workflows/build-check.yml`) re-runs this on every push and fails the build if it produces a diff, so a forgotten rebuild never reaches `main`.

---

*Built as a personal interview-prep and learning resource. Deployed on [Vercel](https://vercel.com).*
