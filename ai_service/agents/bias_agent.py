from typing import List, Dict, Any, Optional
from ai_service.services.llm_service import LLMService

class BiasAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def analyze(self, text: str, source: Optional[str] = None, related_context: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Analyze sentiment, framing, omission, and selection bias.
        """
        return self.llm.analyze_bias(text, source, related_context)
