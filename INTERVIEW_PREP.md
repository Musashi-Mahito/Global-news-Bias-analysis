# Interview Prep: Global News Bias Analyzer Walkthrough

Use this guide to master the narrative pitch, database selections, and engineering design patterns of this application to wow interviewers.

---

## 🎙️ 1. The Elevator Pitch (30-Second Overview)

> "I built a production-grade AI web application that automatically audits potential bias in news articles. Unlike basic sentiment detectors, it performs **narrative auditing** by using a multi-agent pipeline. It fetches related coverages, extracts named entities and structured facts, constructs a Knowledge Graph in **Neo4j**, performs dense vector searches in **Qdrant**, and computes consensus/conflict statistics. It is coordinated through a **Spring Boot** gateway API, a **FastAPI** AI pipeline, and a **Next.js 16 (React 19)** interactive dashboard."

---

## 🏛️ 2. The Architectural Design Decision

**Interviewer: "Why did you use three databases (PostgreSQL, Neo4j, Qdrant)? Isn't that overkill?"**

### The Response:
"Each database fits a specific mathematical and retrieval pattern, following the **Single Responsibility Principle**:
1. **PostgreSQL (Relational)**: Handles structured, ACID-compliant transactional data. It stores user profiles, auth credentials, raw article text, meta parameters, and final summarized analysis reports.
2. **Qdrant (Vector)**: Built specifically for dense vector storage and similarity search. It allows us to index sentence embeddings and query related news documents using cosine similarity. Performing vector search in standard SQL databases is slow and lacks custom payload filters.
3. **Neo4j (Graph)**: Optimized for entity relationship mapping. Representing claims (`subject-predicate-object`) and entity connections in SQL requires expensive multi-way table joins. In Neo4j, Cypher queries traverse these index-free adjacent connections in $O(1)$ time, mapping narrative structures seamlessly."

---

## 🤖 3. The 8-Agent Pipeline Orchestration

**Interviewer: "Walk me through how the analysis pipeline works step-by-step."**

When a user submits an article URL or text to `/article/analyze`:

```text
[URL/Text Ingestion]
         │
         ▼
Agent 1: Article Extractor (Parses URL structure, main body text, and meta dates)
         │
         ▼
Agent 2: News Retriever (Queries RSS directories and web scrapers to gather related coverages)
         │
         ├──────────────────────────┐
         ▼                          ▼
Agent 3: Entity Extractor     Agent 4: Claim Extractor
(Named Entity Recognition)     (Converts paragraphs to subject-predicate-object triples)
         │                          │
         └─────────────┬────────────┘
                       ▼
Agent 5: Graph Builder (Indexes vectors in Qdrant, updates nodes & links in Neo4j)
         │
         ▼
Agent 6: Bias Analyzer (Compares main article text with related coverages to score bias)
         │
         ▼
Agent 7: Consensus Analyzer (Finds factual alignments and isolates direct contradictions)
         │
         ▼
Agent 8: Report Generator (Generates Conservative, Liberal, and Neutral summaries + timelines)
```

---

## ⚙️ 4. Overcoming Core Engineering Challenges

**Interviewer: "What are some real engineering challenges you faced during this project?"**

### Challenge A: React 19 Component Compatibility (Frontend)
- **The Issue**: React 19 introduced major context API changes. Standard third-party visual canvas libraries (like `react-force-graph` or canvas packages) broke or had severe peer dependency conflicts during builds.
- **The Solution**: I wrote a **custom interactive Spring-Force Physics engine** inside [KnowledgeGraph.tsx](file:///Users/prathmesh/Desktop/Projects/NewsBiasDetector/frontend/src/components/KnowledgeGraph.tsx) using pure SVG and native React state hooks.
- **The Code**: The engine runs Coulomb's repulsion and Hooke's spring formulas in an animation tick loop (`requestAnimationFrame`), binding coordinates directly to SVG `<circle>` and `<line>` elements. This is lightweight, compiles instantly under React 19, and is fully responsive.

### Challenge B: Python Folder Import Restrictions
- **The Issue**: Originally, the AI microservice directory was named `ai-service`. Python imports do not support folders containing hyphens (`import ai-service` is interpreted as a subtraction command and fails).
- **The Solution**: I renamed the directory to `ai_service` (with an underscore) and updated Python references, resolving ASGI module importing issues.

### Challenge C: Port Conflicts on Local Developer Environment
- **The Issue**: PostgreSQL runs standardly on port `5432` and Neo4j on `7687`/`7474`. If a developer already has local database instances active, Docker compose fails.
- **The Solution**: I configured isolated host ports (`5433`, `7688`, `6335`) in [docker-compose.yml](file:///Users/prathmesh/Desktop/Projects/NewsBiasDetector/docker-compose.yml) and mapped config clients accordingly to ensure zero-install portability.

---

## ❓ 5. Top 10 Technical Interview FAQs

#### Q1: How does JWT authentication work in Spring Boot?
> **Answer**: It intercepts incoming HTTP calls via a custom `JwtAuthenticationFilter` extending `OncePerRequestFilter`. It reads the `Authorization` header, extracts the `Bearer ` token, validates it against `JwtUtils` and `UserDetailsService`, and sets the authenticated token context in `SecurityContextHolder`.

#### Q2: Why did you compile to Java 21?
> **Answer**: Java 21 is the industry standard LTS (Long-Term Support) release introducing **Virtual Threads** (Project Loom) for lightweight concurrency and modern **Pattern Matching** switches, while compiling cleanly on modern JVM platforms.

#### Q3: What is the benefit of using FastAPI instead of Flask?
> **Answer**: FastAPI is built on ASGI (Asynchronous Server Gateway Interface), offering asynchronous route handlers, automatic Pydantic validation (which maps directly to request/response models), and native OpenAPI documentation.

#### Q4: How is similarity search calculated in Qdrant?
> **Answer**: We generate a 384-dimensional dense vector representing the text. Qdrant computes the **Cosine Similarity** between the target vector and stored points using the formula:
> $$\text{Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$
> The resulting score (0.0 to 1.0) dictates how semantically similar the coverages are.

#### Q5: How do you handle cases where LLM API keys are not provided?
> **Answer**: I implemented a local **Mock Fallback Mode** in `LLMService` that uses regex classifiers and deterministic templates based on text hashes. This guarantees the entire multi-service application is fully runnable, testable, and compile-proof immediately after clonings.

#### Q6: How does the Consensus Engine identify contradictions?
> **Answer**: The Consensus agent maps extracted claim triples. It isolates matching subjects (e.g. "crowd size") and checks if the predicate verbs contain opposing modifiers (such as negations "no", "not" or verbs like "increased" vs "decreased"), grouping them as disputed claims.

#### Q7: What is GraphRAG?
> **Answer**: Retrieval-Augmented Generation (RAG) standardly queries flat text chunks using vector search. **GraphRAG** enriches the context by extracting the localized graph neighborhood (related entities, claims, and event nodes) from a Graph DB, joining them into a cohesive narrative prompt for the LLM.

#### Q8: How did you implement CORS configuration?
> **Answer**: I registered a global CORS filter bean in Spring Security mapping `/` origins, and added CORS middleware in FastAPI to allow cross-service communication during client browser requests.

#### Q9: What is the benefit of index-free adjacency in Neo4j?
> **Answer**: In SQL, querying relationships requires scanning index tables (joins). Neo4j nodes hold direct pointers to their adjacent neighbors. The time to traverse a relationship is constant, independent of the total size of the database graph.

#### Q10: How does next.js compile page routing in your application?
> **Answer**: It uses the Next.js App Router. The landing submission page is mapped inside `app/page.tsx` as a static layout, and the detailed bias report is mapped under `app/report/[id]/page.tsx` as a dynamic client page fetching from Spring Boot API endpoints.
