# Chen-Wei Huang · `Leo`

> Full-stack engineer · multi-agent / LLM systems · learning-sciences-informed product design.

**Taipei, Taiwan** · NTNU double major: Learning Sciences (primary) + Computer Science and Information Engineering (secondary) · junior · expected graduation 2027.
**Contact:** `leolove3very@gmail.com` · `github.com/Isaries` · Mandarin (native), English.

---

## Overview

Junior at NTNU, double-majoring in Learning Sciences and CSIE — a dual training I'm still learning to use as one toolset rather than two. My work sits at the intersection of full-stack engineering, multi-agent / LLM systems, and learning-sciences-grounded product design. Three of the systems I've built are currently in real use.

---

## At a Glance

| | |
|---|---|
| Systems I built, now in production | 3 |
| Projects detailed below | 9 |
| Aggregate source LOC | ~400,000+ |
| Aggregate automated tests | ~12,500+ |
| Largest codebase | AI3L — 99K LOC, 6,759 tests, 205 endpoints |
| Largest multi-contributor work | Normal-OJ — 265 commits in ~3 months |

---

## Tech Stack

**Languages:** Python 3.12 · TypeScript 5+ · Vue 3 SFC · SQL (hand-written, parameterized) · C · Shell / PowerShell.

**Backend:** FastAPI · Flask · Uvicorn / Gunicorn · ARQ · Celery · Huey · SQLAlchemy 2.0 async · Alembic · Pydantic v2 · asyncpg · psycopg2 · HTTPX · wasmtime-py.

**Frontend:** Vue 3 (Composition API) · TypeScript strict · Vite · Pinia · Vue Router · Tailwind CSS · DaisyUI · TanStack Vue Query · TipTap · KaTeX · Mermaid · ECharts · vue-i18n.

**Data layer:** PostgreSQL 15/16 (pgvector, GIN FTS, partial indexes, advisory locks) · Redis 7 (Streams, Pub/Sub, Lua atomic scripts, JTI denylist) · Qdrant · Neo4j · MinIO / Cloudflare R2 / S3 · SQLite.

**LLM / AI:** Anthropic SDK · OpenAI Assistants API · Voyage / Cohere / Gemini · MCP tool servers · custom RAG + GraphRAG pipelines · hand-rolled expression-language interpreter for workflow DSL (no `eval`).

**ML / statistics:** PyTorch · PyTorch Geometric (Graph Attention Networks) · scikit-learn · XGBoost · statsmodels · SHAP.

**Infrastructure & DevOps:** Docker · Docker Compose (multi-stage, multi-network, read-only rootfs, `cap_drop: ALL`) · gVisor (`runsc`) for untrusted-code sandboxing · Nginx · Cloudflare (Tunnel, R2, CDN, WAF) · Hetzner Cloud · HashiCorp Vault (Transit + KV + AppRole, envelope encryption).

**Security implementations:** Argon2id + timing-oracle hardening · JWT + Redis JTI denylist · CSRF double-submit (HMAC-bound) · WebSocket ticket auth · dual-layer rate limiting (Nginx + Redis Lua) · magic-byte MIME validation · PDF sanitization (`pikepdf`) · OOXML structural validation · AST-based SQL injection prevention (`sqlglot`) · SSRF allow-listing via integer-IP comparison · gVisor MCP sandbox with egress proxy · GDPR right-to-erasure.

**Testing & quality gates:** pytest · pytest-asyncio · Vitest · Vue Test Utils · Playwright · MSW · `import-linter` for DDD boundary enforcement · `eslint-plugin-boundaries` · type-coverage ≥ 95% · OpenAPI drift detection · pip-audit · npm audit · gitleaks · custom CI linters.

**Observability:** Loguru (structured JSON) · Sentry · Datadog `ddtrace` · OpenTelemetry · Prometheus · Grafana · Loki + Promtail.

**Documentation:** C4 model · Mermaid diagrams · OpenAPI / JSON Schema · APA-7 academic citation.

**Learning sciences & educational theory:** Cognitive load (Sweller) · productive failure (Kapur) · retrieval practice (Roediger & Karpicke) · ZPD (Vygotsky) · multimedia learning (Mayer) · self-determination theory (Ryan & Deci) · stealth assessment (Shute) · cognitive apprenticeship (Collins, Brown & Newman) · formative assessment (Hattie & Timperley) · MDA framework.

---

## Featured Projects

### 1. AI3L Community Platform — production full-stack platform (Commissioned Project; founding engineer & technical lead; 80% of commits)

> Live on Hetzner Cloud behind Cloudflare. 99,604 source LOC, 6,759 automated tests (1.41× test-to-source ratio), 205 REST endpoints, 57 Alembic migrations, 17 locales.

A multi-feature academic-exchange platform — forum, Q&A, events, SIGs, albums, direct messaging, form-builder, social graph, admin suite — for the AI in Language Learning & Literacy community.

**Architecture:**
- **Backend:** FastAPI with 4-layer DDD (endpoint → service → repository → DB) enforced by a written rule table. 28 endpoint modules, 31 services, 32 repositories (parameterized asyncpg SQL), 15 converters.
- **Frontend:** Vue 3 + TypeScript + Vite 6 + Pinia + Tailwind v4. 53 views, 62 components, 22 typed API modules, 18 composables. TipTap 3 rich-text editor.
- **Data plane:** PostgreSQL 15 (GIN FTS, advisory locks for form-quota races) · Redis 7 (14 keyspaces) · Cloudflare R2 · Celery + Beat (15 scheduled jobs).
- **Real-time:** WebSocket with ticket-based auth (single-use Redis key via `GETDEL`) and Redis Pub/Sub fan-out — no sticky sessions required.
- **Deployment:** Cloudflare Tunnel → Nginx → FastAPI on isolated Docker networks. Zero public ports. Read-only rootfs, `cap_drop: ALL`.
- **Documentation:** ~1,050-line architecture doc (C4 levels 1–3, ER diagrams for 13 bounded contexts, Redis namespace topology, request-lifecycle sequence diagrams), auto-synced via GitHub Action.

**Security:** Argon2id with timing-oracle defense · JWT + Redis JTI denylist · CSRF bound to JTI via HMAC · file pipeline (magic-byte MIME → PDF sanitization → OOXML validation → VirusTotal async scan) · dual-layer rate limiting · GDPR right-to-erasure.

**Process:** 40 dated audit reports producing 300+ documented findings. 4 CI workflows including integration tests against live PostgreSQL + Redis.

---

### 2. SMAP — Smart Multi-Agent Platform (NSTC Undergraduate Research Project; solo developer, end-to-end)

> Self-hosted platform for composing and orchestrating LLM-powered agent groups. Bring-Your-Own-Key model: no SaaS tier, no platform billing.

**Architecture:** 60K+ LOC (43K Python · 17K TypeScript / Vue), 10 bounded contexts with layered DDD, cross-context calls enforced by `import-linter` and `eslint-plugin-boundaries`. Spec-first: 1,500-line SRS with every requirement tagged and traced to commits/tests.

**Subsystems:**
- **Key vault:** 5 LLM + 4 search providers with envelope-encrypted (AES-256-GCM, per-record DEK wrapped by Vault Transit) BYO keys. Sliding-window quotas, automatic rotation. Plaintext keys never returned by any endpoint.
- **Workflow engine:** DAG with 11 executor types and 5 trigger kinds. Custom expression language — hand-rolled interpreter (no `eval`, AST depth ≤ 16, 5 ms CPU budget). 14 linter rules enforced on save. Visual editor on `@vue-flow/core`.
- **Multi-agent orchestration:** Per-agent inbox as Redis Stream. Three approval modes with leader fallback. Instruction chains with cycle detection (depth ≤ 5). Sub-agents depth-1 only to prevent fan-out loops.
- **MCP sandbox:** gVisor-isolated ephemeral containers (read-only root, UID ≥ 10000). Reachable only through an egress proxy with hostname allowlist, private-IP blocking, and `Authorization` header stripping.
- **RAG & GraphRAG:** Qdrant per project + Neo4j knowledge graph. Cross-store consistency via 2-phase commit with compensation and retry/rollback.

**Security:** RS256 JWT with signing key in Vault Transit (never on disk), `kid`-based rotation. NFKC normalization pre-Argon2. Append-only audit at DB-trigger level. Three isolated Docker networks.

**CI & delivery:** 12 separation-of-concerns gates (slice imports, bundle budgets, type coverage ≥ 95%, OpenAPI drift detection). Ten construction phases (A → J) closed sequentially. 27 Alembic migrations · 35 backend test files · 48 frontend integration · 8 Playwright E2E specs.

---

### 3. ETF Co-Ownership Networks & Graph Attention Networks (Capstone Project; lead contributor)

> *When Do ETF Co-Ownership Networks Predict Returns? Cross-Sectional Evidence from Taiwan with Ridge, XGBoost, and Graph Attention Networks.* Cross-disciplinary capstone research at NTNU, 2025–2026, 3-person team — in progress; results not yet finalized.

Within the 3-person team, my work covers the theoretical framework, econometric design, model architecture, and the data pipeline.

**Research question:** Under what conditions, if at all, do debiased ETF co-ownership network features improve out-of-sample stock-return predictions beyond standard controls?

**Methods:**
- **Dual-network framework** — one network from ETF holdings (institutional co-ownership), one from factor-residualized price co-movement. Active-weight construction (Grinold & Kahn 1999) and six-factor residualization (FF5 + MOM + SOX) debias each network.
- **Three model classes on identical features** — Ridge (primary), XGBoost (nonlinear benchmark with SHAP), and a twin-branch Graph Attention Network (~35K params, 4-head attention, semi-supervised on ~900-node graph).
- **Five hypotheses (P1–P5)** spanning the two networks; P3 includes a cross-industry falsification test (permutation on ΔR²).

**Inference:** Clark & West MSFE-adjusted statistic as the primary test, cross-checked against Newey-West HAC and double-clustered standard errors so conclusions don't hinge on a single specification. BH-FDR control across 8 primary tests.

**Engineering:** 43 Python scripts across 20 pipeline stages (9 analysis + 5 optimization + 6 data collection). Async Playwright scraper of TWSE MOPS for quarterly ETF holdings (~120 months back to 2004). ~72,900 KSG transfer-entropy estimates.

---

## Other Projects

### 4. Math Defense — NTNU CSIE Computer Programming II (Coursework Project; team lead, 66% of commits)

> 4-person team · ~7 weeks active development · 262 commits.

A tower-defense game where math is the mechanic, not a quiz gate: 7 tower types each implement a real math topic (polynomial/trig/log curves, radian-arc sector, vector dot-product, limits, derivatives, chain rule, Monty Hall probability). Game-design decisions grounded in learning-sciences theory.

- **WASM anti-cheat kernel** — C99 + Emscripten with deterministic build flags so floating-point operations produce byte-identical output across hosts. Same `.wasm` runs server-side via `wasmtime-py` to recompute and verify scores.
- **DDD backend** — 13 bounded contexts, 18 application services, repository protocols (not inheritance). Architecture enforced by 5 custom CI linters.
- **700-line design audit** citing ~60 APA-7 sources, mapping mechanics to theoretical commitments. 27 of 28 items shipped.
- **Bayesian stealth assessment** — Q-matrix → Beta-Bernoulli posteriors → recommender → teacher dashboard. RCT infrastructure with deterministic group assignment + pre/post/delayed-transfer probes.
- **Accessibility** — unique Unicode glyph per tower (WCAG 1.4.1), ARIA live regions, full keyboard placement, `prefers-reduced-motion` respected across all renderers.

**Stack:** Vue 3 + TypeScript + Vite · FastAPI + PostgreSQL 16 · C99 + Emscripten + `wasmtime-py` · ~331 pytest + 72 Vitest files.

---

### 5. Normal-OJ (NOJ) — NTNU CSIE production online judge (Commissioned Project; frontend-team contributor)

> 265 commits · 2025-10 – 2025-12 (~3 months)

Open-source online judge used by NTNU's CS department for programming courses.

- Principal author of consolidated PR #14: 81 files, +8,347 / −2,102 lines.
- Sandbox rule editor UI for per-problem network access, library imports, file-extension filter, sidecar containers.
- Internationalization across 3 locales including Taiwanese Hokkien (`zh-min-nan`), a low-resource language.
- Working in a large existing TypeScript/Vue codebase under live classroom usage, with Sentry session replay, Playwright CI, and multi-person review.

---

### 6. TMRP — Tutor Matching Platform (Coursework Project; tech lead, 5-person tutor-matching platform)

University SQL-course group project built as a tutor-matching marketplace. Vue 3 SPA + FastAPI + PostgreSQL 16 + Huey, Dockerized.

- 8 bounded contexts; server-authoritative match state machine as frozen-dataclass transition table — every (status, action) pair testable without DB or framework.
- Partial unique index defeats duplicate-active-match races at the DB level; conversation pair-ordering enforced via `CHECK (user_a < user_b)`.
- Async router guard round-trips to HttpOnly-cookie-gated `/api/auth/me` to prevent client-side role tampering. Custom Vite prebuild fails on `v-html` / `innerHTML`.
- 18 pytest files including SQL-injection regression and state-machine transition suites against real Postgres. ~165 KB design documentation.

---

### 7. Thread Console — OpenAI threads management platform (Commissioned Project; sole developer, ~379 commits)

Self-hosted platform for organizing, searching, and exporting OpenAI Assistants API threads. In production use by a research team.

- Adaptive polling classifying threads as normal / low / frozen to reduce API consumption on dormant projects.
- AES-Fernet encryption of stored API keys with indexed HMAC-SHA256 for O(1) bearer-token lookup. Legacy-plaintext auto-migration.
- CSP with per-request nonces; `has_request_context()` guards for background workers.
- 117 backend tests; conventional commits throughout; 6 Dependabot security PRs landed.

---

### 8. RCSL SQL Client — secure SQL middleware (Commissioned Project; sole developer)

Web SQL client wrapping a research lab's MySQL HTTP API. Currently the production access path for the lab's databases.

- AST-based SQL validation via `sqlglot` — ACL boundaries enforced by walking database references; LIMIT clauses injected via AST. Smart DB-context injection with CTE forward-references correctly excluded.
- SSRF prevention via integer-IP comparison across private ranges, with a configured bypass for the Docker-internal endpoint.
- Frontend inline-cell escaping ordered to defeat MySQL-default-mode escape sequences.
- Vanilla ES6 modules, CodeMirror 5 with live-schema-driven autocomplete, `AbortController` query cancellation.

---

### 9. ET&S Format Checker — academic-journal copyediting tool (Commissioned Project; sole developer)

Web tool that validates `.docx` submissions against *Educational Technology & Society* journal's APA 7th formatting rules (47 rules, 9 categories) and returns a structured report plus an annotated `.docx` with native Word comments.

- OOXML manipulation — appends native Word comments by writing `word/comments.xml`, injecting range markers via `lxml`, creating the `CommentReference` style when absent.
- Unicode-correct multilingual NLP — CJK Unicode blocks + Latin diacritics + curated European surname particle table for correct name parsing. Damerau-Levenshtein typo tolerance with year-distance heuristics.
- Async DOI/URL liveness — bounded-concurrency `httpx` with HEAD→GET fallback, exponential backoff with jitter, scheme allowlist rejecting `file://` / `ftp://`.
- 47 rules · 14 test modules · 5 real manuscripts as regression ground truth · multi-stage Docker · ruff + mypy strict.

---

## Research & Professional Experience

| Period | Role · Organization |
|---|---|
| **2026-04 – 2026-06** | Development of a Programmatic Formatting Checker for ET&S Journal (Project #9). |
| **2026-03 – 2026-05** | Development of a Customized Forum (lab community variant of Project #1) by Prof. Yu-Ju Lan, NTNU. |
| **2026-03 – 2026-03** | Lead Instructor, "AI Teaching Agent Design" (2-day workshop for ~70 K-12 teachers across 10 subjects, NCHU) |
| **2025-07 – 2026-06** | Research Assistant, MOE Higher Education Sprout Project · NTNU (Prof. Nian-Shing Chen's team). NLP · MCP function development · Workflow automation · HCI. |
| **2025-02 – 2025-06** | Research Assistant, NSTC Industry-Academic Cooperation Plan · NTNU (Prof. Nian-Shing Chen's team). NLP · HCI · AI Agent & IoT. |
| **2024-04 – 2024-06** | Programming Course Instructor · Fuhe Junior High School, New Taipei City (Python). |
| **2023-10 – 2024-01** | MOE Digital Learning Partner (Tutor) · NTNU. Math and science tutoring. |
| **2023-07 – 2023-08** | Assembly-line Worker · Wistron NeWeb Corporation. |

---

## What I Am Looking For

An internship where I can work on a non-trivial system with real users, ideally touching AI/agent infrastructure, distributed systems, developer tools, or AI-for-education — but I am open and learn quickly. What I most want is code review from people more experienced than me; my biggest gap is multi-engineer collaboration at scale.

Available ~1.5 years until graduation — open to year-long or summer programs.

---

*Last updated: 2026-05-18. Project metrics verified against source repositories.*
