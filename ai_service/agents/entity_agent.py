from typing import List, Dict, Any
from ai_service.services.llm_service import LLMService

class EntityAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities from article content.
        """
        return self.llm.extract_entities(text)
