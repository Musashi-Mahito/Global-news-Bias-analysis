# FAANG Study Guide: Global News Bias Analyzer

This handbook contains the full, unabridged preparation guide for your project. Study this document to master every architectural decision, codebase implementation, database design, AI pipeline detail, system trade-off, and scalability concern.

---

## 1. Elevator Pitch

### 30-Second Pitch (The Hook)
> "I built the Global News Bias Analyzer—a distributed AI application that audits narrative bias in news media by cross-referencing coverages worldwide. Built with Next.js, Spring Boot, and FastAPI, it scrapes articles, retrieves related worldwide coverage, and parses paragraphs into structured claims. It indexes text embeddings in Qdrant for semantic search and matches claim relationships in Neo4j using a custom GraphRAG pipeline. It exposes sentiment, framing, and omission biases, displaying them on an interactive dashboard with a physics-based SVG knowledge graph."

### 1-Minute Pitch (The Architecture)
> "I designed the Global News Bias Analyzer to address editorial framing and omission bias. The architecture is split into a Next.js (React 19) client, a Spring Boot gateway, and a FastAPI AI microservice. The Spring Boot backend manages users, JWT security, and PostgreSQL transactions. The FastAPI microservice runs an asynchronous 8-agent AI pipeline. When an article is submitted, we scrape its content, fetch similar coverage via vector queries, and parse the text into structured claims (Subject-Predicate-Object). These are loaded into Neo4j and indexed as 384-dimension vectors in Qdrant. By running GraphRAG, the system identifies contradictions, calculates factual consensus ratios, and serves an interactive dashboard with a custom spring-force node visualization."

### 3-Minute Pitch (The Technical Depth)
> "I built the Global News Bias Analyzer to audit media bias. Most media bias is driven by framing (slanted wording) or omission (exclusion of opposing facts). To detect this, a system must analyze articles in comparison with alternative coverage.
> I built a distributed system to solve this. The frontend is Next.js 16 (React 19), styled with Tailwind CSS v4, containing a custom physics-based SVG node-link graph visualizer. The backend gateway is Spring Boot 3.2, which handles user sign-ups, JWT validation, and article report transactions in PostgreSQL.
> The AI pipeline runs on FastAPI. When an article is ingested, we run an 8-agent workflow:
> - **Agent 1** extracts body text and metadata.
> - **Agent 2** searches related coverages using RSS scrapers and vector similarity.
> - **Agent 3 & 4** perform Named Entity Recognition and extract semantic triples.
> - **Agent 5** indexes vectors in Qdrant and loads relationships into Neo4j.
> - **Agent 6 & 7** perform GraphRAG, querying Qdrant and traversing neighboring claims in Neo4j to enrich the LLM's prompt context. We run a comparison algorithm on these claims to isolate contradictions (e.g., conflicting job loss numbers) and calculate consensus metrics.
> - **Agent 8** generates multi-perspective summaries (Conservative, Liberal, Neutral, Consensus) and event timelines.
> This demonstrates end-to-end integration of Java enterprise gateways, Python AI microservices, transactional SQL databases, graph analytics, and vector search engines."

### 5-Minute Pitch (Deep Dive)
> "I built the Global News Bias Analyzer to audit media bias by cross-referencing news coverages worldwide.
> **The Problem**: Traditional media bias detectors analyze a single article in isolation. However, editorial bias is rarely about direct factual errors; it manifests as framing bias (wording choice) or omission bias (leaving out crucial counter-arguments). 
> **The Solution & Architecture**: I developed a decoupled system.
> 1. **Client**: A Next.js 16 (React 19) App Router interface styled with Tailwind CSS v4, containing a custom physics spring layout engine rendering SVG node-link networks.
> 2. **Gateway**: A Spring Boot 3.2 gateway handles user state, JWT security filters, and transactional data in PostgreSQL.
> 3. **AI Pipeline**: FastAPI coordinates 8 distinct agents. 
> **Workflow**: Upon ingestion, Agent 1 extracts the content. Agent 2 retrieves related coverage via vector queries. Agents 3 & 4 run named entity recognition and extract semantic triples (Subject-Predicate-Object). Agent 5 upserts embeddings in Qdrant and writes the relationships into Neo4j.
> Agents 6 & 7 execute the GraphRAG pipeline. We perform similarity search in Qdrant to find relevant text chunks and query Neo4j for neighboring claims. The Consensus Engine runs comparison checks on these claims to isolate conflicts (e.g. conflicting crowd size estimates) and compute consensus ratios. Finally, Agent 8 generates multi-perspective summaries (Conservative, Liberal, Neutral, Consensus) and timelines.
> **Engineering Challenges**: 
> - **React 19 Compatibility**: Many React canvas graph components fail to compile under React 19 due to context API changes. I solved this by writing a custom physics-based SVG force layout engine in React that uses spring equations and `requestAnimationFrame`.
> - **Python Directory Naming**: Refactored the AI service from `ai-service` to `ai_service` because Python imports do not support hyphens, which caused syntax errors.
> - **Port Conflicts**: Reconfigured host port mappings to `5433` (PostgreSQL), `7688` (Neo4j Bolt), and `6335` (Qdrant) to ensure the project runs seamlessly on environments with existing database instances."

---

## 2. Project Overview

### Problem Statement
Traditional news bias detection tools analyze a single article in isolation. However, media bias is rarely driven by raw factual inaccuracies. Instead, it manifests as:
- **Sentiment Bias**: Using loaded language to sway the reader's emotions.
- **Framing Bias**: Slanted presentation of events (e.g., "Freedom Fighters" vs "Militants").
- **Omission Bias**: Deliberate exclusion of opposing perspectives.
- **Selection Bias**: Selective focus on certain facts while ignoring others.

### Why It Matters
Public opinion is shaped by editorial framing. Without cross-referencing multiple global perspectives, readers remain trapped in narrative echo chambers.

### Existing Solutions & Limitations
Existing platforms rely on manual crowd-sourced fact-checking (slow and subjective) or basic sentiment classifiers (incapable of detecting omissions or comparing conflicting claims across articles).

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

#### Q1. How would you design a rate limiter for the `/article/analyze` endpoint?
> **Answer**: I would implement a Token Bucket algorithm using Redis. Each user/IP maps to a Redis key containing the token count and the last update timestamp. When a request arrives, we calculate token replenishment based on the elapsed time, decrement a token, and update the key. Redis transactions (`MULTI`/`EXEC`) or Lua scripting prevent race conditions.

#### Q2. How would you handle a sudden traffic spike for a breaking news event?
> **Answer**: I would implement an asynchronous message queue using Apache Kafka. Instead of processing the analysis synchronously, the Spring Boot gateway writes the ingestion request to a Kafka topic and returns an execution ID. A pool of FastAPI consumer instances processes tasks from the topic. Meanwhile, a caching layer (Redis) serves pre-computed reports for identical URLs.

#### Q3. How does the system handle multi-language articles?
> **Answer**: We use translation services to translate foreign articles to English before running the extraction agents, or we utilize multilingual embeddings (e.g., `multilingual-e5-large`) in Qdrant. This maps different language representations of the same fact to the same vector space, enabling cross-lingual related news retrieval.

#### Q4. How do you scale Neo4j to handle millions of relationships?
> **Answer**: I would use Neo4j's Causal Clustering architecture. This separates write-intensive Core Servers (handling consensus via Raft) from read-intensive Read Replicas. Additionally, we would apply graph partitioning, indexing key properties (like `Article.id` and `Claim.subject`), and optimize memory allocation parameters (`dbms.memory.heap.initial_size` and `dbms.memory.pagecache.size`).

#### Q5. How would you design a distributed tracing system for this project?
> **Answer**: I would integrate Spring Cloud Sleuth/Micrometer Tracing in the Java backend and OpenTelemetry in Python. When an HTTP request enters the gateway, a unique `Trace ID` is generated and injected into the headers (`X-B3-TraceId`). This ID is propagated during REST calls to the FastAPI microservice. Trace spans are exported to a central collector (Zipkin or Jaeger) for visualization.

#### Q6. What is the database sharding strategy for PostgreSQL?
> **Answer**: We would shard by `articleId` (using a consistent hashing function) or partition tables by date range (e.g., monthly). This keeps table sizes manageable and ensures queries for recent news remain fast.

#### Q7. How would you design the vector index configuration in Qdrant for fast search?
> **Answer**: I would configure HNSW (Hierarchical Navigable Small World) indexing parameters. Setting `m` (max edges per node) to 16 and `ef_construct` (construction search depth) to 200 balances build speed and search recall. I would also use scalar quantization (converting float32 vectors to int8) to reduce memory consumption by 4x.

#### Q8. How do you implement data durability and backup in Qdrant?
> **Answer**: I would schedule regular snapshots using Qdrant's snapshot API, which produces a tarball of the collection storage. These snapshots are backed up to S3. For active replication, we run Qdrant in distributed mode with a replication factor of 2.

#### Q9. How do you handle schema changes in Neo4j?
> **Answer**: Neo4j is schema-lite, but we must manage constraints and property structures. We write database migration scripts using tools like Neo4j Migrations, ensuring that unique constraints (e.g., `CONSTRAINT FOR (a:Article) REQUIRE a.id IS UNIQUE`) are created before bulk import.

#### Q10. How would you design a circuit breaker for the AI pipeline?
> **Answer**: I would use Spring Cloud Circuit Breaker (Resilience4j) on the Spring Boot gateway. If the FastAPI service encounters high latency or throws 5xx errors, the circuit opens, and calls fallback to a mock response generator or returns a queued status code.

#### Q11. How would you design the system to handle real-time streaming of news feeds (e.g., RSS, Twitter)?
> **Answer**: I would run a consumer service utilizing Spring Integration or PySpark streaming. It connects to RSS endpoints, filters out irrelevant content, and writes target articles to a Kafka topic. Workers pick up these articles, check if they are already in the database, and trigger the analysis pipeline.

#### Q12. How do you resolve database write conflicts when multiple agents update the same Neo4j node?
> **Answer**: I would use Cypher's `MERGE` statement with transaction locks. By matching the unique identifier first, Neo4j applies a write lock on that node. In Python, we wrap graph updates in transaction retries to handle deadlocks gracefully.

#### Q13. How would you design a caching strategy for vector embeddings?
> **Answer**: Since text embeddings are deterministic, we cache them in Redis using a SHA-256 hash of the input text as the key. When an agent requests an embedding, it checks Redis first, avoiding redundant API calls to OpenAI or local CPU execution.

#### Q14. How would you handle hot partitions in PostgreSQL?
> **Answer**: If a specific news event triggers a spike in reads, we cache the resulting `BiasReport` in Redis with an expiration time (TTL) of 10 minutes. This offloads read traffic from PostgreSQL.

#### Q15. How do you ensure high availability for Neo4j?
> **Answer**: We run a Neo4j cluster with at least 3 Core nodes. The cluster uses the Raft protocol to elect a leader. If the leader fails, a new leader is elected automatically, ensuring write availability.

#### Q16. How would you design a deployment strategy for this microservice system?
> **Answer**: I would use Kubernetes (EKS/GKE). Each service (Spring Boot, FastAPI) is deployed as a Deployment with horizontal pod autoscaling (HPA) triggered by CPU/Memory utilization. We deploy PostgreSQL, Neo4j, and Qdrant using StatefulSets with persistent volumes.

#### Q17. How do you monitor the health of the FastAPI service?
> **Answer**: I expose a `/health` endpoint in FastAPI that checks database connectivity (Neo4j and Qdrant). I configure Prometheus to scrape this endpoint and display health metrics on a Grafana dashboard.

#### Q18. How do you handle data privacy regulations (e.g., GDPR) in this system?
> **Answer**: Users can request deletion of their account and historical report history. When a user is deleted, we run a cascading delete in PostgreSQL to remove their profile and association keys. Transaction logs are scrubbed according to compliance timelines.

#### Q19. How do you handle network latency between Spring Boot and FastAPI?
> **Answer**: We deploy both services in the same VPC and private subnets, enabling HTTP/2 or gRPC communication to reduce serialization overhead and connection latency.

#### Q20. How would you design the search logic to support both vector and keyword queries?
> **Answer**: I would implement **Reciprocal Rank Fusion (RRF)**. We run a vector search in Qdrant and a keyword search (e.g., via PostgreSQL full-text search). We then combine the ranked results using the RRF algorithm:
> $$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
> where $r_m(d)$ is the rank of document $d$ in system $m$, and $k$ is a constant (usually 60). This balances semantic matches with exact keyword searches.

#### Q21. How do you prevent SQL injection in Spring Boot?
> **Answer**: We use Spring Data JPA repositories, which use prepared statements and parameter binding by default.

#### Q22. How do you prevent Cypher injection in FastAPI?
> **Answer**: We pass query parameters as a dictionary to the Neo4j driver session run method, rather than using string concatenation to construct Cypher statements.

#### Q23. How would you design the vector index for real-time indexing?
> **Answer**: Qdrant maintains an in-memory index for new points and builds the HNSW index asynchronously in the background. This allows immediate read/write access while maintaining search performance.

#### Q24. How do you scale the entity extraction agent under heavy load?
> **Answer**: I would deploy the entity extraction agent as a serverless function (AWS Lambda or Google Cloud Functions) with automatic scaling.

#### Q25. How do you handle API payload size limits?
> **Answer**: We configure the gateway and FastAPI to accept maximum payloads (e.g., 2MB) and compress requests using gzip when sending large news articles.

#### Q26. How do you handle database connection pooling in Spring Boot?
> **Answer**: We use HikariCP (the default connection pool in Spring Boot). We configure properties like `maximum-pool-size` (e.g., 20) and `idle-timeout` to balance connection reuse and resource conservation.

#### Q27. How do you manage database connection pooling in FastAPI?
> **Answer**: We initialize the Neo4j driver as a singleton on startup and close it on shutdown. The driver manages its own connection pool internally.

#### Q28. How would you design a feedback loop to improve bias scores?
> **Answer**: We allow users to flag incorrect reports and submit corrections. These flags are saved in PostgreSQL. We can periodically retrain or fine-tune our classifiers using this feedback.

#### Q29. How do you handle schema evolution in Qdrant?
> **Answer**: Qdrant is schema-less. If we need to store new metadata fields, we simply add them to the payload dictionary when upserting points.

#### Q30. How would you design a multi-tenant version of this platform?
> **Answer**: I would use a soft multi-tenancy model. Every table in PostgreSQL, node in Neo4j, and point in Qdrant would include a `tenantId` property. All queries must filter by `tenantId` to ensure data isolation.

---

## 12. Backend Interview Questions & Answers

#### Q1. What is the Spring IoC Container and Dependency Injection?
> **Answer**: The IoC (Inversion of Control) container manages the lifecycle and configuration of application objects (Beans). Instead of classes instantiating their dependencies, the container injects them at runtime (Dependency Injection) via constructor, setter, or field injection.

#### Q2. Explain the difference between `@Autowire` and `@Resource`.
> **Answer**: `@Autowired` resolves dependencies by type by default. `@Resource` resolves dependencies by name first, falling back to type if no match is found.

#### Q3. What is Bean Scope in Spring?
> **Answer**: Spring supports several scopes: `singleton` (one instance per container, default), `prototype` (new instance every time requested), `request` (one instance per HTTP request), `session` (one instance per HTTP session), and `application` (one instance per ServletContext lifecycle).

#### Q4. What is the difference between `@Controller` and `@RestController`?
> **Answer**: `@Controller` is used to serve web views, returning templates (HTML). `@RestController` combines `@Controller` and `@ResponseBody`, returning serialized data (JSON/XML) directly in the HTTP response body.

#### Q5. How does Spring Boot auto-configuration work?
> **Answer**: It looks for libraries on the classpath and automatically registers corresponding beans based on conditional annotations like `@ConditionalOnClass` and `@ConditionalOnMissingBean` defined in `spring.factories`.

#### Q6. What is the purpose of Spring Boot Starters?
> **Answer**: They are dependency descriptors that bundle related libraries (e.g., `spring-boot-starter-web` includes Tomcat, Jackson, and Spring MVC), simplifying build configurations.

#### Q7. Explain Spring Data JPA under the hood.
> **Answer**: It uses proxy classes to implement repository interfaces at runtime. It translates method names (e.g., `findByEmail`) into JPQL queries using query creation heuristics.

#### Q8. What is Lazy Loading in Hibernate and how do you prevent the N+1 select problem?
> **Answer**: Lazy loading defers fetching related entities until they are accessed. The N+1 query problem occurs when fetching a list of $N$ parents triggers $N$ separate queries to fetch their children. We prevent this by using `JOIN FETCH` queries, EntityGraphs, or `@BatchSize` annotations.

#### Q9. What is the difference between Optimistic and Pessimistic Locking?
> **Answer**: Optimistic locking uses a version field (`@Version`) to check for concurrent modifications on commit, throwing an exception if a conflict occurs. Pessimistic locking locks the database row directly (`SELECT ... FOR UPDATE`), blocking other transactions until the lock is released.

#### Q10. What is Database Normalization and when would you denormalize?
> **Answer**: Normalization organizes tables to reduce redundancy and dependency (up to 3NF). We denormalize (introducing redundant data) to optimize read performance for heavy reporting queries, reducing the need for expensive joins.

#### Q11. Explain Transaction Isolation Levels.
> **Answer**: Standard isolation levels are: `READ_UNCOMMITTED` (allows dirty reads), `READ_COMMITTED` (prevents dirty reads, default for most DBs), `REPEATABLE_READ` (prevents non-repeatable reads), and `SERIALIZABLE` (prevents phantom reads, executes transactions sequentially).

#### Q12. Explain Transaction Propagation in Spring.
> **Answer**: Key propagation types are: `REQUIRED` (joins existing or creates new), `REQUIRES_NEW` (always creates a new transaction, suspending existing), `MANDATORY` (must run within an active transaction, otherwise throws exception), and `SUPPORTS` (runs within transaction if exists, otherwise non-transactional).

#### Q13. How does Spring Boot Security handle password encryption?
> **Answer**: It uses a `PasswordEncoder` bean (typically `BCryptPasswordEncoder`). BCrypt incorporates a random salt and a work factor parameter to resist brute-force attacks.

#### Q14. What is the difference between Authentication and Authorization?
> **Answer**: Authentication verifies who a user is (e.g., credentials check). Authorization determines what permissions the authenticated user has (e.g., accessing specific endpoints).

#### Q15. How does JWT prevent tampering?
> **Answer**: A JWT consists of a Header, Payload, and Signature. The signature is created by hashing the header and payload with a secret key. If a user modifies the payload, the signature verification fails on the server.

#### Q16. Why is stateless session management preferred in microservices?
> **Answer**: It allows microservice instances to scale horizontally, as they do not need to share session states.

#### Q17. How do you implement global exception handling in Spring Boot?
> **Answer**: By creating a class annotated with `@ControllerAdvice` or `@RestControllerAdvice` and defining methods with `@ExceptionHandler` to catch and format specific exceptions.

#### Q18. What is the difference between a Filter and an Interceptor in Spring?
> **Answer**: Filters are part of the Servlet container and intercept requests before they reach the DispatcherServlet. Interceptors are part of the Spring MVC context, executing between the DispatcherServlet and the Controller.

#### Q19. What is CORS and how do you solve CORS issues in Spring Boot?
> **Answer**: Cross-Origin Resource Sharing (CORS) is a browser security mechanism that restricts cross-origin HTTP requests. We configure it in Spring Boot by registering a `CorsFilter` bean or using the `@CrossOrigin` annotation on controllers.

#### Q20. What is Spring Boot Actuator?
> **Answer**: It is a sub-project that exposes built-in endpoints (like `/health`, `/metrics`, `/info`) to monitor application health and performance.

#### Q21. Explain the difference between synchronous and asynchronous REST calls.
> **Answer**: Synchronous calls block the executing thread until a response is received. Asynchronous calls return immediately, handling the response via callbacks, Futures, or reactive streams (`Mono`/`Flux`).

#### Q22. What is HikariCP?
> **Answer**: It is a high-performance JDBC connection pool library used as the default in Spring Boot 2.x and 3.x.

#### Q23. What is the N+1 query issue in JPA and how do you detect it?
> **Answer**: It occurs when loading an entity with lazy relationships triggers additional queries to load those relations. We detect it by enabling SQL logs or using analysis tools like QuickPerf.

#### Q24. Explain `@Entity` and `@Table` annotations.
> **Answer**: `@Entity` declares that a class is a JPA entity mapped to a database table. `@Table` specifies the table name and schema constraints.

#### Q25. What is the difference between `@Embedded` and `@OneToOne`?
> **Answer**: `@Embedded` stores the embedded class fields in the parent entity's database row. `@OneToOne` maps the relationship to a separate table via a foreign key.

#### Q26. Explain `@Query` in Spring Data JPA.
> **Answer**: It allows declaring custom JPQL or native SQL queries directly on repository methods.

#### Q27. What is flyway or liquibase?
> **Answer**: They are database migration libraries that track and execute SQL schema changes version-by-version.

#### Q28. What is the difference between `Statement` and `PreparedStatement` in JDBC?
> **Answer**: `PreparedStatement` compiles the SQL query once and parameterizes inputs, preventing SQL injection and improving execution speed. `Statement` compiles the query on every execution.

#### Q29. How do you implement a soft delete in Hibernate?
> **Answer**: By adding a boolean flag (e.g., `deleted`) and using `@SQLDelete` to override the delete command, along with `@Where` to filter out deleted rows by default.

#### Q30. Explain Garbage Collection in Java.
> **Answer**: It is an automatic memory management process that identifies and deletes unreferenced objects in the Heap space, freeing up memory.

#### Q31. What is the difference between the JVM, JRE, and JDK?
> **Answer**: The JVM (Java Virtual Machine) executes bytecode. The JRE (Java Runtime Environment) includes the JVM and core libraries. The JDK (Java Development Kit) includes the JRE and development tools (compiler, debugger).

#### Q32. What are Virtual Threads (Project Loom)?
> **Answer**: They are lightweight threads managed by the JVM instead of the operating system. They allow running millions of concurrent threads with minimal memory overhead, optimizing I/O-bound operations.

#### Q33. What is the difference between `HashMap` and `ConcurrentHashMap`?
> **Answer**: `HashMap` is not thread-safe. `ConcurrentHashMap` uses segment locking and lock-free read operations to handle concurrent accesses safely.

#### Q34. How does the Java `CompletableFuture` work?
> **Answer**: It represents a future result of an asynchronous computation, exposing methods like `thenApply` and `thenCompose` to chain async steps.

#### Q35. What is HTTP status code 401 vs 403?
> **Answer**: 401 indicates Unauthorized (the request lacks valid credentials). 403 indicates Forbidden (the server understands the credentials but the user lacks permissions).

#### Q36. What is the difference between PUT and PATCH?
> **Answer**: `PUT` replaces the entire target resource with the request payload. `PATCH` applies partial modifications to the resource.

#### Q37. What is connection leakage and how do you prevent it?
> **Answer**: Connection leakage occurs when database connections are checked out of the pool but never returned. We prevent it by closing resources using try-with-resources blocks.

#### Q38. Explain connection pooling properties: `maxLifetime` and `connectionTimeout`.
> **Answer**: `maxLifetime` is the maximum time a connection can remain in the pool before being retired. `connectionTimeout` is the maximum time the client will wait for a connection from the pool before throwing an exception.

#### Q39. What is Dirty Read, Non-Repeatable Read, and Phantom Read?
> **Answer**: Dirty Read: Reading uncommitted changes. Non-Repeatable Read: Reading different values for the same row within a transaction. Phantom Read: Reading new rows added by another transaction.

#### Q40. Explain the Difference between L1 and L2 Caching in Hibernate.
> **Answer**: L1 cache is session-scoped and enabled by default. L2 cache is SessionFactory-scoped (shared across sessions) and requires explicit configuration.

#### Q41. How does Jackson serialize Java objects to JSON?
> **Answer**: It uses reflection to read getter methods and class properties, writing them to a JSON stream.

#### Q42. Explain `@Valid` and `@Validated` annotations.
> **Answer**: `@Valid` triggers validation on method parameters and nested properties. `@Validated` is a Spring-specific annotation that enables validation groups and method-level validation.

#### Q43. What is the difference between `Map` and `FlatMap` in reactive programming?
> **Answer**: `Map` transforms each element in a stream. `FlatMap` transforms elements into asynchronous streams, flattening them into a single stream.

#### Q44. What is the CAP Theorem?
> **Answer**: The CAP theorem states that a distributed system can guarantee at most two of the three properties: Consistency, Availability, and Partition Tolerance.

#### Q45. Explain OAuth2 vs JWT.
> **Answer**: OAuth2 is an authorization framework defining token delegation flows. JWT is a token format used to transmit claims securely between parties.

#### Q46. What is a Thread Dump and how do you analyze it?
> **Answer**: A thread dump is a snapshot of all active threads in a JVM, showing their stack traces and lock states. We analyze it to debug deadlocks and CPU spikes.

#### Q47. Explain the differences between SQL and NoSQL.
> **Answer**: SQL databases are relational, table-based, and enforce schemas. NoSQL databases are non-relational and can be document, key-value, graph, or wide-column based.

#### Q48. What is connection pool sizing rule of thumb?
> **Answer**: The standard formula is:
> $$\text{Connections} = (\text{Core Count} \times 2) + \text{Disk Count}$$
> Having too many connections leads to thread context switching overhead.

#### Q49. What is `@JsonIgnore` used for?
> **Answer**: It prevents annotated fields from being serialized to JSON (e.g., hiding password hashes).

#### Q50. How does Tomcat serve HTTP requests concurrently?
> **Answer**: Tomcat maintains a thread pool. When an HTTP request arrives, an idle thread is assigned to parse the request, execute the servlet code, and write the response.

---

## 13. AI Engineering Questions & Answers

#### Q1. What is Retrieval-Augmented Generation (RAG)?
> **Answer**: RAG is a pattern where an LLM's prompt is enriched with context retrieved from an external data source (like a vector or graph database) at inference time. This allows the model to answer queries using up-to-date, domain-specific data without retraining.

#### Q2. Explain the difference between Vector Search and Graph Search.
> **Answer**: Vector search uses mathematical distance (e.g., Cosine) to find semantically similar text chunks. Graph search traverses relationships (edges) between nodes to find contextual connections and hierarchies.

#### Q3. What is GraphRAG and what are its advantages?
> **Answer**: GraphRAG combines vector search with graph traversals. Instead of retrieving isolated text chunks, it extracts related entity nodes, claim triples, and relationship structures. This provides the LLM with structured, multi-dimensional context.

#### Q4. How do you prevent LLM hallucinations during claim extraction?
> **Answer**: We use structured output formats (Pydantic schemas with Gemini/OpenAI API configuration) and add strict instructions in the system prompt, telling the LLM to extract only facts directly present in the text.

#### Q5. What are Embeddings?
> **Answer**: Embeddings are dense, real-valued vectors representing the semantic meaning of text. They are generated by feeding text to neural networks (like BERT).

#### Q6. Explain the Cosine Similarity metric.
> **Answer**: Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space, indicating how close their semantic meanings are:
> $$\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$

#### Q7. What is the difference between Cosine Similarity and Dot Product?
> **Answer**: Dot product is sensitive to vector magnitude. Cosine similarity normalizes the vectors, measuring only the directional alignment.

#### Q8. What is the HNSW algorithm?
> **Answer**: Hierarchical Navigable Small World (HNSW) is a graph-based algorithm for approximate nearest neighbor (ANN) search. It builds a multi-layer graph index for quick vector traversal.

#### Q9. How do you determine the optimal chunk size for RAG?
> **Answer**: We balance retrieval accuracy and context window limits. For news articles, chunk sizes of 256 to 512 tokens with a 10-20% overlap capture paragraph context without splitting sentences.

#### Q10. What is a Vector Database?
> **Answer**: A database optimized for storing, indexing, and querying high-dimensional vector embeddings with low latency.

#### Q11. Explain what a Multi-Agent AI Workflow is.
> **Answer**: It is a design pattern where complex tasks are split among specialized agents. Each agent handles a specific step (e.g., retrieval, extraction, analysis), communicating via structured APIs.

#### Q12. How do you evaluate the quality of a RAG pipeline?
> **Answer**: We use frameworks like **Ragas** or **TruLens** to measure metrics such as **Faithfulness** (is the answer grounded in the retrieved context?), **Answer Relevance**, and **Context Recall**.

#### Q13. What is context window limit and how does it impact RAG?
> **Answer**: The context window is the maximum number of tokens an LLM can process in a single request. If we retrieve too many documents, we hit this limit, requiring selective filtering.

#### Q14. What are System Prompts vs. User Prompts?
> **Answer**: The System Prompt sets the behavior, rules, and constraints of the assistant. The User Prompt contains the specific task or question to process.

#### Q15. How do you handle cold-start issues in vector search?
> **Answer**: By falls back to keyword matching (like TF-IDF or BM25) when vector indexes are empty.

#### Q16. Explain the term "Vector Quantization".
> **Answer**: It is a compression technique that converts 32-bit floating-point numbers in vectors to 8-bit integers, reducing memory usage by 4x at a minor cost to accuracy.

#### Q17. What is an approximate nearest neighbor (ANN) search?
> **Answer**: An ANN search finds points close to a query vector quickly by traversing pre-built index structures, sacrificing absolute precision for search speed.

#### Q18. How do you prevent LLMs from writing code or executing shell scripts when they parse inputs?
> **Answer**: By sanitizing inputs and using structured JSON outputs to prevent prompt injections.

#### Q19. What is temperature parameter in LLMs?
> **Answer**: The temperature parameter controls the randomness of predictions. Lower temperatures (e.g., 0.0) produce deterministic, factual answers. Higher temperatures (e.g., 0.8) increase creativity.

#### Q20. What is Top-P sampling?
> **Answer**: Top-P (nucleus sampling) limits token selection to the smallest set of words whose cumulative probability exceeds the threshold $P$.

#### Q21. Explain the difference between tokenization and embedding.
> **Answer**: Tokenization splits text into tokens (words or sub-words) represented as integers. Embedding maps these integers to multi-dimensional vectors.

#### Q22. What is the role of the system prompt in bias analysis?
> **Answer**: It defines the bias guidelines (e.g., sentiment, framing, omission definitions) and instructs the model to evaluate context objectively.

#### Q23. How do you handle rate limits of third-party LLM APIs?
> **Answer**: We implement exponential backoff with jitter and retry loops.

#### Q24. What are named entities in NLP?
> **Answer**: Real-world objects like people, organizations, locations, and events.

#### Q25. What is the difference between open-source LLMs and closed-source LLMs?
> **Answer**: Open-source models (like Llama) can be self-hosted, ensuring data privacy. Closed-source models (like Gemini/GPT) are accessed via managed APIs, offering higher reasoning capabilities without hosting overhead.

#### Q26. How do you handle long articles that exceed the LLM's context window?
> **Answer**: We split the text into chunks, generate summaries for each chunk, and combine them.

#### Q27. Explain what a Knowledge Graph is.
> **Answer**: A graph representation of data where nodes represent entities and edges represent relationships between them.

#### Q28. What is the APOC library in Neo4j?
> **Answer**: A collection of utility procedures that extend Cypher's functionality (e.g., JSON parsing, graph export).

#### Q29. How do you calculate LLM call latency?
> **Answer**: We track the start and end timestamps of the API request, calculating latency as the elapsed time.

#### Q30. Explain what a prompt template is.
> **Answer**: A pre-defined string template with placeholders replaced with dynamic user data before sending to the LLM.

#### Q31. What is Ragas evaluation framework?
> **Answer**: An open-source tool for evaluating RAG pipelines on metrics like faithfulness and relevance.

#### Q32. How do you prevent hallucinated links in the retrieved output?
> **Answer**: We force the LLM to return only URLs present in the retrieved source documents.

#### Q33. What is the difference between semantic search and keyword search?
> **Answer**: Semantic search understands the query's meaning, while keyword search matches exact character sequences.

#### Q34. How does the Sentence Transformers library work?
> **Answer**: It maps sentences to a dense vector space, placing semantically similar sentences close together.

#### Q35. What is the purpose of HNSW index in Qdrant?
> **Answer**: It enables fast nearest neighbor search on multi-million point collections.

#### Q36. What is fine-tuning?
> **Answer**: Training a pre-trained model on a specific dataset to adapt it for a particular task or domain.

#### Q37. What is semantic search classification?
> **Answer**: Labeling texts based on their semantic meaning rather than metadata tags.

#### Q38. What is the difference between supervised and unsupervised learning?
> **Answer**: Supervised learning trains models on labeled datasets. Unsupervised learning finds hidden patterns in unlabeled datasets.

#### Q39. What is the role of an agent in a multi-agent system?
> **Answer**: An autonomous worker that performs a specific task using tools and structured APIs.

#### Q40. How do you measure the accuracy of named entity extraction?
> **Answer**: We compare extracted entities against a hand-labeled test set, calculating Precision, Recall, and F1 scores.

#### Q41. How does LLM instruction-tuning work?
> **Answer**: Training a base language model on prompt-response pairs to teach it to follow instructions.

#### Q42. Explain what a vector collision is.
> **Answer**: When two semantically different texts are mapped to similar vector coordinates due to model limitations.

#### Q43. What is context retrieval redundancy?
> **Answer**: Retrieving duplicate or highly similar documents in RAG, which increases token costs without adding new information. We prevent this by applying deduplication filters.

#### Q44. How do you handle bias in training datasets for LLMs?
> **Answer**: By auditing datasets for balanced representations and applying safety alignment techniques (like RLHF).

#### Q45. Explain what token compression is.
> **Answer**: Removing redundant words from prompt context to reduce token counts.

#### Q46. What is the difference between extractive and abstractive summarization?
> **Answer**: Extractive summarization pulls key sentences directly from the source text. Abstractive summarization generates new sentences to summarize the text.

#### Q47. What is a claim triple in GraphRAG?
> **Answer**: A structured fact containing a Subject, Predicate, and Object relationship.

#### Q48. What is standard deviation in vector databases?
> **Answer**: It is a metric used to evaluate distance score distributions.

#### Q49. What is prompt injection?
> **Answer**: An attack where malicious user input overrides system instructions, forcing the LLM to execute unintended commands.

#### Q50. Explain RLHF (Reinforcement Learning from Human Feedback).
> **Answer**: A method that uses human feedback to align LLM behaviors with human values and preferences.

---

## 14. Resume Discussion

### Action Verbs
*Designed*, *Implemented*, *Orchestrated*, *Decomposed*, *Synchronized*, *Audited*, *Resolved*, *Developed*, *Mitigated*.

### ATS-Friendly Resume Bullets
- **Distributed Systems & APIs**: Designed and implemented a distributed AI platform in Java Spring Boot and Python FastAPI, reducing coupling through clean microservice APIs.
- **AI Agent Pipelines**: Orchestrated an asynchronous 8-agent AI workflow that scrapes articles, extracts entities, and decomposes unstructured text into semantic triples.
- **GraphRAG Retrieval**: Integrated a GraphRAG retrieval pipeline combining Qdrant vector similarity search and Neo4j relationship traversals to identify narrative contradictions.
- **Frontend Visualization**: Developed an interactive Next.js dashboard featuring a custom physics-based SVG knowledge graph engine.
- **Database Architecture**: Implemented a three-database design using PostgreSQL for transactions, Qdrant for vectors, and Neo4j for graphs.

---

## 15. HR Round Questions

#### Q1. Why did you build this project?
> **Answer**: "I wanted to address narrative bias in media. I noticed that media bias is rarely about direct factual errors; it manifests as framing bias or omission bias. I built this system to cross-reference global coverages and identify these subtle narrative differences."

#### Q2. What was the hardest engineering part of this project?
> **Answer**: "Building the interactive knowledge graph on the client. I originally used third-party canvas libraries, but they had compatibility issues with React 19. I resolved this by writing a custom physics-based SVG force graph using React state hooks."

#### Q3. What would you improve if you had more time?
> **Answer**: "I would replace the HTTP calls between Spring Boot and FastAPI with gRPC to reduce serialization overhead and network latency. I would also integrate Apache Kafka to handle incoming URLs asynchronously."

#### Q4. What would you do differently next time?
> **Answer**: "I would design the system to be event-driven from the start. Using Kafka instead of HTTP REST requests would make the system more resilient to sudden traffic spikes."

---

## 16. Project Defense Round

#### Q1. Why not use only PostgreSQL for everything?
> **Answer**: "PostgreSQL is great for transactional data but inefficient for graph traversals and high-dimensional vector searches. Using PostgreSQL for everything would result in complex join tables and poor query performance at scale."

#### Q2. Is the bias score scientifically valid?
> **Answer**: "The bias score is not an absolute metric. It is a comparative score based on how much the target article's claims deviate from the consensus facts established by other global coverages."

#### Q3. Why not use Elasticsearch instead of Qdrant?
> **Answer**: "Qdrant is optimized specifically for dense vector search and similarity calculations. Elasticsearch is great for keyword search but has higher memory and query latency overhead for pure vector operations."

#### Q4. Why do you need GraphRAG if you already have standard RAG?
> **Answer**: "Standard RAG retrieves isolated text chunks. GraphRAG retrieves structured relationships and claim connections from Neo4j, providing the LLM with richer, multi-dimensional context."

#### Q5. How do you handle translation issues in foreign articles?
> **Answer**: "We translate foreign articles to English using translation APIs before running the extraction agents, or we utilize multilingual embeddings (e.g., `multilingual-e5-large`) in Qdrant."

#### Q6. What happens if the RSS feed scraper is blocked by cloudflare?
> **Answer**: "We configure the scraper to use rotating user agents and proxies, and fall back to public datasets or mock models if the scrape fails."

#### Q7. Is Neo4j Community edition scalable?
> **Answer**: "Neo4j Community edition is single-instance but can handle up to 34 billion nodes and relationships. For enterprise scale, we would upgrade to Neo4j Enterprise causal clustering."

#### Q8. Why did you choose RestTemplate over WebClient in Spring Boot?
> **Answer**: "RestTemplate is simple and sufficient for synchronous requests. If we transition the gateway to reactive programming, we will replace it with WebClient."

#### Q9. How do you prevent database connection pool exhaustion?
> **Answer**: "We set strict connection timeouts, use try-with-resources to close resources, and size our connection pools based on CPU cores."

#### Q10. How do you prevent cross-site scripting (XSS) in the Next.js client?
> **Answer**: "Next.js automatically escapes values rendered in JSX. We also sanitize raw HTML content before displaying it."

#### Q11. Why did you use all-MiniLM-L6-v2 instead of OpenAI text-embedding-3-small?
> **Answer**: "`all-MiniLM-L6-v2` is open-source, runs locally on CPU, and is free, which is ideal for local prototyping. For production, we can switch to OpenAI embeddings by changing the config."

#### Q12. How do you handle schema changes in PostgreSQL?
> **Answer**: "We use database migration tools like Liquibase or Flyway to track schema changes version-by-version."

#### Q13. How does the spring-force physics engine work in Next.js?
> **Answer**: "It runs Coulomb's repulsion and Hooke's spring formulas in an animation loop (`requestAnimationFrame`), updating coordinates in React state."

#### Q14. What is the CPU impact of running Sentence Transformers locally?
> **Answer**: "It is CPU-intensive. For production, we offload embedding generation to a dedicated GPU instance or an external API like OpenAI."

#### Q15. How do you secure database credentials?
> **Answer**: "We store credentials in environment variables or inject them at runtime using Spring Cloud Config or AWS Secrets Manager."

#### Q16. Why did you disable CSRF in Spring Security?
> **Answer**: "CSRF is a session-based vulnerability. Since our Spring Boot backend uses stateless JWT sessions, CSRF protection is disabled."

#### Q17. How do you validate email format in SignupRequest?
> **Answer**: "Using the `@Email` validation annotation on the email field in the DTO class."

#### Q18. What happens if Neo4j is offline?
> **Answer**: "The `GraphService` catches the connection error and falls back to a mock graph structure, allowing the app to remain functional."

#### Q19. What is the impact of Spring Boot's `@Builder` annotation?
> **Answer**: "It implements the Builder pattern, but can cause compilation issues if constructors are missing. I removed Lombok and wrote standard Java builders to prevent compile conflicts."

#### Q20. Why did you use openjdk 25?
> **Answer**: "It is a modern LTS Java release. We compile to Java 21 compatibility, which runs cleanly on JDK 25."

#### Q21. How do you ensure the Postgres DB exists on startup?
> **Answer**: "We configure PostgreSQL initialization parameters in `docker-compose.yml` or use a setup script to create the DB before starting Spring Boot."

#### Q22. How do you handle database index fragmentation in PostgreSQL?
> **Answer**: "By running periodic `REINDEX` commands in PostgreSQL."

#### Q23. Why did you choose Cosine similarity over L2 distance for Qdrant?
> **Answer**: "Cosine similarity measures direction rather than magnitude, which is preferred for comparing the semantic meaning of texts of different lengths."

#### Q24. How do you prevent Docker containers from consuming all host RAM?
> **Answer**: "By setting memory limits (e.g., `mem_limit: 1g`) on each service in `docker-compose.yml`."

#### Q25. What is the thread safety profile of your Python FastAPI code?
> **Answer**: "FastAPI runs async endpoints on an event loop. Non-async tasks are executed in a thread pool managed by AnyIO, ensuring safety."

#### Q26. Why did you separate the frontend and backend instead of Server Side Next.js?
> **Answer**: "To keep our Java gateway decoupled from visual rendering, which allows us to scale the frontend and backend independently."

#### Q27. What is the maximum character limit for URL string?
> **Answer**: "Most browsers limit URLs to 2048 characters. We validate and truncate incoming URLs to prevent database overflow."

#### Q28. How does the user authenticate requests on the Next.js client?
> **Answer**: "The client stores the JWT in `localStorage` or HttpOnly cookies and attaches it as a `Bearer ` token in the `Authorization` header of REST calls."

#### Q29. How do you handle token expiration?
> **Answer**: "We set an expiration time (e.g., 24 hours) in the JWT. The backend rejects expired tokens, forcing the client to re-authenticate."

#### Q30. Why did you choose Uvicorn?
> **Answer**: "Uvicorn is a high-performance ASGI server that is the standard choice for running FastAPI applications."

#### Q31. What happens if the LLM output is not valid JSON?
> **Answer**: "The Pydantic parser catches the validation error, and the agent falls back to a mock JSON payload."

#### Q32. How do you prevent model drift?
> **Answer**: "By using pinned API versions and running regular regression tests on our prompts."

#### Q33. Why did you choose Tailwind CSS v4?
> **Answer**: "Tailwind CSS v4 compiles faster, uses CSS variables instead of JS configuration, and provides modern styling defaults."

#### Q34. How do you handle null values in API responses?
> **Answer**: "By defining fields as `Optional` in Pydantic schemas and configuring Jackson to omit null values in Spring Boot."

#### Q35. How do you implement logging in FastAPI?
> **Answer**: "Using Python's standard `logging` module configured with a standard console handler."

#### Q36. What is the default pool size for HikariCP?
> **Answer**: "10 connections. We adjust it based on traffic requirements."

#### Q37. How do you handle transaction rollbacks in Spring Boot?
> **Answer**: "Spring Boot rolls back transactions automatically if a runtime exception is thrown within a `@Transactional` method."

#### Q38. Why did you choose standard Java getters/setters over Lombok?
> **Answer**: "To ensure compilation reliability under different JVM versions without relying on IDE plugins or specific annotation processors."

#### Q39. How do you handle CORS credentials?
> **Answer**: "By setting `allowCredentials=true` on the backend, allowing the client to send cookies or authorization headers."

#### Q40. Why did you choose 384 dimensions for vectors?
> **Answer**: "384 is the native output dimension of the `all-MiniLM-L6-v2` model, balancing memory usage and retrieval performance."

#### Q41. How does the timeline event sorting work?
> **Answer**: "We sort timeline items chronologically based on their parsed time strings before persisting them."

#### Q42. How do you prevent duplicate claims in Neo4j?
> **Answer**: "By using `MERGE` statements on unique identifiers, ensuring that existing nodes are updated rather than duplicated."

#### Q43. What is the impact of disabling CSRF?
> **Answer**: "It exposes the backend to CSRF attacks if we use cookies. Since we use stateless Bearer tokens in headers, browser-based CSRF is mitigated."

#### Q44. How do you compile Spring Boot test files?
> **Answer**: "Using `mvn test-compile` or `mvn test`."

#### Q45. Why did you choose a microservice design instead of a monolithic design?
> **Answer**: "To isolate CPU-heavy AI operations (FastAPI) from user management (Spring Boot), allowing us to scale them independently."

#### Q46. What happens if a user enters extremely long text in the submit field?
> **Answer**: "The backend validates input lengths, rejecting payloads that exceed limits to prevent memory exhaustion."

#### Q47. How do you optimize Neo4j Cypher query performance?
> **Answer**: "By analyzing queries using the `EXPLAIN` and `PROFILE` keywords to ensure indexes are utilized."

#### Q48. How do you prevent thread starvation in Spring Boot?
> **Answer**: "By sizing the Tomcat thread pool correctly and avoiding blocking operations on request threads."

#### Q49. How do you manage Python packages in production?
> **Answer**: "By pinning dependency versions in `requirements.txt` and using a Docker container for deployment."

#### Q50. Why did you choose RAG over Fine-Tuning?
> **Answer**: "RAG is cheaper, does not require a large training dataset, and allows updating database facts dynamically without retraining."

---

## 17. Tradeoffs

### SQL vs. NoSQL
- **SQL (PostgreSQL)**: Guarantees ACID compliance for transaction safety, but scaling writes requires complex sharding setups.
- **NoSQL (Qdrant & Neo4j)**: Extremely fast for vector and graph queries, but lacks ACID transaction guarantees across databases.

### Graph vs. Relational
- **Graph (Neo4j)**: Traverses multi-degree relationships quickly, but has higher memory overhead than relational databases.
- **Relational (PostgreSQL)**: Highly optimized for tabular data and aggregations, but slow for traversing deep relationship networks.

---

## 18. Future Enhancements

### Roadmap V2
- **gRPC Integration**: Replace REST calls between Spring Boot and FastAPI with gRPC to reduce serialization latency.
- **Message Queue Ingestion**: Introduce Apache Kafka to ingest news URLs asynchronously.

### Roadmap V3
- **Active Scrapers**: Implement rotating scrapers to monitor major global news portals in real-time.
- **Narrative Tracking**: Track how narratives evolve over time using temporal graph modeling in Neo4j.

---

## 19. Storytelling Preparation

### Keywords to Use
- *"Distributed Gateway Pattern"*
- *"Idempotent Graph Insertion"*
- *"Dense Vector Retrieval"*
- *"GraphRAG Narrative Auditor"*
- *"Spring Physics Simulation"*

### Common Mistakes to Avoid
- Don't describe the system as a simple wrapper. Emphasize the multi-agent pipeline orchestration, the three-database design, and the custom physics engine.

---

## 20. Final Interview Cheat Sheet

```text
┌────────────────────────────────────────────────────────┐
│               Global News Bias Analyzer                │
├────────────────────────────────────────────────────────┤
│ Architecture: Next.js ──> Spring Boot ──> FastAPI     │
│               └─> Postgres                └─> Neo4j    │
│                                           └─> Qdrant   │
├────────────────────────────────────────────────────────┤
│ Core Technologies:                                     │
│ - Java 21, Spring Data JPA, Spring Security, JWT       │
│ - Python 3.14, FastAPI, Qdrant Client, Neo4j Bolt      │
│ - Next.js 16, React 19, Tailwind CSS v4, SVG Physics   │
├────────────────────────────────────────────────────────┤
│ Key Concepts:                                          │
│ - GraphRAG: Vector search + Neo4j neighborhood context  │
│ - Consensus matching: claims triples comparison        │
│ - Port isolation: Postgres (5433), Neo4j (7688),       │
│   Qdrant (6335)                                        │
└────────────────────────────────────────────────────────┘
```
