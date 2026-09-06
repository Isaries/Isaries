# Hi, I'm Leo (Chen-Wei Huang)

**Software engineer and applied researcher. I solve problems that sit between education and infrastructure — and I solve them all the way down.**

Every project I've built started with a concrete problem someone needed fixed: a production server holding students' data with no version control and a backup that had been silently failing for months. An AI tutor whose instructions a student could rewrite from the browser console. A research corpus trapped inside an API with no search. I don't stop at making things work — I care about making them hold up: tested, secure, and maintainable enough that someone else can operate them after I leave.

That approach has taken me from learning sciences into full-stack engineering, security auditing, systems operations, and research. I've carried these as concurrent workstreams — shipping production code, authoring a conference paper, teaching workshops, and operating a live classroom platform in the same month.

Taipei, Taiwan · NTNU, double major in [Learning Sciences](https://www.upls.ntnu.edu.tw/) (cognitive science and HCI applied to how people learn) + Computer Science · Senior, graduating 2027  
GPA 4.00 · Class rank #2 (top 15%) · Dean's List · NTNU Programming Contest top distinction (x2)  
[cw.huang.work@gmail.com](mailto:cw.huang.work@gmail.com) · Mandarin (native) · English

---

## Highlights

- **9 security patches merged upstream** into UC Berkeley's [WISE](https://github.com/WISE-Community) platform, shipped in three releases used by institutions worldwide
- **Published researcher**: accepted paper at ICCE 2026 (first author); journal manuscript in preparation for *Language Learning & Technology*
- **Multiple production systems** built and operated, serving live classrooms and active research groups — routinely managing concurrent workstreams across engineering, research deadlines, and teaching
- **Instructor & TA**: AI workshops across 3 institutions for ~100 teachers; TA for SQL & Database Design
- **7 consecutive RA appointments** since 2023-09, under 4 PIs, funded by NSTC, MOE, and MOST

---

## Awards

- **Dean's List** (書卷獎), NTNU, 2026
- **STAR Scholarship**, NTNU, 2026
- **NTNU Programming Contest**, 特優 (top distinction), 2024 (x2)
- **五育獎學金** (Holistic Development Scholarship), NTNU, 2024
- **Academia Sinica Statistics Camp**, 2025

---

## Featured Work

### TWISE — Production Platform Operations & Security
*Sole operator and developer for NTNU's deployment of UC Berkeley's WISE science-learning platform, serving live secondary-school classes. (Private repos under [WISE-NTNU-Community](https://github.com/WISE-NTNU-Community))*

The platform serving real classrooms had no version control, a backup that had been silently failing for three and a half months, and no way to ship a code change to production. The database held minors' personal data under Taiwan's privacy law. In 41 active days: migrated 15 repositories, built 3 CI/CD pipelines, conducted a security audit (20 findings), and built an administration dashboard from scratch with 953 backend and 446 frontend tests. Authored 9 upstream PRs that Berkeley's maintainers reviewed and merged, including fixes for privilege escalation ([#322](https://github.com/WISE-Community/WISE-API/pull/322)), password-reset IDOR ([#325](https://github.com/WISE-Community/WISE-API/pull/325)), any-teacher password overwrite ([#332](https://github.com/WISE-Community/WISE-API/pull/332)), and brute-force throttling ([#324](https://github.com/WISE-Community/WISE-API/pull/324)). 3 additional PRs remain open upstream.

**Stack:** Java · Spring Boot · Angular · FastAPI · Next.js · PostgreSQL · MySQL · Docker · GitHub Actions

### [SMAP](https://github.com/Research-Center-for-Smart-Learning-RCSL/Smart-MultiAgent-Platform) — Multi-Agent LLM Platform
*NSTC-funded undergraduate research project. Sole developer.*

A research group needed to define LLM agents, compose them into workflows, ground them in documents, give them sandboxed tools, and audit everything — without writing code. Built the platform end to end: 14 domain modules, 364 REST endpoints, 8 WebSocket channels, 8,400+ backend tests, 1,800+ frontend tests. Includes a visual workflow editor with a hand-written expression language, gVisor-sandboxed tool execution, envelope-encrypted BYO API keys, and RAG + GraphRAG with cross-store consistency.

**Stack:** Python · FastAPI · TypeScript · Vue 3 · PostgreSQL · Redis · Qdrant · Neo4j · Docker · gVisor

### [AI Nexus](https://github.com/Research-Center-for-Smart-Learning-RCSL/RCSL-AI-Nexus) — Self-Hosted LLM Gateway
*Sole developer. In production on a Mac Studio after the lab needed shared AI infrastructure without giving every project its own API keys and model configs.*

LLM inference gateway with an OpenAI-compatible API, a management control plane, multi-runtime support (Ollama, MLX, vLLM), key management, spend controls, and a 15-check health monitoring system with alerting. 91 endpoints, ~1,500 tests, 12 Compose services. Two external integrators are running agent clients against it. Recent additions include a Rust/PyO3 native tokenizer that parses GGUF model files directly for token counting and chat-template rendering, and a structured model-evaluation harness with multi-seed rotation and quantization-matched comparisons for production model selection.

**Stack:** Python · Rust (PyO3) · FastAPI · TypeScript · React · PostgreSQL · Docker · launchd

---

## Other Projects

| Project | What it does |
|---|---|
| [**AI3L**](https://github.com/ISW-stack/AI3L-Community) | Academic-exchange platform (forum, Q&A, events, DMs, admin suite). 205 endpoints, 6,759 tests, 17 locales |
| **Hybrid Copyediting System** | Validates `.docx` manuscripts against 47 APA-7 rules for an SSCI journal; outputs annotated Word comments via raw OOXML |
| **Fishbone Cave** | Multi-device classroom activity platform — contributed the room server, security model, and 125 tests to a colleague's repo in 4 days |
| [**Math Defense**](https://github.com/2026-NTNU-Computer-Programming-II-POLS/Math-Defense) | Tower-defense game with a deterministic C99/WASM scoring kernel replayed server-side for anti-cheat. 3-person team, architecture lead |
| **ETF Co-Ownership × GAT** | Capstone: dual co-ownership networks + Graph Attention Networks predicting Taiwan stock returns. Ridge/XGBoost baselines, Clark-West inference |
| [**NOJ**](https://github.com/2025-NTNU-Software-Engineering-Team-1/new-front-end-2025Team1) | Production online judge for NTNU CS courses. Consolidated PR #14 (81 files), sandbox rule editor, i18n |
| **Thread Console** | Self-hosted OpenAI Assistants thread manager with encrypted credentials, adaptive sync, and batch export |
| **SQL Client** | SQL middleware with AST-based query validation, database-scope ACL, and SSRF prevention |

---

## Collaboration

- **WISE upstream**: authored 9 PRs that Berkeley's maintainers reviewed and merged across two repositories; coordinated responsible disclosure after verifying no private reporting channel existed
- **Fishbone Cave**: contributed the entire backend to a colleague's repository, working within their project structure and coordinating feature boundaries across a four-day sprint
- **NOJ**: contributed to a multi-developer production codebase — consolidated PR across 81 files, sandbox policy editor, and i18n including Taiwanese Hokkien

---

## Research & Publications

**First author** · "Generative AI as a Socratic Tutor in Robot-Assisted Language Learning" — *ICCE 2026* (accepted)  
Quasi-experimental study with 32 EFL learners on a robot-and-tablet platform; found a Socratic agent's usability deficit lands on Ease of Use (*p* = .012) but not Ease of Learning — a distinction a composite score cannot make.

**First & corresponding author** · "Three LLM-Driven AI Agents for EFL Grammar Learning" — journal manuscript in preparation  
Reports task compression: under fixed time-on-task, three agent conditions diverged sharply in practice volume (eta-squared = .360) while producing no detectable difference in learning outcomes.

<details>
<summary><strong>Research experience</strong> (7 consecutive appointments since 2023-09)</summary>

| Period | Role |
|---|---|
| 2026-07 – 2027-02 | **NSTC Undergraduate Research Project** — sole developer of SMAP (Prof. Nian-Shing Chen) |
| 2026-07 – present | Platform engineer & operator, TWISE (Prof. Hsin-Yi Chang) |
| 2025-07 – 2026-06 | RA, MOE Higher Education Sprout Project (Prof. Nian-Shing Chen) — NLP, MCP, workflow automation |
| 2025-02 – 2025-06 | RA, NSTC Industry-Academic Plan (Prof. Nian-Shing Chen) — NLP, HCI, AI agents |
| 2023-09 – 2024 | RA, ICILS 2023 Taiwan execution team (Prof. Cheng-Chih Wu, former NTNU president) |

</details>

---

<details>
<summary><strong>Teaching & Mentoring</strong></summary>

| When | What |
|---|---|
| 2026-09 | **Teaching assistant** — SQL & Database Design, NTNU |
| 2026-03 | **Course designer & instructor** — AI + Chinese language teaching game development, 30 grad students, NTNU |
| 2026-01 – 03 | **Lead instructor** — AI teaching-agent workshops across 3 institutions (~100 K-12 teachers and grad students) |
| 2024 | **Programming instructor** — Python, Fuhe Junior High School |
| 2023 – 2024 | **Digital tutor** — MOE Digital Companion program |

</details>

---

## Tech Stack

**Languages:** Python · TypeScript · Rust · SQL · C · Java  
**Backend:** FastAPI · Flask · Spring Boot · SQLAlchemy · Pydantic · Celery  
**Frontend:** Vue 3 · React · Next.js · Angular · Tailwind · Vite  
**Data:** PostgreSQL · MySQL · Redis · Qdrant · Neo4j · SQLite  
**AI/ML:** OpenAI · Anthropic · MCP · RAG · GraphRAG · PyTorch Geometric · XGBoost  
**Infra:** Docker · gVisor · Nginx · Cloudflare · GitHub Actions · Bash

---

## What I'm Looking For

An internship where I can work on a production system with real users alongside more experienced engineers — ideally in AI infrastructure, developer tools, distributed systems, or applied research. I've led small teams, contributed to other people's codebases, and coordinated with upstream maintainers, but most of my work has been in university labs. I want to find out what production engineering looks like at a larger scale — with deeper code review, shared ownership, and problems I haven't seen before. Flexible year-round on a part-time basis; available for full-time during breaks through graduation in 2027.

Reach me at [cw.huang.work@gmail.com](mailto:cw.huang.work@gmail.com) — happy to chat about any of the work above.

---

*Last updated: 2026-09-06*
