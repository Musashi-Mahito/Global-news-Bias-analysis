from typing import List, Dict, Any
from ai_service.services.llm_service import LLMService

class ReportAgent:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def generate(self, text: str) -> Dict[str, Any]:
        """
        Generate multi-perspective summaries and a chronological event timeline.
        """
        summaries = self.llm.generate_summaries(text)
        timeline = self.llm.generate_timeline(text)
        
        return {
            "multiPerspectiveSummaries": summaries,
            "timeline": timeline
        }
