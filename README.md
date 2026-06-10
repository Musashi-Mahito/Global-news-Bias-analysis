# Global News Bias Analyzer

An AI-powered web application that detects potential bias in news articles by performing narrative comparisons against related global coverage. The platform parses articles, searches similar articles, extracts named entities, structures textual claims, builds knowledge graphs, processes factual consensus, and generates interactive explainable reports.

---

## 🏗️ Architecture

```text
       ┌────────────────────────┐
       │     Next.js Client     │ (TypeScript, Tailwind v4, Framer Motion)
       └───────────┬────────────┘
                   │
                   ▼ (HTTP REST + JWT)
       ┌────────────────────────┐
       │  Spring Boot Gateway   │ (Java 21/25, JPA, Spring Security)
       └─────┬───────────┬──────┘
             │           │
   ┌─────────┘           └─────────┐
   ▼ (JPA)                         ▼ (HTTP REST)
┌────────────┐               ┌────────────┐
│ PostgreSQL │               │  FastAPI   │ (Python 3.14, Agents, NLP)
└────────────┘               └─────┬──────┘
                                   │
                     ┌─────────────┼─────────────┐
                     ▼ (Bolt)      ▼ (HTTP/gRPC) ▼ (HTTP)
                  ┌───────┐     ┌────────┐    ┌───────────┐
                  │ Neo4j │     │ Qdrant │    │ LLM APIs  │
                  └───────┘     └────────┘    └───────────┘
```

---

## ⚡ Core Features

- **Article Extraction**: Scrapes clean body text, publishers, dates, and languages from URLs.
- **Similar News Retrieval**: Queries RSS directories and alternative press feeds to find comparable coverages on similar topics.
- **Named Entity Recognition (NER)**: Identifies key people, organizations, locations, and events.
- **Structured Claims Extraction**: Transforms unstructured prose into semantic `subject-predicate-object` JSON triples.
- **Knowledge Graphs**: Links related articles, claims, events, and entities in Neo4j to query narrative configurations.
- **Semantic Vector Indexes**: Utilizes Qdrant to store and retrieve dense vector embeddings for semantic document search.
- **Narrative Consensus Engine**: Scores factual agreement, contradictions, and uncertainties across sources.
- **Multi-Perspective Summarization**: Generates Tabbed summaries (Liberal, Conservative, Neutral, and Core Consensus facts) side-by-side.
- **Visual Timelines**: Maps chronological occurrences extracted from text.

---

## 📁 Repository Structure

```text
├── docker-compose.yml       # PostgreSQL, Neo4j, and Qdrant container settings
├── ai_service/              # FastAPI Python service
│   ├── main.py              # Exposed ASGI routes & API orchestrator
│   ├── config.py            # Settings and DB connections configurations
│   ├── schemas.py           # Pydantic JSON validation models
│   ├── services/            # LLM, Vector (Qdrant), and Graph (Neo4j) connectors
│   └── agents/              # The 8 narrative analysis pipeline agents
├── backend/                 # Spring Boot Java Gateway
│   ├── pom.xml              # Maven dependencies definitions
│   └── src/main/java/...   # Controllers, JWT security, Jpa Entities & Services
└── frontend/                # Next.js TypeScript client app
    ├── src/app/             # Pages routing (Home and dynamic Reports)
    └── src/components/      # Visual widgets (SVG Spring Graph, Gauges, Timeline)
```

---

## 🚀 How to Run Locally

### 1. Database Containers
Start PostgreSQL, Neo4j, and Qdrant database services:
```bash
docker compose up -d
```
- **PostgreSQL**: `localhost:5433`
- **Neo4j**: `localhost:7475` (HTTP Console), `localhost:7688` (Bolt Connection)
- **Qdrant**: `localhost:6335` (HTTP Console), `localhost:6336` (gRPC Connection)

### 2. FastAPI AI Service
Navigate to the root directory, activate the Python virtual environment, and start the uvicorn server:
```bash
# Activate venv from root directory
source venv/bin/activate

# Start ASGI server
uvicorn ai_service.main:app --host 0.0.0.0 --port 8000 --reload
```
*Note: To run with real LLM processing, configure `GEMINI_API_KEY` or `OPENAI_API_KEY` in your environment. If no keys are set, the application operates in **Mock Mode**, using deterministic regex templates to generate realistic metrics.*

### 3. Spring Boot Gateway
Compile and start the Java backend gateway server:
```bash
cd backend
mvn spring-boot:run
```
Exposes APIs on `http://localhost:8080`.

### 4. Next.js Web App
Start the Next.js development server:
```bash
cd frontend
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to audit reports.

---

## 🛠️ Technology Stack

- **Frontend**: Next.js 16 (App Router), React 19, Tailwind CSS v4, TypeScript, Framer Motion, Lucide Icons.
- **Backend**: Spring Boot 3.2.x, Java 21, Spring Data JPA, Hibernate, Spring Security, JWT (JJWT).
- **AI Microservice**: FastAPI, Python 3.14, Pydantic v2, Qdrant Client, Neo4j Python Driver, Google GenAI SDK, OpenAI SDK, Sentence Transformers.
- **Databases**: PostgreSQL 16 (Relational), Neo4j 5.x (Graph), Qdrant (Vector).
