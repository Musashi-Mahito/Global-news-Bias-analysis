from typing import List, Dict, Any
from ai_service.services.llm_service import LLMService

class ClaimAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        Decompose text into structured claims of format subject-predicate-object.
        """
        return self.llm.extract_claims(text)
