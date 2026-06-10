# Learning Path: Mastering the Global News Bias Analyzer

To completely master the architectural patterns, databases, and AI concepts utilized in this project, follow this structured learning path. It spans across backend systems, databases, frontends, and AI engineering.

---

## 📈 Study Map

```text
┌───────────────────────────┐      ┌───────────────────────────┐
│     1. AI & NLP Basic     │ ───> │   2. Database Foundations │
│  (NLP pipelines, Triples)  │      │  (Neo4j Cypher, Vectors)  │
└─────────────┬─────────────┘      └─────────────┬─────────────┘
              │                                  │
              ▼                                  ▼
┌───────────────────────────┐      ┌───────────────────────────┐
│ 3. Microservices Gateway  │ ───> │  4. Advanced GraphRAG &   │
│  (Spring, FastAPI, JWT)   │      │    Multi-Agent Workflows  │
└───────────────────────────┘      └───────────────────────────┘
```

---

## Phase 1: NLP Foundations & Information Extraction
Mastering how unstructured news text is transformed into queryable facts.

### Key Concepts to Learn
- **Named Entity Recognition (NER)**: Identifying categories like Persons, Organizations, and Locations from raw text.
- **Open Information Extraction (OpenIE)**: Extracting semantic triples (`subject-predicate-object`) from unstructured text (e.g., "The bill reduces inflation" -> `("Bill", "reduces", "inflation")`).
- **Text Chunking & Parsing**: Splitting articles by semantics rather than hard character limits.

### Recommended Learning Tasks
1. Write a script using Python's `spaCy` or `NLTK` to extract noun chunks and named entities.
2. Study the JSON Structured Outputs feature of modern LLMs (using Pydantic models). Learn how to force an LLM to output valid JSON representations of facts.

---

## Phase 2: Vector Search & Embeddings (Qdrant)
Understanding semantic retrieval, distance metrics, and vector indexing.

### Key Concepts to Learn
- **Text Embeddings**: How words and paragraphs are mapped to high-dimensional mathematical space (e.g., size 384 or 1536).
- **Distance Metrics**: Cosine Similarity vs. L2 (Euclidean) Distance vs. Dot Product.
- **Indexing & Payload Filters**: Querying similar documents and filtering them on-the-fly using metadata keys (like `language` or `publish_date`).

### Recommended Learning Tasks
1. Read the **Qdrant Vector Database Documentation** on "Collections" and "Points".
2. Deploy a local script that generates vectors using `sentence-transformers` and performs a k-NN similarity search in Qdrant.

---

## Phase 3: Graph Databases & Cypher (Neo4j)
Mastering graph modeling and Cypher, the SQL equivalent for graphs.

### Key Concepts to Learn
- **Property Graph Model**: Understanding Nodes, Labels, Relationships (edges), and Properties.
- **Cypher Query Language**:
  - `MERGE` vs. `CREATE` (for idempotent updates).
  - Graph traversals: finding paths between nodes (e.g. `(a:Article)-[:SUPPORTS]->(c:Claim)<-[:CONTRADICTS]-(c2:Claim)`).
- **APOC Plugins**: Neo4j's Awesome Procedures on Cypher utility library.

### Recommended Learning Tasks
1. Complete the free **Neo4j GraphAcademy** courses (specifically *Neo4j Fundamentals* and *Cypher Fundamentals*).
2. Write Cypher queries to detect "Triangles" of relationships or identify conflicting claims (e.g. claiming different numerical counts for the same event).

---

## Phase 4: Backend Microservice Architectures (Spring Boot & FastAPI)
Building secure, decoupled gateway nodes communicating via HTTP.

### Key Concepts to Learn
- **Java REST & RestTemplate/WebClient**: Coordinating synchronous and asynchronous requests between Spring Boot and Python FastAPI.
- **Spring Security Stateless Filter Chain**:
  - Intercepting HTTP calls to extract JWT Bearer tokens.
  - Allowing guest access for demo routes while guarding writing/history routes.
- **FastAPI Dependency Injection**: Running background tasks, validating schemas using Pydantic, and managing database connections cleanly.

### Recommended Learning Tasks
1. Learn how to configure CORS (Cross-Origin Resource Sharing) properly in both Spring Boot and FastAPI.
2. Implement custom global exception handlers in Spring Boot (`@RestControllerAdvice`) to map FastAPI failure responses into clean client-facing JSON alerts.

---

## Phase 5: RAG & GraphRAG Pipeline Integration
Combining vector retrieval and graph traversals to feed context to AI.

### Key Concepts to Learn
- **Hybrid Search**: Querying PostgreSQL (keywords/SQL), Qdrant (vectors), and Neo4j (graph neighbors) together.
- **Sub-graph Contextual Ingestion**: Extracting a localized graph neighborhood, converting it to text, and appending it to the LLM prompt.
- **Consensus Metrics Algorithms**: Writing comparison formulas (using word similarity or logic checks) to identify factual contradictions between sources.

### Recommended Learning Tasks
1. Read Microsoft's whitepaper on **GraphRAG** (Graph-based Retrieval-Augmented Generation).
2. Learn how to parse claims, match subject/object entities, and detect polar oppositions in predicate verbs (like "increased" vs "decreased").

---

## Phase 6: Modern Interactive Frontends (Next.js & React 19)
Developing beautiful, responsive interfaces with custom physics and transitions.

### Key Concepts to Learn
- **React 19 App Router & Hydration**: Server components vs Client-Side state.
- **Tailwind CSS v4 Modern Theming**: Custom animations, keyframes, CSS variables, grid alignments, and glassmorphism.
- **Spring-Force Physics Layouts**:
  - Coulomb's Law (repelling nodes).
  - Hooke's Law (spring tension between connected edges).
  - Integrating mathematical updates inside React state animation loops (`requestAnimationFrame`).

### Recommended Learning Tasks
1. Master building custom SVGs dynamically in React (binding coordinates `x` and `y` to circle/line elements).
2. Study **Framer Motion** for orchestrating page transition triggers, fades, and scale animations.
