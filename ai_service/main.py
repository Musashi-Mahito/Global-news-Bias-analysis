import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional

from ai_service.config import settings
from ai_service.schemas import (
    ArticleRequest, EmbeddingsRequest, BiasAnalysisRequest, ConsensusAnalysisRequest,
    EntitiesResponse, ClaimsResponse, EmbeddingsResponse, BiasAnalysisResponse, ConsensusAnalysisResponse,
    FullAnalysisResponse, Entity, Claim, DisputedClaim
)

from ai_service.services.llm_service import LLMService
from ai_service.services.vector_service import VectorService
from ai_service.services.graph_service import GraphService

from ai_service.agents.extractor_agent import ExtractorAgent
from ai_service.agents.retriever_agent import RetrieverAgent
from ai_service.agents.entity_agent import EntityAgent
from ai_service.agents.claim_agent import ClaimAgent
from ai_service.agents.graph_agent import GraphAgent
from ai_service.agents.bias_agent import BiasAgent
from ai_service.agents.consensus_agent import ConsensusAgent
from ai_service.agents.report_agent import ReportAgent

app = FastAPI(
    title="Global News Bias AI Service",
    description="Microservice exposing NLP agents, graph database sync, and vector embeddings.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate singletons
llm_service = LLMService()
vector_service = VectorService()
graph_service = GraphService()

extractor_agent = ExtractorAgent()
retriever_agent = RetrieverAgent()
entity_agent = EntityAgent(llm_service)
claim_agent = ClaimAgent(llm_service)
graph_agent = GraphAgent(graph_service)
bias_agent = BiasAgent(llm_service)
consensus_agent = ConsensusAgent()
report_agent = ReportAgent(llm_service)

@app.on_event("shutdown")
def shutdown_event():
    graph_service.close()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "provider": settings.LLM_PROVIDER,
        "qdrant_connected": vector_service.client is not None,
        "neo4j_connected": graph_service.driver is not None
    }

@app.post("/extract-entities", response_model=EntitiesResponse)
def api_extract_entities(request: ArticleRequest):
    try:
        entities = entity_agent.extract(request.text)
        # Map list of dicts to list of Entity Pydantic models
        entities_models = [Entity(**e) for e in entities]
        return EntitiesResponse(entities=entities_models)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity extraction failed: {str(e)}")

@app.post("/extract-claims", response_model=ClaimsResponse)
def api_extract_claims(request: ArticleRequest):
    try:
        claims = claim_agent.extract(request.text)
        claims_models = [Claim(**c) for c in claims]
        return ClaimsResponse(claims=claims_models)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Claim extraction failed: {str(e)}")

@app.post("/generate-embeddings", response_model=EmbeddingsResponse)
def api_generate_embeddings(request: EmbeddingsRequest):
    try:
        emb = vector_service.generate_embeddings(request.text)
        return EmbeddingsResponse(embedding=emb)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embeddings generation failed: {str(e)}")

@app.post("/bias-analysis", response_model=BiasAnalysisResponse)
def api_bias_analysis(request: BiasAnalysisRequest):
    try:
        res = bias_agent.analyze(request.text, request.source, request.related_context)
        return BiasAnalysisResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bias analysis failed: {str(e)}")

@app.post("/consensus-analysis", response_model=ConsensusAnalysisResponse)
def api_consensus_analysis(request: ConsensusAnalysisRequest):
    try:
        article_claims_dict = [c.dict() for c in request.article_claims]
        related_claims_dict = [c.dict() for c in request.related_claims]
        
        res = consensus_agent.analyze(article_claims_dict, related_claims_dict)
        
        # Format response
        disputed = []
        for d in res.get("disputedClaims", []):
            disputed.append(
                DisputedClaim(
                    claim=Claim(**d["claim"]),
                    contradicting_claim=Claim(**d["contradicting_claim"]),
                    source=d["source"]
                )
            )
            
        return ConsensusAnalysisResponse(
            agreementPercent=res["agreementPercent"],
            contradictionPercent=res["contradictionPercent"],
            uncertaintyPercent=res["uncertaintyPercent"],
            sharedFacts=res["sharedFacts"],
            disputedClaims=disputed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Consensus analysis failed: {str(e)}")

@app.post("/analyze", response_model=FullAnalysisResponse)
def api_analyze(request: ArticleRequest):
    """
    Orchestrate the 8 NLP agents pipeline to ingest, retrieve, index, graph, and analyze news bias.
    """
    try:
        # Generate a stable or random ID for the article
        article_id = str(uuid.uuid4())
        
        # Agent 1: Extract article content and metadata
        extracted = extractor_agent.extract(request.text, request.url)
        title = extracted["title"]
        content = extracted["content"]
        source = extracted["source"]
        pub_date = extracted["publish_date"]
        lang = extracted["language"]
        
        # Agent 2: Retrieve related coverage from news sources
        related_coverages = retriever_agent.retrieve_related_articles(title, content)
        
        # Agent 3: Extract entities (NER)
        entities = entity_agent.extract(content)
        entities_models = [Entity(**e) for e in entities]
        
        # Agent 4: Extract structured claims
        claims = claim_agent.extract(content)
        claims_models = [Claim(**c) for c in claims]
        
        # Agent 5 & Qdrant: Generate embedding and upsert article in Vector DB
        vector_service.upsert_article(
            article_id=article_id,
            text=content,
            metadata={
                "title": title,
                "source": source,
                "publish_date": pub_date,
                "language": lang
            }
        )
        
        # Also upsert related coverages in vector DB for future semantic retrieval
        related_ids = []
        for i, rc in enumerate(related_coverages):
            rc_id = f"{article_id}_related_{i}"
            related_ids.append(rc_id)
            vector_service.upsert_article(
                article_id=rc_id,
                text=rc["content"],
                metadata={
                    "title": rc["title"],
                    "source": rc["source"],
                    "publish_date": rc["publish_date"],
                    "language": rc["language"]
                }
            )
            
        # Agent 8: Report generation (Multi-perspective summaries and timelines)
        report_data = report_agent.generate(content)
        summaries = report_data["multiPerspectiveSummaries"]
        timeline_raw = report_data["timeline"]
        
        # Agent 5 & Neo4j: Sync main article, entities, claims, events and related linkages into graph
        # This will write nodes and relationships to Neo4j.
        graph_agent.build_graph(
            article_id=article_id,
            article_data=extracted,
            entities=entities,
            claims=claims,
            timeline=timeline_raw
        )
        
        # Build related articles nodes in graph & link them
        for i, rc in enumerate(related_coverages):
            rc_id = related_ids[i]
            graph_service.save_article_node(
                article_id=rc_id,
                title=rc["title"],
                source=rc["source"],
                url=rc.get("url", ""),
                publish_date=rc["publish_date"]
            )
        # Link main to related
        graph_agent.link_related_articles(article_id, related_ids)
        
        # Agent 6: Bias Analyzer
        # Context list for bias comparison
        related_texts = [f"Source: {rc['source']}\nTitle: {rc['title']}\nContent: {rc['content']}" for rc in related_coverages]
        bias_res = bias_agent.analyze(content, source, related_texts)
        bias_report = BiasAnalysisResponse(**bias_res)
        
        # Extract related claims to run consensus matching
        # For simplicity, extract claims from the related texts (either mocks or using the claim agent)
        # Let's extract claims from first related article or generate from all
        all_related_claims = []
        for rc in related_coverages[:2]:  # compare top 2 related articles' claims
            rc_claims = claim_agent.extract(rc["content"])
            for rcc in rc_claims:
                rcc["source"] = rc["source"]
                all_related_claims.append(rcc)
                
        # Agent 7: Consensus Analyzer
        claims_dicts = [c.dict() for c in claims_models]
        consensus_res = consensus_agent.analyze(claims_dicts, all_related_claims)
        
        # Parse consensus
        disputed = []
        for d in consensus_res.get("disputedClaims", []):
            disputed.append(
                DisputedClaim(
                    claim=Claim(**d["claim"]),
                    contradicting_claim=Claim(**d["contradicting_claim"]),
                    source=d["source"]
                )
            )
            
        consensus_report = ConsensusAnalysisResponse(
            agreementPercent=consensus_res["agreementPercent"],
            contradictionPercent=consensus_res["contradictionPercent"],
            uncertaintyPercent=consensus_res["uncertaintyPercent"],
            sharedFacts=consensus_res["sharedFacts"],
            disputedClaims=disputed
        )
        
        # Package and return
        return FullAnalysisResponse(
            title=title,
            content=content,
            source=source,
            publish_date=pub_date,
            language=lang,
            entities=entities_models,
            claims=claims_models,
            biasReport=bias_report,
            consensusReport=consensus_report,
            multiPerspectiveSummaries=summaries,
            timeline=timeline_raw
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")

@app.get("/graph/{article_id}")
def api_get_graph(article_id: str):
    try:
        return graph_service.get_article_graph(article_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch graph: {str(e)}")
