# Chen-Wei Huang · `Leo`

> Full-stack engineer building multi-agent / LLM systems — with a learning-sciences background.

**Taipei, Taiwan** · NTNU double major: Learning Sciences (primary) + CSIE (secondary) · junior, expected 2027.
**Contact:** `leolove3very@gmail.com` · [github.com/Isaries](https://github.com/Isaries) · Mandarin (native), English.

---

## At a Glance

| | |
|---|---|
| Systems I built, now in production | **3** |
| Aggregate source LOC / automated tests | ~480,000+ / ~13,000+ |
| Largest codebase | AI3L — 99K LOC · 6,759 tests · 205 endpoints |
| Largest multi-contributor work | Normal-OJ — 265 commits in ~3 months |

I work at the intersection of **full-stack engineering, multi-agent / LLM systems, and learning-sciences-grounded product design**.

---

## Featured Projects

### AI3L Community Platform — production full-stack platform
*Commissioned project · founding engineer & technical lead · ~80% of commits · live on Hetzner behind Cloudflare*

A multi-feature academic-exchange platform (forum, Q&A, events, SIGs, albums, DMs, form-builder, social graph, admin suite). **99,604 LOC · 6,759 tests (1.41× test-to-source) · 205 REST endpoints · 57 migrations · 17 locales.**

- **Backend:** FastAPI with 4-layer DDD (endpoint → service → repository → DB), enforced by a written rule table. Parameterized asyncpg SQL throughout.
- **Frontend:** Vue 3 + TypeScript + Vite 6 + Pinia + Tailwind v4 — 53 views, 62 components, TipTap 3 editor.
- **Real-time & data:** WebSocket with ticket-based auth (single-use Redis `GETDEL`) + Pub/Sub fan-out; PostgreSQL 15 (GIN FTS, advisory locks) · Redis 7 · Cloudflare R2 · Celery.
- **Security:** Argon2id (timing-oracle defense) · JWT + Redis JTI denylist · HMAC-bound CSRF · file pipeline (magic-byte → PDF sanitization → OOXML validation → VirusTotal) · GDPR right-to-erasure.
- **Ops:** SUPER_ADMIN-only site backup/export — a distributed-lock-guarded Celery task backing up database + files with structured logging.
- **Deployment:** Cloudflare Tunnel → Nginx → FastAPI on isolated Docker networks. Zero public ports, read-only rootfs, `cap_drop: ALL`.

### SMAP — Smart Multi-Agent Platform
*NSTC Undergraduate Research Project · solo developer, end-to-end · bring-your-own-key, self-hosted*

Self-hosted platform for composing and orchestrating LLM-powered agent groups. **140K+ LOC (82K Python / 58K TS-Vue) · 1,243 backend tests · 11 bounded contexts with layered DDD, cross-context boundaries enforced by `import-linter` + `eslint-plugin-boundaries`.**

- **Workflow engine:** DAG with 11 executor types; a **hand-rolled expression-language interpreter** (no `eval`, AST depth ≤ 16, 5 ms CPU budget) with 16 save-time linter rules (plus 6 advisory warnings). Visual editor on `@vue-flow/core`.
- **Multi-agent orchestration:** per-agent inbox as a Redis Stream, three approval modes with leader fallback, instruction chains with cycle detection, depth-1 sub-agents to prevent fan-out loops.
- **MCP sandbox:** gVisor-isolated ephemeral containers (read-only root, UID ≥ 10000), reachable only via an egress proxy with hostname allowlist + private-IP blocking.
- **Key vault:** envelope-encrypted BYO keys (AES-256-GCM, per-record DEK wrapped by Vault Transit); plaintext keys never returned by any endpoint.
- **RAG & GraphRAG:** Qdrant per project + Neo4j knowledge graph, cross-store consistency via 2-phase commit with compensation.
- **Compliance & self-service:** append-only audit log with streaming CSV export and privileged retention purge; self-service "build-your-own-assistant" studio with custom system prompts, model/key bindings, RAG-lite file grounding, and per-user rate limits.

---

## Other Projects

| Project | Role | One-liner |
|---|---|---|
| **ETF Co-Ownership × Graph Attention Networks** | Capstone · lead contributor | Cross-disciplinary finance-ML research: dual co-ownership networks + twin-branch GAT (~35K params) predicting Taiwan stock returns. Clark–West / Newey–West inference, BH-FDR control. |
| **Math Defense** | Coursework · team lead (~69% commits) | Tower-defense game where math *is* the mechanic; **deterministic C99/WASM scoring core** (level generation, score formula, PRNG) shared bit-exact between frontend and backend, independently replayed and checked server-side within a tight tolerance via `wasmtime-py`; Beta-Bernoulli competency model drives adaptive (ZPD) difficulty recommendation (production evidence is currently success-only); competitive territory/leaderboard mode. |
| **Normal-OJ (NOJ)** | Commissioned · frontend contributor | Production online judge for NTNU CS courses. Authored consolidated PR #14 (81 files, +8.3K/−2.1K); sandbox rule editor; i18n incl. Taiwanese Hokkien (`zh-min-nan`). |
| **TMRP — Tutor Matching and Rating Platform** | Coursework · tech lead (5-person team) | Vue 3 + FastAPI + PostgreSQL marketplace with a three-party (parent↔tutor↔student) rating system (~9K backend LOC, 8 bounded contexts, 243 tests); server-authoritative match state machine as a frozen-dataclass `(status, action)` → transition table, unit-tested independent of the API; partial unique index closes a TOCTOU race that could otherwise double-book matches; 8-layer defense-in-depth middleware (JWT key rotation, double-submit CSRF) + concurrently-refreshed materialized view for the tutor-rating hot path. |
| **Thread Console** | Commissioned · sole dev (~379 commits) | Self-hosted OpenAI Assistants thread manager, in production use. Adaptive polling; AES-Fernet key storage with indexed HMAC for O(1) lookup. |
| **RCSL SQL Client** | Commissioned · sole dev | Secure SQL middleware; **AST-based SQL validation via `sqlglot`** (ACL by walking DB refs, LIMIT injection); SSRF prevention via integer-IP comparison. |
| **ET&S Format Checker** | Commissioned · sole dev | Validates `.docx` journal submissions against 47 APA-7 rules, returns an annotated `.docx` with **native Word comments** (raw OOXML `comments.xml` manipulation via `lxml`). |

---

## Tech Stack

- **Languages:** Python 3.12 · TypeScript 5+ · Vue 3 SFC · SQL · C
- **Backend:** FastAPI · SQLAlchemy 2.0 async · Pydantic v2 · asyncpg · Celery / ARQ · wasmtime-py
- **Frontend:** Vue 3 (Composition API) · Vite · Pinia · Tailwind · TanStack Query · TipTap · KaTeX
- **Data:** PostgreSQL 15/16 (pgvector, FTS, advisory locks) · Redis 7 (Streams, Lua) · Qdrant · Neo4j · MinIO / R2 / S3
- **LLM / ML:** Anthropic SDK · OpenAI · MCP tool servers · custom RAG + GraphRAG · PyTorch Geometric (GAT) · XGBoost · SHAP
- **Infra & security:** Docker (read-only rootfs, `cap_drop: ALL`) · gVisor sandboxing · Nginx · Cloudflare (Tunnel/R2/WAF) · HashiCorp Vault · Argon2id · JWT + JTI denylist
- **Quality:** pytest · Vitest · Playwright · MSW · `import-linter` DDD boundaries · type-coverage ≥ 95% · OpenAPI drift detection
- **Learning sciences:** cognitive load (Sweller) · productive failure (Kapur) · retrieval practice · stealth assessment (Shute) · self-determination theory

---

## Research & Professional Experience

| Period | Role · Organization |
|---|---|
| **2026-04 – 2026-06** | Developer, Programmatic Formatting Checker for *ET&S* Journal |
| **2026-03 – 2026-05** | Developer, Customized Forum — Prof. Yu-Ju Lan, NTNU |
| **2026-03** | Lead Instructor, "AI Teaching Agent Design" — 2-day workshop, ~70 K-12 teachers, NCHU |
| **2025-07 – 2026-06** | Research Assistant, MOE Higher Education Sprout Project · NTNU (Prof. Nian-Shing Chen) — NLP · MCP · workflow automation |
| **2025-02 – 2025-06** | Research Assistant, NSTC Industry-Academic Plan · NTNU (Prof. Nian-Shing Chen) — NLP · HCI · AI Agent & IoT |
| **2024-04 – 2024-06** | Programming Instructor · Fuhe Junior High School (Python) |

---

## What I'm Looking For

An internship on a non-trivial system with real users — ideally AI/agent infrastructure, distributed systems, developer tools, or AI-for-education, though I'm open and learn fast. What I most want is **code review from more experienced engineers**; my biggest gap is multi-engineer collaboration at scale. Available ~1.5 years until graduation — open to year-long or summer programs.

---

*Last updated: 2026-07-05. Project metrics verified against source repositories.*
