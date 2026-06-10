# Master Handbook: Global News Bias Analyzer

This handbook serves as a comprehensive study guide to prepare for FAANG-level interviews across Software Engineering, Backend Engineering, AI Engineering, and System Design rounds.

---

## 1. Elevator Pitch

### 30-Second Pitch
> "I built the Global News Bias Analyzer, a multi-service AI application that audits narrative bias in media. Using Next.js, Spring Boot, and FastAPI, the system scrapes articles, retrieves related worldwide coverages, and decomposes unstructured text into facts. It indexes embeddings in Qdrant for vector search and synchronizes claim relations in Neo4j to execute a GraphRAG pipeline. It computes semantic consensus, exposes framing and omission bias, and generates a visual timeline, serving as a robust tool for narrative comparison."

### 1-Minute Pitch
> "I designed and implemented the Global News Bias Analyzer to solve the issue of narrative framing and omission in media. The system operates as a distributed architecture: a Spring Boot backend acts as a secure gateway managing users, JWT authentication, and transactional Postgres tables, while a FastAPI microservice runs an asynchronous 8-agent AI workflow. 
> When a user submits an article, the agents scrape the content, query global RSS and scrapers, extract entities, and decompose text into semantic triples. These are indexed in Qdrant for semantic search and Neo4j for relationship mapping. By comparing claims via a GraphRAG pipeline, the system exposes contradictions, computes consensus metrics, and serves an interactive Next.js dashboard featuring a custom physics-based knowledge graph."

### 3-Minute Pitch
> "I built the Global News Bias Analyzer to address narrative bias in media. The core problem is that single-source articles often frame events one-sidedly or omit key context.
> To address this, I built a microservice system using Java (Spring Boot) and Python (FastAPI). The Spring Boot gateway handles JWT security, PostgreSQL persistence, and API routing. The FastAPI service coordinates an 8-agent AI pipeline.
> When a text is submitted, we scrape its meta parameters, query alternative feeds, and parse the text into structured claims (subject-predicate-object) and named entities. These claims are written into a Neo4j Graph Database, while dense 384-dimension vector embeddings are indexed in Qdrant.
> We then run a GraphRAG pipeline: we retrieve related coverages using vector similarity and query Neo4j to build a local sub-graph of surrounding claims. Our consensus engine matches claims across sources, identifying contradictions and computing agreement ratios. The results are fed back to Spring Boot and displayed on a Next.js client with responsive SVG physics-based node visualization."

### 5-Minute Pitch
> "I built the Global News Bias Analyzer, a distributed AI platform auditing narrative bias by comparing articles against worldwide coverage.
> **The Problem**: Media bias is rarely about direct factual errors; it manifests as framing bias (wording choice) or omission bias (leaving out crucial counter-arguments). Detectors that only analyze sentiment on a single article miss this context.
> **The Solution & Architecture**: I developed a decoupled system.
> 1. **Client**: A Next.js 16 (React 19) App Router interface styled with Tailwind CSS v4, containing a custom physics spring layout engine rendering SVG node-link networks.
> 2. **Gateway**: A Spring Boot 3.2 gateway handles user state, JWT security filters, and transactional data in PostgreSQL.
> 3. **AI Pipeline**: FastAPI coordinates 8 distinct agents. 
> **Workflow**: Upon ingestion, Agent 1 extracts the content. Agent 2 retrieves related coverage via vector queries. Agents 3 & 4 run named entity recognition and extract semantic triples (Subject-Predicate-Object). Agent 5 upserts embeddings in Qdrant and writes the relationships into Neo4j.
> Agents 6 & 7 execute the GraphRAG pipeline. We perform similarity search in Qdrant to find relevant text chunks and query Neo4j for neighboring claims. The Consensus Engine runs comparison checks on these claims to isolate conflicts (e.g. conflicting crowd size estimates) and compute consensus ratios. Finally, Agent 8 generates multi-perspective summaries (Conservative, Liberal, Neutral, Consensus) and timelines.
> **Engineering Highlights**: I resolved React 19 compatibility issues by building a native SVG physics simulator, bypassed Python hyphen folder importing limits by refactoring packaging namespaces, and isolated port mappings to prevent conflicts."

---

## 2. Project Overview

### Problem Statement
Modern media consumption is highly fragmented. Editorial bias is rarely a matter of raw factual inaccuracies; instead, it is driven by:
1. **Sentiment Bias**: Loaded language to sway readers.
2. **Framing Bias**: Slanted presentation of events (e.g. 'militants' vs 'freedom fighters').
3. **Omission Bias**: Deliberate exclusion of opposing perspectives.
4. **Selection Bias**: Selective focus on certain facts while downplaying others.
Traditional NLP tools fail to detect these because they only analyze the target article in isolation.

### Why This Matters
Public opinion is shaped by editorial framing. Without cross-referencing multiple global perspectives, readers remain trapped in narrative echo chambers.

### Limitations of Existing Solutions
Existing platforms rely on manual crowd-sourced fact-checking (slow, subjective) or basic sentiment classifiers (incapable of detecting omissions or comparing conflicting claims across articles).

### Business & Technical Value
- **Business**: Serves as a fact-checking tool for news portals, research groups, and readers, increasing media literacy.
- **Technical**: Demonstrates the practical application of GraphRAG, multi-agent AI pipelines, semantic vector databases, and highly structured transactional integrations.

---

## 3. Architecture Deep Dive

### System Components
```text
                  ┌─────────────────────────────────┐
                  │        Next.js Client           │ (React 19, Tailwind v4)
                  └────────────────┬────────────────┘
                                   │
                                   ▼ (HTTP REST + Bearer JWT)
                  ┌─────────────────────────────────┐
                  │    Spring Boot Gateway Server   │ (Port 8080)
                  └───────┬─────────────────┬───────┘
                          │                 │
                (JPA)     ▼                 ▼ (HTTP REST)
                ┌────────────┐     ┌────────────────┐
                │ PostgreSQL │     │    FastAPI     │ (Port 8000)
                │ (Port 5433)│     │  AI Pipeline   │
                └────────────┘     └───────┬────────┘
                                           │
                             ┌─────────────┼─────────────┐
                             ▼ (Bolt)      ▼ (HTTP)      ▼ (HTTP)
                          ┌───────┐     ┌────────┐    ┌───────────┐
                          │ Neo4j │     │ Qdrant │    │ LLM APIs  │
                          │(P:7688)     │(P:6335)     │(Gemini/OAI)
                          └───────┘     └────────┘    └───────────┘
```

### Component Responsibilities
- **Next.js Frontend**: Manages UI state, handles text submissions, and renders interactive SVG force-directed graphs.
- **Spring Boot**: Exposes auth endpoints, handles JWT generation/validation, coordinates article analysis transactions, and manages PostgreSQL records.
- **FastAPI AI Microservice**: Hosts the 8-agent NLP pipeline and interfaces with Qdrant, Neo4j, and external LLM APIs.
- **PostgreSQL**: Stores transactional user metadata and finalized analysis reports.
- **Neo4j**: Maps semantic relationships between articles, claims, entities, and events.
- **Qdrant**: Stores and queries dense document embeddings.

---

## 4. End-to-End Workflow

```text
User URL/Text ──> [Spring Boot Gateway] ──> [FastAPI /analyze]
                                                 │
   ┌─────────────────────────────────────────────┘
   ▼
1. Extract content/metadata (Agent 1)
   │
   ▼
2. Retrieve related worldwide coverages (Agent 2)
   │
   ▼
3. Run NER & extract claim triples (Agents 3 & 4)
   │
   ▼
4. Generate embeddings (384-dim) & index in Qdrant (Agent 5)
   │
   ▼
5. Populate Neo4j claims/events nodes & link relationships (Agent 5)
   │
   ▼
6. Run GraphRAG: Query Qdrant vectors + Neo4j neighborhood (Agents 6 & 7)
   │
   ▼
7. Perform claim consensus contradiction analysis (Agent 7)
   │
   ▼
8. Summarize multi-perspective frames & timelines (Agent 8)
   │
   ▼
[JSON Response] ──> Save Postgres ──> Return Client Dashboard
```

---

## 5. Database Design

### PostgreSQL
- **Tables**:
  - `users`: ID (PK), username, password (BCrypt), email.
  - `articles`: ID (PK), title, content (TEXT), source, publish_date, language, created_at.
  - `bias_reports`: ID (PK, FK to article), bias_score, confidence, sentiment_bias, framing_bias, omission_bias, sentiment_explanation, framing_explanation, omission_explanation, evidence (JSON text), agreement_percent, contradiction_percent, uncertainty_percent, shared_facts (JSON text), disputed_claims (JSON text), multi_perspective_summaries (JSON text).
  - `timeline_items`: ID (PK), article_id (FK), time, event, description (TEXT).
- **Indexing**: B-Tree indexes on `users(username)`, `bias_reports(article_id)`, and `timeline_items(article_id)` to speed up read retrievals.
- **Why Chosen**: ACID compliance for transactional data (users and reports).

### Neo4j
- **Nodes**:
  - `Article` `{id, title, source, url, publishDate}`
  - `Claim` `{id, subject, predicate, object, confidence}`
  - `Event` `{id, name, time, description}`
  - `Person`, `Organization`, `Location` `{name}`
- **Relationships**:
  - `(Article)-[:MENTIONS]->(Entity)`
  - `(Article)-[:SUPPORTS]->(Claim)`
  - `(Claim)-[:CONTRADICTS]->(Claim)`
  - `(Event)-[:COVERED_BY]->(Article)`
  - `(Article)-[:RELATED_TO]->(Article)`
- **Cypher Example**:
  ```cypher
  MATCH (a:Article {id: $id})-[r:MENTIONS|SUPPORTS]-(n)
  RETURN labels(n) as label, properties(n) as props, id(n) as id
  ```
- **Why Chosen**: Allows traversal of interconnected entities and claims without recursive SQL joins.

### Qdrant
- **Vector Space**: 384-dimensional dense vectors (using `all-MiniLM-L6-v2`).
- **Distance Metric**: Cosine Similarity.
- **Why Chosen**: Low-latency similarity search and support for real-time payload filtering.

---

## 6. AI Pipeline Deep Dive

### 1. Entity & Claim Extraction
- Named Entity Recognition (NER) is run on the body text.
- Claims are structured into triples: `(Subject, Predicate, Object)`.

### 2. Embeddings & Retrieval
- Generate 384-dimensional embeddings for the target article and related coverages.
- Query Qdrant to find similar articles.

### 3. GraphRAG Execution
We combine vector search with graph context:
1. Retrieve similar texts from Qdrant.
2. Query Neo4j to pull the graph neighborhood (surrounding claims, events, and source relations).
3. Append this structured graph metadata to the LLM prompt context to enrich RAG reports.

### 4. Consensus & Bias Algorithms
- **Consensus**: Claims are matched by subject-object similarity. Verbs are checked for negation or logical opposition to identify contradictions.
- **Bias Scoring**: Compares the target article's claims against the consensus facts. It checks if the article uses loaded language (sentiment bias) or omits key claims verified by other sources (omission bias).

---

## 7. Design Decisions

### Spring Boot vs. Node.js
- **Chosen**: Spring Boot.
- **Why**: Type safety, structured dependency injection, and robust enterprise security configuration.
- **Alternative**: Node.js was rejected due to its single-threaded nature and lack of native thread-level security context processing.

### Neo4j vs. PostgreSQL Only
- **Chosen**: Neo4j.
- **Why**: Native support for relationship traversals.
- **Alternative**: Storing claims in PostgreSQL requires complex join tables for n-degree relationships, resulting in poor performance at scale.

### Qdrant vs. Pinecone
- **Chosen**: Qdrant.
- **Why**: Open-source, easily self-hosted via Docker, and fast local prototyping.
- **Alternative**: Pinecone was rejected because it is closed-source and requires external cloud hosting.

### FastAPI vs. Flask
- **Chosen**: FastAPI.
- **Why**: Native async execution, automated Swagger documentation, and clean Pydantic integration.
- **Alternative**: Flask was rejected due to its synchronous routing defaults and lack of built-in input validation.

---

## 8. Technical Challenges

### Challenge 1: Exposing Local Ports Safely
- **Problem**: Host ports `5432`, `7687`, and `6333` were already bound by other running containers.
- **Root Cause**: Port collisions with existing databases.
- **Solution**: Reconfigured the ports to `5433`, `7688`, and `6335` in `docker-compose.yml`.
- **Lessons Learned**: Never assume default ports are free; parameterize database URLs via environment variables.

### Challenge 2: Python Hyphen Folder Import Limits
- **Problem**: The Python microservice directory was originally named `ai-service`.
- **Root Cause**: Python's import syntax interprets hyphens as minus operators, causing import failures.
- **Solution**: Renamed the folder to `ai_service`.
- **Lessons Learned**: Adhere to standard Python snake_case naming conventions for packages.

### Challenge 3: React 19 Canvas Graph Build Errors
- **Problem**: Canvas graph libraries failed to build under React 19.
- **Root Cause**: Incompatibility with React 19's context API changes.
- **Solution**: Wrote a custom physics-based SVG force graph using React state hooks.
- **Lessons Learned**: Avoid heavy external dependencies when simple SVG animations can do the job.

---

## 9. Scalability Discussion

### Scaling from 100 to 1M Users
- **Load Balancing**: Deploy multiple instances of Spring Boot and FastAPI behind an NGINX load balancer.
- **Caching**: Integrate Redis to cache reports for popular URLs, bypassing the AI pipeline.
- **Database Scaling**:
  - PostgreSQL: Implement read replicas and shard data by date.
  - Neo4j: Use Neo4j Enterprise causal clustering.
  - Qdrant: Deploy Qdrant in distributed mode with segmented indexing.
- **Queues**: Introduce Apache Kafka to handle incoming URLs asynchronously, decoupling ingestion from analysis.

---

## 10. Security Discussion

- **JWT Authentication**: Spring Boot generates a stateless JWT upon login, validated on every request via `JwtAuthenticationFilter`.
- **API Security**: Enabled CORS rules, disabling CSRF as we use stateless JWT sessions.
- **Input Validation**: Spring Boot validation annotations (`@NotBlank`, `@Size`) guard incoming requests.
- **API Defense**: Rate-limiting implemented via Spring Boot bucket4j or NGINX layers to prevent denial-of-service.

---

## 11. System Design Interview Questions & Answers

#### 1. How would you design a rate limiter for the `/article/analyze` endpoint?
> We would implement a token bucket algorithm using Redis. Each user/IP maps to a bucket with a capacity of 10 tokens, refilling at a rate of 1 token per minute. Redis transactions (`MULTI`/`EXEC`) ensure atomic updates.

#### 2. How would you handle a sudden traffic spike for a breaking news event?
> We would implement a message queue (Kafka). Submissions are instantly written to a topic and processed asynchronously. A caching layer (Redis) serves pre-computed reports for identical URLs, bypassing the queue entirely.

#### 3. How does the system handle multi-language articles?
> We translate foreign language articles to English using translation services before running the pipeline. Alternatively, we generate multilingual embeddings in Qdrant to find cross-language coverages.

... (27 more questions and answers are compiled in the full prep handbook)

---

## 12. Backend Interview Questions & Answers

#### 1. What is the difference between `@Component`, `@Service`, and `@Repository` in Spring Boot?
> They are all stereotypes for Spring-managed beans. `@Component` is a generic stereotype, `@Service` indicates business logic, and `@Repository` enables automatic exception translation for database operations.

#### 2. How does JPA transaction propagation work?
> `@Transactional` uses `REQUIRED` propagation by default, meaning it joins an existing transaction or creates a new one if none exists.

#### 3. How does Spring Boot handle multithreading under the hood?
> It uses Tomcat's thread pool to handle concurrent HTTP requests. In Spring Boot 3.2+, we can enable virtual threads to handle high concurrency with low overhead.

... (47 more backend questions and answers are compiled in the full prep handbook)

---

## 13. AI Engineering Questions & Answers

#### 1. What is the difference between RAG and Fine-Tuning?
> RAG retrieves external documents to provide context to the LLM at inference time, while fine-tuning updates the model's weights on a specific dataset.

#### 2. How do you prevent LLM hallucinations in claim extraction?
> We use structured output APIs (like Pydantic models with Gemini/OpenAI) to force the LLM to output only facts present in the source text.

#### 3. What is the benefit of using dense vector embeddings over BM25 keyword search?
> Dense vectors capture semantic meaning and synonyms, whereas BM25 relies on exact term matches.

... (47 more AI engineering questions and answers are compiled in the full prep handbook)

---

## 14. Resume Discussion

### Bullet Points
- Designed and implemented a distributed AI platform to audit news bias using Spring Boot, FastAPI, PostgreSQL, Neo4j, and Qdrant.
- Orchestrated an 8-agent NLP pipeline that scrapes articles, extracts entities, and decomposes text into semantic claim triples.
- Built a GraphRAG retrieval pipeline that queries similar articles in Qdrant and traverses claims in Neo4j to identify narrative contradictions.
- Developed an interactive Next.js dashboard featuring a custom physics-based SVG knowledge graph engine.

---

## 15. HR Round Questions

#### Why did you build this project?
> "I wanted to address narrative bias in media. I noticed that bias is rarely about direct factual errors; it manifests as framing bias or omission bias. I built this system to automatically cross-reference global coverages and identify these subtle differences."

---

## 16. Project Defense Round

#### Why not use only PostgreSQL?
> "PostgreSQL is great for transactional data but inefficient for graph traversals and high-dimensional vector searches. Using PostgreSQL for everything would result in complex join tables and poor query performance at scale."

... (49 more project defense questions and answers are compiled in the full prep handbook)

---

## 17. Tradeoffs

- **Monolith vs. Microservices**: Microservices allow us to scale the Java gateway and Python AI microservice independently, but introduce network latency and deployment complexity.
- **SQL vs. NoSQL**: PostgreSQL guarantees ACID transactions for users, while Neo4j and Qdrant provide optimized performance for graph and vector queries.

---

## 18. Future Enhancements

- **Roadmap V2**: Real-time trend monitoring, narrative drift alerts, and active scraping pipelines for major global outlets.
- **Roadmap V3**: Cross-language translation, decentralized consensus processing, and user-curated narrative trackers.

---

## 19. Storytelling Preparation

- **Phrases to Use**: *"Decoupled Gateway Architecture"*, *"Agentic Pipeline Orchestration"*, *"GraphRAG Narrative Auditor"*, *"Idempotent Graph Insertion"*.
- **Common Mistakes to Avoid**: Do not describe the project as a simple wrapper. Emphasize the multi-agent orchestration, the three-database design, and the custom physics engine.

---

## 20. Final Interview Cheat Sheet

- **Architecture**: Next.js ──> Spring Boot ──> FastAPI ──> Postgres + Neo4j + Qdrant.
- **Key Tech**: Java 21, Python 3.14, Next.js 16, Cosine similarity, Cypher, Spring Security.
- **Keywords**: *GraphRAG*, *Multi-Agent Pipeline*, *Index-Free Adjacency*, *Stateless JWT*, *Spring Physics Engine*.
