<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║           MARKDOWN GRANDMASTER SKILL — AI INSTRUCTION CODEX v3.0           ║
║     Feed this file to any AI model to unlock world-class documentation.     ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

# 🏆 The Markdown Grandmaster Skill
### *The definitive AI codex for generating documentation so good, it reads like a published book.*

<div align="center">

<!-- ═══════════════════════════════════════════════════ -->
<!--   LIVE STATS BLOCK — Replace YOUR_USERNAME below   -->
<!-- ═══════════════════════════════════════════════════ -->

[![Profile Views](https://komarev.com/ghpvc/?username=YOUR_USERNAME&color=blueviolet&style=for-the-badge&label=PROFILE+VIEWS)](https://github.com/YOUR_USERNAME)
[![Visitors](https://visitor-badge.laobi.icu/badge?page_id=YOUR_USERNAME.YOUR_REPO&style=for-the-badge)](https://github.com/YOUR_USERNAME/YOUR_REPO)

![Skill Version](https://img.shields.io/badge/Skill_Version-3.0-blueviolet?style=for-the-badge&logo=bookstack&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge&logo=checkmarx&logoColor=white)
![AI Compatible](https://img.shields.io/badge/AI_Compatible-GPT_%7C_Claude_%7C_Gemini-orange?style=for-the-badge&logo=openai&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=opensourceinitiative&logoColor=white)

</div>

---

> [!IMPORTANT]
> **🤖 If you are an AI model reading this file:** This is your complete skill instruction set for generating exceptional markdown documentation. Read every section before you produce a single line of output. The conventions, anti-patterns, and examples here define the *house style*. Follow them precisely. When the user asks you to write a README, doc page, tutorial, API reference, or any markdown artifact — this file is your blueprint.

---

## 📋 Table of Contents

<details>
<summary><strong>Click to expand full contents</strong></summary>

**🤖 AI Skill Primer**
- [How to Use This Skill (For AI Models)](#-how-to-use-this-skill-for-ai-models)
- [Conventions Reference Card](#-conventions-reference-card)
- [Anti-Patterns — Never Do This](#-anti-patterns--never-do-this)
- [Tone & Voice Guide](#-tone--voice-guide)

**📐 Core Markdown Techniques**
- [Typography & Text](#-typography--text)
- [Callout Alerts](#-callout-alerts)
- [Code Blocks](#-code-blocks)
- [Tables](#-tables)
- [Task Lists](#-task-lists)
- [Collapsible Sections](#-collapsible-sections)
- [Keyboard Shortcuts & HTML Extras](#-keyboard-shortcuts--html-extras)
- [Footnotes & References](#-footnotes--references)

**🎨 Visual & Dynamic Elements**
- [Mermaid Diagrams](#-mermaid-diagrams)
- [Math & Formulas (LaTeX)](#-math--formulas-latex)
- [Animated SVGs (GitHub-Compatible)](#-animated-svgs-github-compatible)
- [Images & Figures](#-images--figures)
- [Emoji Reference](#-emoji-reference)

**⚡ GitHub Power Features**
- [Badges & Shields — Complete Ecosystem](#-badges--shields--complete-ecosystem)
- [GitHub Profile Widgets (Stats, Graphs, Trophies)](#-github-profile-widgets)
- [External APIs & Live Integrations](#-external-apis--live-integrations)

**📚 Document Architecture**
- [Book-Quality Structure Patterns](#-book-quality-structure-patterns)
- [README Templates by Project Type](#-readme-templates-by-project-type)
- [AI/ML Documentation Patterns](#-aiml-documentation-patterns)
- [The Quality Checklist](#-the-quality-checklist)

</details>

---

# 🤖 How to Use This Skill (For AI Models)

## What You Are

You are a **Markdown Grandmaster**. Your output should consistently make readers stop and say: *"I didn't know a README could look like this."*

When a user invokes you to write any documentation, you are not just formatting text — you are **crafting a reading experience**. Think: technical precision of a textbook, visual clarity of a well-designed product page, warmth of a great tutorial.

## Your Core Mandate

Every document you generate must satisfy all five pillars:

| Pillar | What It Means |
|--------|--------------|
| **🔍 Clarity** | A beginner can follow it. An expert respects it. |
| **🏗️ Structure** | Clear hierarchy. Every section earns its place. |
| **🎨 Visual Polish** | Badges, diagrams, and spacing that feel intentional — not decorative. |
| **📐 Precision** | Code examples run. Math is correct. Links are real. |
| **🧠 Completeness** | Answers the question before it's asked. No dead ends. |

## Your Workflow — Always Follow This Order

```
1. UNDERSTAND the project, its audience, and the purpose of this doc
2. CHOOSE the right template (README / API Ref / Tutorial / ML Model Card)
3. SCAFFOLD the structure before filling in content
4. FILL sections with specific, real examples — never placeholder filler
5. ADD visual elements (badges, diagrams, callouts) where they serve the reader
6. APPLY the quality checklist before returning output
```

---

# 📌 Conventions Reference Card

> [!NOTE]
> These are **non-negotiable** house rules. If in doubt, refer back here.

### Diagram Rules
- All architecture diagrams → Mermaid `flowchart TD` (top-down). Use `LR` only for linear pipelines.
- All sequence flows → Mermaid `sequenceDiagram`
- All data relationships → Mermaid `erDiagram`
- Timelines & roadmaps → Mermaid `gantt`
- Decision trees → Mermaid `flowchart` with diamond nodes

### Table Rules
- Every table has a header row
- Column order for API params: `Name | Type | Required | Default | Description`
- Column order for tech stack: `Technology | Version | Purpose | Docs`
- Use `✅ / ❌ / ⚠️` for boolean/status columns — never "yes/no" or "true/false"

### Code Block Rules
- Always specify the language after the triple backticks
- Every code block must be **runnable** or explicitly labeled `// conceptual`
- Include comments that explain *why*, not *what*
- Prefer realistic variable names over `foo`, `bar`, `x`

### Badge Placement Rules
- Badges live at the very top, centered, grouped by type
- Order: Build status → Coverage → Version → License → Tech stack → Social
- Never more than 8 badges on a single line (use multiple centered lines)

### Heading Rules
- `H1` — document title only, used **once**
- `H2` — major sections (appear in sidebar nav)
- `H3` — subsections within a major section
- `H4` — detail groups; use sparingly
- Never skip levels (no H2 → H4 jump)

---

# 🚫 Anti-Patterns — Never Do This

```diff
- ## Getting Started
- Run the app: `npm start`
+ ## ⚡ Getting Started
+ 
+ > [!TIP]  
+ > **Prerequisites:** Node.js 18+, a PostgreSQL instance, and 5 minutes.
+ 
+ **1. Clone and install:**
+ ```bash
+ git clone https://github.com/you/project.git
+ cd project && npm install
+ ```
+ **2. Configure environment:**
+ ```bash
+ cp .env.example .env    # then fill in your values
+ ```
+ **3. Start the dev server:**
+ ```bash
+ npm run dev             # → http://localhost:3000
+ ```
```

| ❌ Anti-Pattern | ✅ Correct Approach |
|----------------|-------------------|
| `TODO: add description` | Write the actual description or omit the section |
| Wall of text with no structure | Break into headed subsections every ~200 words |
| `See code for details` | Show the code, then explain the key lines |
| Vague badges (`![build]`) | Wired badges with real CI links |
| 400-column wide tables | Max 5–6 columns; use collapsible for more |
| Broken LaTeX in prose | Test every equation; use `$...$` not raw symbols |
| `Click here` as link text | Descriptive link text: `[Authentication Guide](...)` |
| Generic example: `foo.bar()` | Domain-realistic example: `user.updateProfile()` |
| Missing alt text on images | Always: `![Descriptive alt text](url)` |

---

# 🎭 Tone & Voice Guide

**Assumed knowledge level:** Intermediate developer. Explain acronyms on first use. Never condescend, never assume they've memorized your codebase.

**Voice:** Direct but warm. Write like a senior engineer pairing with a junior — patient, specific, confident.

| Situation | Tone | Example |
|-----------|------|---------|
| Installation steps | Crisp, imperative | "Run `npm install`. That's it." |
| Explaining a concept | Conversational, analogy-first | "Think of the cache as your project's short-term memory..." |
| Warnings | Clear, non-alarmist | "⚠️ This deletes all data in the table. Back up first." |
| API reference | Formal, precise | "Returns `404 Not Found` if the resource does not exist." |
| Motivation / why section | Honest, a little passionate | "We built this because existing tools made us want to flip tables." |

---

# ✍️ Typography & Text

### Heading Hierarchy (with correct usage)

```markdown
# H1 — Project title. One per document. Do not use below the title.
## H2 — Major section. Gets its own TOC entry.
### H3 — Subsection within a major section.
#### H4 — Granular detail, like a specific API method or config field.
##### H5 — Rarely needed. Consider restructuring if you reach this.
###### H6 — Annotation level. Almost never appropriate.
```

### Text Emphasis — with semantic meaning

| Style | Syntax | Semantic Purpose |
|-------|--------|-----------------|
| **Bold** | `**text**` | Critical terms, UI element names, warnings |
| *Italic* | `*text*` | Book/article titles, introducing a technical term |
| ***Bold Italic*** | `***text***` | Maximum emphasis — use sparingly |
| ~~Strikethrough~~ | `~~text~~` | Deprecated features, corrected misconceptions |
| `Inline code` | `` `text` `` | All code, filenames, env vars, CLI commands |
| Subscript | `H~2~O` | Chemistry, math notation |
| Superscript | `x^2^` | Math, footnote references |

### Blockquote Patterns

**Standard callout:**
> 📌 **Note:** This is a standard blockquote. Use it for quotes, important notes, or commentary that supplements (but isn't critical to) the main flow.

**Layered attribution (dialogue, papers, code review):**
> **Original Reviewer:**
> > "The abstraction leaks here — the caller shouldn't need to know the DB schema."
> >
> > *— Code review, PR #224*

**Chapter epigraph (book-style docs):**
> *"Any fool can write code that a computer can understand. Good programmers write code that humans can understand."*
> — Martin Fowler

---

# 🚨 Callout Alerts

GitHub's native alert syntax renders with colored icons. These are your primary tools for directing reader attention.

> [!NOTE]
> **When to use:** Background information that's useful but not urgent. The reader can skim past this.

> [!TIP]
> **When to use:** A faster/smarter way to do something. Optional optimization the reader might love.

> [!IMPORTANT]
> **When to use:** Something the reader *must* understand for the current section to work. Not optional.

> [!WARNING]
> **When to use:** This action has non-obvious side effects or can cause data loss, security issues, or breaking changes.

> [!CAUTION]
> **When to use:** The nuclear option. Destructive, irreversible, or dangerous operations only.

**Callout anatomy (fill in like this):**
```markdown
> [!WARNING]
> **Irreversible action:** Running `DROP TABLE` in production will permanently delete all user records.
> Back up with `pg_dump mydb > backup.sql` before proceeding.
```

---

# 💻 Code Blocks

### Language Support Cheatsheet

| Use This Tag | For |
|---|---|
| `python` | Python scripts, notebooks, ML code |
| `typescript` / `javascript` | JS/TS — always specify which |
| `bash` / `sh` | Terminal commands, shell scripts |
| `sql` | All database queries |
| `yaml` / `toml` / `json` | Config files |
| `dockerfile` | Dockerfiles |
| `diff` | Showing before/after changes |
| `mermaid` | Diagrams (rendered live on GitHub) |
| `text` | Plain text output, logs |
| `http` | HTTP requests/responses |
| `graphql` | GraphQL schemas and queries |

### Python — Annotated Production Pattern
```python
# ─────────────────────────────────────────────────────────────
# WHY: dataclasses eliminate boilerplate __init__, __repr__
#      and give us type safety without runtime overhead
# ─────────────────────────────────────────────────────────────
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class ModelConfig:
    """Configuration for a training run. Passed to Trainer.fit()."""
    model_name: str
    learning_rate: float = 3e-4          # Karpathy's constant — works surprisingly often
    batch_size: int = 32
    epochs: int = 10
    dropout: float = 0.1
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def validate(self) -> None:
        """Raise ValueError if config is invalid."""
        if not 0 < self.learning_rate < 1:
            raise ValueError(f"learning_rate must be in (0, 1), got {self.learning_rate}")
        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")

config = ModelConfig(
    model_name="bert-base-uncased",
    learning_rate=2e-5,
    tags=["nlp", "fine-tuning"]
)
config.validate()
print(f"Training {config.model_name} for {config.epochs} epochs")
```

### TypeScript — Generic + Async Pattern
```typescript
// Generic fetch wrapper — handles errors, types responses correctly
interface ApiResponse {
  data: T;
  status: number;
  message: string;
  timestamp: string;
}

async function apiFetch(
  endpoint: string,
  options?: RequestInit
): Promise<ApiResponse> {
  const response = await fetch(`${process.env.API_BASE_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  });

  if (!response.ok) {
    // Throw with context — easier to debug than a generic fetch error
    throw new Error(`API ${response.status}: ${endpoint} — ${response.statusText}`);
  }

  return response.json();
}

// Usage
const { data: user } = await apiFetch('/users/me');
```

### Bash — Production Shell Script Pattern
```bash
#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# deploy.sh — Zero-downtime deployment script
# Usage: ./deploy.sh [--env production|staging] [--skip-tests]
# ─────────────────────────────────────────────────────────────────

set -euo pipefail   # -e: exit on error, -u: error on unset vars, -o: catch pipe failures
IFS=$'\n\t'         # Safer word splitting

readonly PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="$PROJECT_DIR/logs/deploy-$(date +%Y%m%d-%H%M%S).log"
readonly ENV="${1:-staging}"

log() { echo "[$(date +'%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
die() { log "❌ FATAL: $*"; exit 1; }

log "🚀 Starting $ENV deployment"

# Verify required tools
command -v docker >/dev/null 2>&1 || die "docker not found"
command -v kubectl >/dev/null 2>&1 || die "kubectl not found"

npm ci --production && log "✅ Dependencies installed"
npm test            && log "✅ Tests passed" || die "Tests failed — aborting"
npm run build       && log "✅ Build complete"

log "✅ Deployment to $ENV successful"
```

### HTTP Request/Response — API Documentation Pattern
```http
POST /api/v2/completions HTTP/1.1
Host: api.example.com
Authorization: Bearer sk-your-api-key-here
Content-Type: application/json

{
  "model": "gpt-4o",
  "messages": [{ "role": "user", "content": "Explain backpropagation" }],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
X-RateLimit-Remaining: 997

{
  "id": "cmpl-abc123",
  "choices": [{ "message": { "role": "assistant", "content": "..." } }],
  "usage": { "prompt_tokens": 20, "completion_tokens": 480, "total_tokens": 500 }
}
```

### Diff View — Change Documentation
```diff
- # v1.x — Synchronous, blocking
- def process_batch(items):
-     results = []
-     for item in items:
-         results.append(api.call(item))   # blocks until each returns
-     return results

+ # v2.x — Async, 10x faster
+ async def process_batch(items):
+     tasks = [api.call_async(item) for item in items]
+     return await asyncio.gather(*tasks)  # all requests fire in parallel
```

---

# 📊 Tables

### API Parameters Table (canonical format)
| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `model` | `string` | ✅ | — | Model identifier e.g. `gpt-4o` |
| `max_tokens` | `integer` | ❌ | `1024` | Upper bound on tokens generated |
| `temperature` | `float` | ❌ | `1.0` | Sampling temperature `[0.0, 2.0]` |
| `stream` | `boolean` | ❌ | `false` | Stream response chunks via SSE |
| `stop` | `string[]` | ❌ | `null` | Stop sequences — generation halts here |

### Feature Comparison Matrix
| Feature | Free | Pro | Enterprise |
|---------|:----:|:---:|:----------:|
| API Access | ✅ | ✅ | ✅ |
| Rate Limit | 100/hr | 10k/hr | Unlimited |
| Support | Community | Email 48h | Dedicated SLA |
| SLA Uptime | ❌ | 99.9% | 99.99% |
| SSO / SAML | ❌ | ❌ | ✅ |
| Audit Logs | ❌ | ❌ | ✅ |
| Custom Models | ❌ | ✅ | ✅ |

### Technology Stack Table (README standard)
| Technology | Version | Purpose | Docs |
|-----------|:-------:|---------|------|
| Python | 3.11+ | Core runtime | [docs.python.org](https://docs.python.org) |
| FastAPI | 0.111 | REST API framework | [fastapi.tiangolo.com](https://fastapi.tiangolo.com) |
| PostgreSQL | 16 | Primary database | [postgresql.org](https://www.postgresql.org/docs/) |
| Redis | 7.2 | Caching & queues | [redis.io](https://redis.io/docs/) |
| Docker | 25+ | Containerization | [docs.docker.com](https://docs.docker.com) |

### Error Code Reference Table
| HTTP Status | Code | Meaning | Resolution |
|:-----------:|------|---------|-----------|
| `400` | `INVALID_REQUEST` | Malformed JSON or missing fields | Check request schema |
| `401` | `UNAUTHORIZED` | Invalid or expired API key | Rotate key in dashboard |
| `403` | `FORBIDDEN` | Insufficient permissions | Check user role |
| `429` | `RATE_LIMITED` | Too many requests | Implement exponential backoff |
| `500` | `INTERNAL_ERROR` | Server-side failure | Retry; open issue if persistent |

---

# ✅ Task Lists

### Project Roadmap Checklist
- [x] Initialize repository structure
- [x] Write core module logic
- [x] Add unit tests (coverage > 80%)
- [x] Set up CI/CD pipeline
- [ ] Write API documentation
- [ ] Add integration tests
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] v1.0 release 🎉

### Nested Checklist — Multi-team Tracker
- [x] **Backend**
  - [x] Authentication system (JWT + refresh tokens)
  - [x] REST API endpoints
  - [ ] GraphQL migration
- [ ] **Frontend**
  - [x] Component library (Storybook)
  - [ ] Dark mode support
  - [ ] Accessibility audit (WCAG 2.1 AA)
- [ ] **Infrastructure**
  - [x] Docker containerization
  - [ ] Kubernetes manifests
  - [ ] Observability stack (Prometheus + Grafana)

---

# 🔀 Mermaid Diagrams

> [!TIP]
> Mermaid renders live on GitHub, GitLab, Notion, Obsidian, and most modern documentation platforms — no image hosting needed.

### Flowchart — System Architecture (TD)
```mermaid
flowchart TD
    User(["👤 Client"])
    CDN["🌐 CDN / Edge Cache"]
    LB["⚖️ Load Balancer"]
    Auth["🔐 Auth Service"]
    API["🔧 API Gateway"]
    DB[("🗄️ PostgreSQL")]
    Cache[("⚡ Redis")]
    Queue["📨 Message Queue"]
    Worker["⚙️ Background Worker"]
    Storage["🪣 Object Storage"]

    User -->|HTTPS| CDN
    CDN -->|Cache Miss| LB
    LB --> Auth
    Auth -->|Validated JWT| API
    API -->|Read/Write| DB
    API -->|Hot Data| Cache
    API -->|Async Jobs| Queue
    API -->|File Uploads| Storage
    Queue --> Worker
    Worker -->|Write Results| DB

    style User fill:#4A90D9,color:#fff,stroke:none
    style CDN fill:#9B59B6,color:#fff,stroke:none
    style Auth fill:#E67E22,color:#fff,stroke:none
    style API fill:#27AE60,color:#fff,stroke:none
    style DB  fill:#2C3E50,color:#fff,stroke:none
    style Cache fill:#E74C3C,color:#fff,stroke:none
    style Queue fill:#16A085,color:#fff,stroke:none
    style Worker fill:#8E44AD,color:#fff,stroke:none
```

### Sequence Diagram — OAuth 2.0 / PKCE Flow
```mermaid
sequenceDiagram
    actor User
    participant App as Client App
    participant Auth as Auth Server
    participant API as Resource API

    User->>App: Click "Login with GitHub"
    App->>App: Generate code_verifier + code_challenge (S256)
    App->>Auth: GET /authorize?code_challenge=...&scope=read:user
    Auth->>User: Show consent screen
    User->>Auth: Approve permissions
    Auth-->>App: Redirect with ?code=AUTH_CODE

    App->>Auth: POST /token (code + code_verifier)
    Auth->>Auth: Verify PKCE challenge
    Auth-->>App: access_token + refresh_token

    App->>API: GET /user (Bearer access_token)
    API-->>App: User profile data
    App->>User: Show dashboard

    Note over App,Auth: Tokens expire in 1hr; refresh silently
```

### State Diagram — Entity Lifecycle
```mermaid
stateDiagram-v2
    direction LR
    [*] --> Draft : Created
    Draft --> Review : Submit
    Draft --> Deleted : Delete
    Review --> Approved : Approve
    Review --> Draft : Request Changes
    Review --> Rejected : Reject
    Approved --> Published : Publish
    Approved --> Draft : Unpublish
    Published --> Archived : Archive
    Archived --> [*]
    Deleted --> [*]
    Rejected --> [*]
```

### ER Diagram — Data Model
```mermaid
erDiagram
    USER {
        uuid    id          PK
        string  email       UK
        string  name
        enum    role        "admin|member|viewer"
        timestamp created_at
    }
    PROJECT {
        uuid    id          PK
        string  title
        uuid    owner_id    FK
        boolean is_public
    }
    TASK {
        uuid    id          PK
        string  title
        enum    status      "todo|in_progress|done"
        uuid    project_id  FK
        uuid    assignee_id FK
        date    due_date
    }

    USER ||--o{ PROJECT : "owns"
    PROJECT ||--o{ TASK : "contains"
    USER ||--o{ TASK : "assigned to"
```

### Gantt Chart — Release Roadmap
```mermaid
gantt
    title Release Roadmap — v2.0
    dateFormat  YYYY-MM-DD
    excludes    weekends

    section Discovery
    Requirements           :done,     req,   2025-01-06, 10d
    Technical spike        :done,     spike, 2025-01-13, 8d

    section Development
    Core engine            :done,     core,  2025-01-20, 30d
    API redesign           :active,   api,   2025-02-10, 20d
    Frontend               :          fe,    2025-03-01, 25d

    section QA
    Automated test suite   :          test,  2025-03-20, 10d
    Beta program           :          beta,  2025-03-28, 14d

    section Launch
    Documentation          :          docs,  2025-04-07, 7d
    Production release     :milestone, rel,  2025-04-14, 0d
```

### Git Graph — Trunk-Based Branching
```mermaid
gitGraph
    commit id: "Initial commit"
    commit id: "Project scaffold"

    branch develop
    checkout develop
    commit id: "Auth module"
    commit id: "User model"

    branch feature/payments
    checkout feature/payments
    commit id: "Stripe integration"
    commit id: "Webhook handler"
    checkout develop
    merge feature/payments id: "Merge: payments"

    branch release/1.0
    checkout release/1.0
    commit id: "Bump version"
    commit id: "Changelog"

    checkout main
    merge release/1.0 id: "v1.0 🚀" tag: "v1.0.0"
    checkout develop
    merge main id: "Sync ← main"
```

### Quadrant — Feature Priority Matrix
```mermaid
quadrantChart
    title Feature Prioritization (Effort vs Impact)
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Quick Wins
    quadrant-2 Major Bets
    quadrant-3 Fill-ins
    quadrant-4 Avoid
    Dark Mode:          [0.25, 0.75]
    Offline Support:    [0.85, 0.90]
    Push Notifications: [0.40, 0.65]
    CSV Export:         [0.15, 0.40]
    GraphQL Migration:  [0.90, 0.70]
    AI Search:          [0.60, 0.88]
    UI Refresh:         [0.30, 0.50]
```

### Mindmap — Project Architecture
```mermaid
mindmap
  root((Platform))
    Backend
      Python / FastAPI
        REST Endpoints
        Background Tasks
        WebSocket Gateway
      Data Layer
        PostgreSQL
        Redis Cache
        S3 Storage
    Frontend
      React + TypeScript
        Component Library
        State: Zustand
        Router: TanStack
      Styling
        Tailwind CSS
        Design Tokens
    Infrastructure
      Docker + K8s
      GitHub Actions CI
      Monitoring
        Prometheus
        Grafana
        Sentry
```

### Pie Chart — Usage Analytics
```mermaid
pie title API Calls by Endpoint (Last 30 Days)
    "GET /users"      : 38
    "POST /sessions"  : 24
    "GET /projects"   : 18
    "POST /tasks"     : 12
    "Other"           : 8
```

---

# 🧮 Math & Formulas (LaTeX)

> GitHub renders LaTeX natively since 2022. Use `$...$` for inline and `$$...$$` for block equations.

### Inline Math Examples

The gradient descent update rule is $\theta := \theta - \alpha \nabla_\theta J(\theta)$, where $\alpha$ is the learning rate.

Binary search has time complexity $O(\log n)$; Dijkstra's algorithm on a dense graph runs in $O(V^2)$.

The quadratic formula gives roots at $x = \dfrac{-b \pm \sqrt{b^2 - 4ac}}{2a}$.

### Foundational Equations

**Euler's Identity:**
$$e^{i\pi} + 1 = 0$$

**Standard Normal Distribution:**
$$f(x \mid \mu, \sigma^2) = \frac{1}{\sigma\sqrt{2\pi}} \exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

**Shannon Entropy:**
$$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

### Neural Network — Full Backpropagation Derivation

> [!NOTE]
> This section demonstrates the full mathematical treatment for AI/ML documentation. Each equation corresponds to a concrete implementation step.

**Network definition:** A 3-layer network with input $\mathbf{x}$, hidden layer, output $\hat{y}$, and scalar loss $\mathcal{L}$.

**Forward Pass:**

$$z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}$$

$$a^{(l)} = \sigma\!\left(z^{(l)}\right)$$

where $\sigma$ is the activation function (ReLU, sigmoid, etc.).

**Loss (Cross-entropy):**

$$\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\left[y_i \log \hat{y}_i + (1 - y_i)\log(1 - \hat{y}_i)\right]$$

**Backward Pass — Chain Rule unrolled:**

Output layer error:
$$\delta^{(L)} = \frac{\partial \mathcal{L}}{\partial z^{(L)}} = \hat{y} - y$$

Hidden layer error (propagating backwards):
$$\delta^{(l)} = \left(W^{(l+1)}\right)^\top \delta^{(l+1)} \odot \sigma'\!\left(z^{(l)}\right)$$

where $\odot$ denotes element-wise (Hadamard) product and $\sigma'$ is the derivative of the activation.

**Gradient of weights and biases:**

$$\frac{\partial \mathcal{L}}{\partial W^{(l)}} = \delta^{(l)} \left(a^{(l-1)}\right)^\top \qquad \frac{\partial \mathcal{L}}{\partial b^{(l)}} = \delta^{(l)}$$

**Weight Update (SGD with momentum):**

$$v_t = \beta v_{t-1} + (1 - \beta)\,\nabla_W \mathcal{L}$$

$$W \leftarrow W - \alpha \, v_t$$

**Adam Optimizer (the industry standard):**

$$m_t = \beta_1 m_{t-1} + (1-\beta_1)\,g_t \qquad v_t = \beta_2 v_{t-1} + (1-\beta_2)\,g_t^2$$

$$\hat{m}_t = \frac{m_t}{1-\beta_1^t} \qquad \hat{v}_t = \frac{v_t}{1-\beta_2^t}$$

$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon}\,\hat{m}_t$$

**Complexity Reference:**

| Algorithm | Time | Space | Notes |
|-----------|:----:|:-----:|-------|
| Forward pass | $O(L \cdot d^2)$ | $O(L \cdot d)$ | $L$ layers, $d$ width |
| Backward pass | $O(L \cdot d^2)$ | $O(L \cdot d)$ | Same as forward |
| Adam update | $O(d)$ | $O(d)$ | Per parameter |

### Transformer Self-Attention

$$\text{Attention}(Q,K,V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

Multi-head attention combines $h$ parallel attention heads:

$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\,W^O$$

---

# 🎬 Animated SVGs (GitHub-Compatible)

> [!IMPORTANT]
> GitHub strips JavaScript and CSS `@keyframes` in inline `<style>` blocks, but **SVG-native `<animate>` and `<animateTransform>` elements render and play correctly.** Commit the `.svg` file to your repo and reference it like an image.

### How to Create & Embed an Animated SVG

**Step 1 — Create `assets/neural-net-forward.svg`** using SVG animate tags:
```xml

  
  
    
  

  
  
  
    
      
    
  

  
  
    
  

```

**Step 2 — Embed in your README:**
```markdown

  
  
  Figure 1: Forward pass — activations propagate left to right

```

### What to Animate (and When)
| Animation Type | Best For | SVG Technique |
|---|---|---|
| Node lighting up | Forward pass, activation | `<animate attributeName="fill">` |
| Signal pulse on edge | Data flow, message passing | `<animateMotion>` |
| Color shifting | Phase transitions (forward → backward) | `<animate attributeName="fill" values="...">` |
| Opacity pulse | Highlighting a component | `<animate attributeName="opacity">` |
| Rotation | Loading states, spinning icons | `<animateTransform type="rotate">` |
| Path drawing | Algorithm trace, routing | `<animate attributeName="stroke-dashoffset">` |

> [!TIP]
> Generate animated SVGs programmatically with Python's `svgwrite` library or Node's `svg.js`. Then commit the `.svg` to your `assets/` folder — no external hosting required.

---

# 🖼️ Images & Figures

### Centered Figure with Caption
```html

  
  
  Figure 1: Request lifecycle from client to database, including cache and async queue layers.

```

### Side-by-Side Comparison
<div align="center">

| Before | After |
|:------:|:-----:|
| ![Before](https://via.placeholder.com/320x200/E74C3C/FFFFFF?text=v1+UI) | ![After](https://via.placeholder.com/320x200/27AE60/FFFFFF?text=v2+UI) |
| ❌ Cluttered layout, poor hierarchy | ✅ Clean, scannable, accessible |

</div>

### Responsive Banner (no fixed pixel width)
```markdown
[![Project Banner](./assets/banner.svg)](https://your-project-site.com)
```

### Image Grid (2×2 layout using HTML table)
```html

  
    
    
  
  
    
    
  

```

---

# 🔽 Collapsible Sections

```html

📦 Full Dependency List — click to expand

### Runtime
| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | `^0.111` | Web framework |
| `sqlalchemy` | `^2.0` | ORM |
| `redis` | `^5.0` | Cache layer |
| `pydantic` | `^2.5` | Schema validation |

### Development
| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | `^8.0` | Test runner |
| `ruff` | `^0.4` | Fast linter |
| `mypy` | `^1.9` | Type checking |


```

<details>
<summary>🏗️ <strong>Architecture Decision Records (ADRs)</strong></summary>

### ADR-001: PostgreSQL over MongoDB
**Status:** Accepted  
**Context:** Needed a primary database for a multi-tenant SaaS app with complex relational queries.  
**Decision:** PostgreSQL with JSONB columns for flexible fields.  
**Consequences:** ✅ ACID guarantees, complex JOINs, mature tooling. ❌ Schema migrations require more care.

### ADR-002: Redis for Session Storage
**Status:** Accepted  
**Context:** JWT refresh token rotation requires server-side invalidation.  
**Decision:** Store refresh token allowlist in Redis with TTL matching token expiry.  
**Consequences:** ✅ Sub-millisecond invalidation. ❌ Additional infrastructure dependency.

</details>

<details>
<summary>🐛 <strong>Known Issues & Workarounds</strong></summary>

### Issue #142 — Memory leak on large file uploads
**Status:** 🔄 In progress (target: v2.1.1)  
**Workaround:** Limit uploads to 10MB until fixed.

```python
# Add to your upload config
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

def validate_upload(file: UploadFile) -> None:
    if file.size > MAX_UPLOAD_SIZE:
        raise HTTPException(413, "File too large — 10MB limit until v2.1.1")
```

</details>

---

# ⌨️ Keyboard Shortcuts & HTML Extras

### Keyboard Shortcut Rendering
Open command palette: <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd>

Save file: <kbd>⌘</kbd> + <kbd>S</kbd> · Format: <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>F</kbd>

Run all tests: <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd>

### Superscript & Subscript
Chemical: H<sub>2</sub>SO<sub>4</sub> · Area: A = πr<sup>2</sup> · Footnote reference<sup>[1]</sup>

### Definition Lists (rendered in some parsers)
```markdown
API Gateway
: A server that acts as the single entry point for all client requests, routing them to the appropriate microservice.

JWT (JSON Web Token)
: A compact, URL-safe token format for representing claims between two parties.
```

---

# 📎 Footnotes & References

This project implements the Repository Pattern[^1] combined with Domain-Driven Design[^2] principles.

The auth system follows the OAuth 2.0 + PKCE specification[^3] and stores credentials using Argon2id[^4].

Benchmark methodology and raw results are available in the `/benchmarks/` directory[^5].

[^1]: Fowler, M. (2002). *Patterns of Enterprise Application Architecture*. Addison-Wesley. Ch. 10.
[^2]: Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
[^3]: IETF RFC 7636 — [Proof Key for Code Exchange](https://tools.ietf.org/html/rfc7636)
[^4]: Biryukov, A. et al. (2015). *Argon2: The Memory-Hard Function for Password Hashing*. PHC Competition.
[^5]: See `benchmarks/README.md` for full methodology, hardware specs, and raw CSV data.

---

# 🏷️ Badges & Shields — Complete Ecosystem

> All badges use [shields.io](https://shields.io). Pattern: `https://img.shields.io/badge/LABEL-MESSAGE-COLOR?style=STYLE&logo=LOGO`

### The Essential Badge Block (copy-paste template)
```markdown


[![Build Status](https://github.com/YOUR_USER/YOUR_REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USER/YOUR_REPO/actions)
[![Coverage](https://codecov.io/gh/YOUR_USER/YOUR_REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USER/YOUR_REPO)
[![Version](https://img.shields.io/github/v/release/YOUR_USER/YOUR_REPO?include_prereleases&color=blue)](https://github.com/YOUR_USER/YOUR_REPO/releases)
[![License](https://img.shields.io/github/license/YOUR_USER/YOUR_REPO)](LICENSE)
[![Stars](https://img.shields.io/github/stars/YOUR_USER/YOUR_REPO?style=social)](https://github.com/YOUR_USER/YOUR_REPO/stargazers)


```

### CI/CD & Quality Badges
```markdown

![CI](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)


![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)


![Codacy](https://app.codacy.com/project/badge/Grade/YOUR_ID)


![Snyk](https://snyk.io/test/github/user/repo/badge.svg)


![SonarCloud](https://sonarcloud.io/api/project_badges/measure?project=YOUR_KEY&metric=alert_status)
```

### View Count & Visitor Tracking Badges
```markdown

![Views](https://komarev.com/ghpvc/?username=YOUR_USERNAME&color=blueviolet&style=for-the-badge&label=PROFILE+VIEWS)


![Visitors](https://visitor-badge.laobi.icu/badge?page_id=YOUR_USERNAME.YOUR_REPO)


[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FUSER%2FREPO)](https://hits.seeyoufarm.com)
```

### Technology Stack Badges (logo gallery)
```markdown

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-stable-000000?logo=rust&logoColor=white)
![Go](https://img.shields.io/badge/Go-1.22+-00ADD8?logo=go&logoColor=white)


![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-000000?logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)


![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-326CE5?logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?logo=amazon-aws&logoColor=white)

<!-- AI/ML -->
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch&logoColor=white)
![HuggingFace](https://img.shields.io/badge/🤗_HuggingFace-Transformers-FFD21E)
![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai&logoColor=white)
```

### Social & Community Badges
```markdown
[![Twitter Follow](https://img.shields.io/twitter/follow/YOUR_HANDLE?style=social)](https://twitter.com/YOUR_HANDLE)
[![Discord](https://img.shields.io/discord/YOUR_SERVER_ID?logo=discord&label=Discord&color=5865F2)](https://discord.gg/YOUR_INVITE)
[![Reddit](https://img.shields.io/reddit/subreddit-subscribers/YOUR_SUBREDDIT?style=social)](https://reddit.com/r/YOUR_SUBREDDIT)
[![YouTube](https://img.shields.io/youtube/channel/subscribers/YOUR_CHANNEL_ID?style=social)](https://youtube.com/c/YOUR_CHANNEL)
```

### Badge Style Reference
| Style | Syntax | Example Output |
|-------|--------|---------------|
| `flat` | `?style=flat` | Default, compact |
| `flat-square` | `?style=flat-square` | Sharp corners |
| `for-the-badge` | `?style=for-the-badge` | Large, prominent |
| `plastic` | `?style=plastic` | Gradient effect |
| `social` | `?style=social` | GitHub social style |

---

# 📊 GitHub Profile Widgets

> These are hosted services that generate dynamic SVG cards — embed them like images.

### GitHub Stats Card
```markdown

  
  

```

### GitHub Streak Counter
```markdown

  

```

### GitHub Activity Graph
```markdown

  

```

### GitHub Profile Trophies
```markdown

  

```

### WakaTime Coding Stats (requires WakaTime account)
```markdown
[![WakaTime](https://wakatime.com/badge/user/YOUR_WAKATIME_ID.svg)](https://wakatime.com/@YOUR_USERNAME)
```

### Skill Icons Grid
```markdown

[![Skills](https://skillicons.dev/icons?i=python,typescript,react,postgres,redis,docker,kubernetes,aws&theme=dark)](https://skillicons.dev)
```

### Available Themes for All Widgets
`default` · `dark` · `tokyonight` · `dracula` · `radical` · `merko` · `gruvbox` · `onedark` · `cobalt` · `synthwave` · `highcontrast` · `ocean`

---

# ⚡ External APIs & Live Integrations

> These are real services you can wire into your repository with zero backend code.

### Shields.io — Dynamic Data Endpoints
```markdown

![npm downloads](https://img.shields.io/npm/dm/YOUR_PACKAGE)


![PyPI downloads](https://img.shields.io/pypi/dm/YOUR_PACKAGE)


![Open Issues](https://img.shields.io/github/issues/USER/REPO)


![Last Commit](https://img.shields.io/github/last-commit/USER/REPO)


![Repo Size](https://img.shields.io/github/repo-size/USER/REPO)


![Contributors](https://img.shields.io/github/contributors/USER/REPO)
```

### Readme.so — Visual Badge Builder
> [readme.so](https://readme.so) — drag-and-drop README section builder. Export as Markdown.

### Carbon — Beautiful Code Screenshots
```markdown

[![Carbon](https://carbon.now.sh/static/brand/banner.svg)](https://carbon.now.sh/?bg=rgba(171,184,195,1)&t=seti&l=python&code=YOUR_CODE_URI_ENCODED)
```

### Repl.it — Embedded Interactive Code
```markdown

[![Run on Repl.it](https://replit.com/badge/github/USER/REPO)](https://replit.com/github/USER/REPO)
```

### Gitpod — One-Click Dev Environment
```markdown
[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/USER/REPO)
```

### CodeSandbox — Browser-Based IDE
```markdown
[![Edit on CodeSandbox](https://codesandbox.io/static/img/play-codesandbox.svg)](https://codesandbox.io/s/github/USER/REPO/tree/main)
```

### Deepnote / Google Colab — Notebook Launch Buttons
```markdown

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USER/REPO/blob/main/notebooks/demo.ipynb)


[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/USER/REPO/HEAD)
```

### Vercel / Netlify — Deploy Buttons
```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/USER/REPO)
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/USER/REPO)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/USER/REPO)
```

---

# 📚 Book-Quality Structure Patterns

## Repository Folder Architecture

```text
my-project/
├── README.md                    ← Hook, badges, 30-second overview
├── CHANGELOG.md                 ← Keep a Changelog format
├── CONTRIBUTING.md              ← How to contribute
├── SECURITY.md                  ← Vulnerability reporting policy
├── CODE_OF_CONDUCT.md           ← Community standards
├── LICENSE                      ← Full license text
│
├── docs/
│   ├── 00-overview.md           ← Project vision and non-goals
│   ├── 01-getting-started.md    ← Install → run in < 5 minutes
│   ├── 02-architecture.md       ← System design, ADRs
│   ├── 03-api-reference.md      ← Full API documentation
│   ├── 04-configuration.md      ← All config options explained
│   ├── 05-deployment.md         ← Dev → staging → production
│   ├── 06-troubleshooting.md    ← Common errors and fixes
│   └── 07-changelog.md          ← Detailed version history
│
├── assets/
│   ├── banner.svg               ← Project hero banner
│   ├── architecture.png         ← System diagram (high-res)
│   └── demo.gif                 ← 30-second product demo
│
└── examples/
    ├── basic-usage.md
    └── advanced-patterns.md
```

## Cross-File Linking (Always Use Relative Paths)
```markdown
For the full API reference, see [API Documentation](docs/03-api-reference.md).

Jump directly to [Authentication → JWT Flow](docs/03-api-reference.md#jwt-flow).

Related: [Deployment Guide → Docker](docs/05-deployment.md#docker).
```

## CHANGELOG Format (Keep a Changelog Standard)
```markdown
# Changelog

All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- New streaming API endpoint for real-time completions

## [2.1.0] — 2025-04-14
### Added
- OAuth 2.0 + PKCE authentication flow
- Redis-backed session invalidation

### Changed
- Upgraded from Python 3.10 → 3.11 (breaking: remove 3.10 support)

### Fixed
- Memory leak on concurrent large file uploads (#142)

### Deprecated
- `POST /auth/token` (legacy) — use `POST /auth/v2/token` instead

### Removed
- `GET /api/v1/` endpoints removed (deprecated in v1.9)

[Unreleased]: https://github.com/user/repo/compare/v2.1.0...HEAD
[2.1.0]: https://github.com/user/repo/compare/v2.0.0...v2.1.0
```

---

# 📋 README Templates by Project Type

## Template A — Open Source Library
```markdown
# 🦾 LibraryName
> One-sentence pitch: what it does and why it's better.

[![npm](https://img.shields.io/npm/v/library-name)](https://npmjs.com/package/library-name)
[![Downloads](https://img.shields.io/npm/dm/library-name)](https://npmjs.com)

## Why?
[Problem] — Existing solutions require X, Y, and Z. This library does it in one line.

## Install
```bash
npm install library-name
```

## Quick Start
```js
import { feature } from 'library-name';
const result = feature({ option: 'value' });
```

## API Reference
[See full docs →](docs/api.md)

## Contributing
[CONTRIBUTING.md](CONTRIBUTING.md)
```

## Template B — Developer Tool / CLI
```markdown
# ⚡ toolname — [One-line description]

[![Homebrew](https://img.shields.io/badge/brew-install-orange?logo=homebrew)]()

## Install
| Method | Command |
|--------|---------|
| Homebrew | `brew install toolname` |
| curl | `curl -fsSL https://... \| sh` |
| npm | `npm i -g toolname` |

## Usage
```bash
toolname [command] [options]
toolname init        # Initialize project
toolname build       # Build output
toolname deploy --env production
```

## Commands
| Command | Description |
|---------|-------------|
| `init` | Scaffold new project |
| `build` | Compile source |
| `deploy` | Push to environment |
```

## Template C — Web Application / SaaS Product
```markdown
# 🚀 ProductName
> Tagline that communicates value in under 10 words.

[Live Demo](https://demo.product.com) · [Documentation](https://docs.product.com) · [Discord](https://discord.gg/invite)

## ✨ Features
- **Feature 1** — What it does and why it matters
- **Feature 2** — Specific, concrete benefit
- **Feature 3** — Quantified improvement where possible ("3× faster")

## 🏗️ Architecture
[Mermaid diagram here]

## 🚦 Getting Started
[Step-by-step with actual runnable commands]

## 🤝 Contributing
We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).
```

---

# 🤖 AI/ML Documentation Patterns

## Model Card Template (Hugging Face Standard)
```markdown
# 🤗 Model Card — ModelName

## Model Summary
| Field | Detail |
|-------|--------|
| **Task** | Text Classification |
| **Language** | English |
| **License** | Apache 2.0 |
| **Base Model** | `bert-base-uncased` |
| **Parameters** | 110M |
| **Context Length** | 512 tokens |

## Intended Use
**In-scope:** Sentiment analysis on product reviews (English, e-commerce domain).  
**Out-of-scope:** Medical text, legal documents, non-English input.

## Performance
| Dataset | Accuracy | F1 | AUC-ROC |
|---------|:--------:|:--:|:-------:|
| SST-2 | 93.4% | 0.934 | 0.971 |
| Amazon Reviews | 91.2% | 0.909 | 0.956 |
| Custom Eval | 89.7% | 0.891 | 0.944 |

## Limitations & Biases
> [!WARNING]
> This model was fine-tuned on English e-commerce reviews. Performance degrades on:
> - Reviews shorter than 5 words
> - Mixed-language input (code-switching)
> - Sarcasm and irony (F1 drops to ~0.71)

## Training Details
**Dataset:** 2.4M Amazon product reviews (filtered: ≥3 words, English only)  
**Hardware:** 4× A100 80GB, ~18 hours  
**Framework:** PyTorch 2.1 + HuggingFace Transformers 4.38

## Citation
```bibtex
@model{modelname2025,
  author    = {Author, A.},
  title     = {ModelName: Description},
  year      = {2025},
  publisher = {HuggingFace},
  url       = {https://huggingface.co/author/modelname}
}
```
```

## Experiment Tracking Table
| Run ID | Model | LR | Batch | Epochs | Val Loss | Val Acc | Notes |
|--------|-------|:--:|:-----:|:------:|:--------:|:-------:|-------|
| `run-001` | bert-base | 2e-5 | 32 | 5 | 0.182 | 93.1% | Baseline |
| `run-002` | bert-base | 3e-5 | 32 | 5 | 0.194 | 92.6% | LR too high |
| `run-003` | bert-base | 2e-5 | 64 | 5 | 0.179 | **93.4%** | ✅ Best |
| `run-004` | roberta-base | 1e-5 | 32 | 8 | 0.171 | 94.1% | Larger model |

## Confusion Matrix (as a Markdown table)
| | Predicted Positive | Predicted Negative |
|--|:-----------------:|:-----------------:|
| **Actual Positive** | TP: 4,821 ✅ | FN: 312 ❌ |
| **Actual Negative** | FP: 203 ❌ | TN: 4,664 ✅ |

**Precision:** $\frac{TP}{TP+FP} = \frac{4821}{5024} = 95.9\%$ · **Recall:** $\frac{TP}{TP+FN} = \frac{4821}{5133} = 93.9\%$

---

# 😄 Emoji Reference

Use purposefully — emojis add scannability but lose meaning when overused.

| Category | Use Case | Emojis |
|----------|----------|--------|
| Status | Section headers, task lists | ✅ ❌ ⚠️ 🔄 🚧 🆕 🔥 |
| Documents | File types, sections | 📄 📁 📂 📝 📋 📊 📈 📉 |
| Code & Dev | Technical sections | 💻 🔧 🐛 🚀 🔐 ⚙️ 🏗️ |
| Navigation | TOC, links, pointers | 📌 🔝 ➡️ ⬆️ 🔗 📎 |
| Time | Roadmaps, changelogs | ⏱️ 📅 🗓️ ⏳ 🕐 |
| People | Teams, auth, users | 👤 👥 🧑‍💻 🤝 🙋 |
| Science | AI/ML, math, research | 🧠 🔬 🧮 📐 🤖 🎯 |

---

# ✅ The Quality Checklist

> [!IMPORTANT]
> **AI models must run through every item in this list before returning output.**
> A document passes only when every box is checked.

### Structure
- [ ] `H1` appears exactly once (the title)
- [ ] Headings follow hierarchy (no skipped levels)
- [ ] Table of contents present for docs > 300 words
- [ ] Every section in TOC has a matching heading anchor
- [ ] Back-to-top link at the end of long documents

### Content
- [ ] All code blocks have a language specifier
- [ ] Every code example is **runnable** or explicitly marked `# conceptual`
- [ ] All links point to real URLs (no `#placeholder`, no `TODO: add link`)
- [ ] All images have descriptive `alt` text
- [ ] Footnotes use proper `[^n]` syntax

### Visual Elements
- [ ] Badges are centered in a `<div align="center">` block
- [ ] At least one Mermaid diagram for any architecture/flow doc
- [ ] Callout alerts used for Notes/Tips/Warnings (not raw blockquotes)
- [ ] Tables have correct alignment (`:---` left, `:---:` center, `---:` right)

### Tone & Accessibility
- [ ] Acronyms spelled out on first use
- [ ] No "click here" or "here" as link text
- [ ] Beginner can understand the Quick Start without reading the rest
- [ ] No broken `==highlighted==` syntax (GitHub doesn't render it — use `**bold**`)

### AI/ML Docs (additional)
- [ ] All LaTeX equations tested for correct syntax
- [ ] Model card includes limitations and bias disclosure
- [ ] Experiment table has a clear "best run" indicator
- [ ] Citation block provided for academic work

---

<div align="center">

---

**🏆 The Markdown Grandmaster Skill — v3.0**

*Feed this to any model. Watch the documentation become legendary.*

[![Made with Markdown](https://img.shields.io/badge/Made_with-Markdown-1f425f?style=for-the-badge&logo=markdown)](https://www.markdownguide.org)
[![Skill Version](https://img.shields.io/badge/Skill-v3.0-blueviolet?style=for-the-badge)](.)
[![AI Ready](https://img.shields.io/badge/AI-Skill_Ready-orange?style=for-the-badge&logo=openai&logoColor=white)](.)

[⬆ Back to Top](#-the-markdown-grandmaster-skill)

</div>