from pydantic import BaseModel, Field
from typing import List, Optional

# Basic Models
class Entity(BaseModel):
    name: str
    type: str  # Person, Organization, Location, Event, Date
    relevance: float = 0.5

class Claim(BaseModel):
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0

# Request Models
class ArticleRequest(BaseModel):
    url: Optional[str] = None
    text: str

class EmbeddingsRequest(BaseModel):
    text: str

class BiasAnalysisRequest(BaseModel):
    text: str
    source: Optional[str] = None
    related_context: Optional[List[str]] = Field(default_factory=list)

class ConsensusAnalysisRequest(BaseModel):
    article_claims: List[Claim]
    related_claims: List[Claim]

# Response Models
class EntitiesResponse(BaseModel):
    entities: List[Entity]

class ClaimsResponse(BaseModel):
    claims: List[Claim]

class EmbeddingsResponse(BaseModel):
    embedding: List[float]

class BiasAnalysisResponse(BaseModel):
    biasScore: int
    confidence: int
    sentimentBias: int
    framingBias: int
    omissionBias: int
    sentimentExplanation: str
    framingExplanation: str
    omissionExplanation: str
    evidence: List[str]

class DisputedClaim(BaseModel):
    claim: Claim
    contradicting_claim: Claim
    source: str

class ConsensusAnalysisResponse(BaseModel):
    agreementPercent: int
    contradictionPercent: int
    uncertaintyPercent: int
    sharedFacts: List[str]
    disputedClaims: List[DisputedClaim] = Field(default_factory=list)

class TimelineItem(BaseModel):
    time: str
    event: str
    description: str

class MultiPerspectiveSummaries(BaseModel):
    conservative: str
    liberal: str
    neutral: str
    consensus: str

class FullAnalysisResponse(BaseModel):
    title: str
    content: str
    source: str
    publish_date: str
    language: str
    entities: List[Entity]
    claims: List[Claim]
    biasReport: BiasAnalysisResponse
    consensusReport: ConsensusAnalysisResponse
    multiPerspectiveSummaries: MultiPerspectiveSummaries
    timeline: List[TimelineItem]
