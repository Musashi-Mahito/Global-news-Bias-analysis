import json
import re
import random
from typing import List, Dict, Any, Optional
from ai_service.config import settings

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.gemini_client = None
        self.openai_client = None
        
        if self.provider == "gemini" and settings.GEMINI_API_KEY:
            try:
                from google import genai
                self.gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                print(f"Error initializing Gemini client: {e}. Falling back to Mock.")
                self.provider = "mock"
                
        elif self.provider == "openai" and settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}. Falling back to Mock.")
                self.provider = "mock"

    def _call_gemini(self, prompt: str, schema: Optional[Any] = None) -> str:
        if not self.gemini_client:
            return "{}"
        try:
            # Using google-genai client
            # config parameter can dictate structured JSON outputs if schema is provided
            config = {}
            if schema:
                # google-genai expects response_mime_type and response_schema
                config = {
                    "response_mime_type": "application/json",
                    "response_schema": schema
                }
            
            # Use gemini-2.5-flash as default
            response = self.gemini_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=config
            )
            return response.text
        except Exception as e:
            print(f"Gemini API call failed: {e}. Falling back to Mock.")
            return ""

    def _call_openai(self, prompt: str, response_format_json: bool = False) -> str:
        if not self.openai_client:
            return "{}"
        try:
            messages = [{"role": "user", "content": prompt}]
            response_format = {"type": "json_object"} if response_format_json else None
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                response_format=response_format
            )
            return response.choices[0].message.content or "{}"
        except Exception as e:
            print(f"OpenAI API call failed: {e}. Falling back to Mock.")
            return ""

    def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        if self.provider == "mock" or (self.provider == "gemini" and not self.gemini_client) or (self.provider == "openai" and not self.openai_client):
            return self._mock_entities(text)
            
        prompt = f"""
        Extract the key entities from the following news article. Group them into Categories: Person, Organization, Location, Event, Date.
        For each entity, output: name, type, and relevance (float 0.0 to 1.0).
        Output format must be valid JSON:
        {{
            "entities": [
                {{"name": "Entity Name", "type": "Person|Organization|Location|Event|Date", "relevance": 0.9}}
            ]
        }}
        
        Text:
        {text}
        """
        
        try:
            if self.provider == "gemini":
                # We can specify simple Pydantic schema or fetch text and parse
                res_text = self._call_gemini(prompt)
            else:
                res_text = self._call_openai(prompt, response_format_json=True)
                
            data = json.loads(res_text)
            return data.get("entities", [])
        except Exception as e:
            print(f"Error parsing LLM entities response: {e}")
            return self._mock_entities(text)

    def extract_claims(self, text: str) -> List[Dict[str, Any]]:
        if self.provider == "mock":
            return self._mock_claims(text)
            
        prompt = f"""
        Extract structured claims from the following text. 
        Each claim should be decomposed into a Subject, Predicate, and Object relationship.
        For example: "The protest was attended by 10,000 people" -> {{ "subject": "Protest", "predicate": "attendance", "object": "10,000 people" }}
        Output format must be valid JSON:
        {{
            "claims": [
                {{"subject": "Subject", "predicate": "predicate relationship", "object": "Object", "confidence": 0.95}}
            ]
        }}
        
        Text:
        {text}
        """
        try:
            if self.provider == "gemini":
                res_text = self._call_gemini(prompt)
            else:
                res_text = self._call_openai(prompt, response_format_json=True)
            data = json.loads(res_text)
            return data.get("claims", [])
        except Exception as e:
            print(f"Error parsing LLM claims response: {e}")
            return self._mock_claims(text)

    def analyze_bias(self, text: str, source: Optional[str] = None, related_context: Optional[List[str]] = None) -> Dict[str, Any]:
        if self.provider == "mock":
            return self._mock_bias_analysis(text, source)
            
        context_str = "\n".join([f"- {c}" for c in related_context]) if related_context else "None"
        prompt = f"""
        Perform a news bias analysis on the following article by comparing it to the provided related coverage details.
        Detect:
        1. Sentiment Bias (Emotionally loaded language, tone)
        2. Framing Bias (Wording choices, perspective e.g. "Freedom Fighters" vs "Militants")
        3. Omission Bias (Important details or viewpoints from related context that are missing in the main text)
        4. Selection Bias (Facts emphasized vs facts downplayed)

        Provide:
        - biasScore (0-100, where 0 is neutral/balanced, 100 is highly biased)
        - confidence (0-100 rating of analyzer confidence)
        - sentimentBias (0-100 rating)
        - framingBias (0-100 rating)
        - omissionBias (0-100 rating)
        - sentimentExplanation (Detailed reasoning with evidence)
        - framingExplanation (Detailed reasoning with evidence)
        - omissionExplanation (Detailed reasoning with evidence)
        - evidence (List of text fragments or specific instances showing bias)

        Output format must be valid JSON matching this schema:
        {{
            "biasScore": 45,
            "confidence": 85,
            "sentimentBias": 30,
            "framingBias": 50,
            "omissionBias": 60,
            "sentimentExplanation": "Explanation...",
            "framingExplanation": "Explanation...",
            "omissionExplanation": "Explanation...",
            "evidence": ["quote 1", "quote 2"]
        }}

        Article:
        {text}

        Source: {source or 'Unknown'}

        Related Coverage Details:
        {context_str}
        """
        try:
            if self.provider == "gemini":
                res_text = self._call_gemini(prompt)
            else:
                res_text = self._call_openai(prompt, response_format_json=True)
            return json.loads(res_text)
        except Exception as e:
            print(f"Error parsing LLM bias analysis response: {e}")
            return self._mock_bias_analysis(text, source)

    def generate_summaries(self, text: str) -> Dict[str, str]:
        if self.provider == "mock":
            return self._mock_summaries(text)
            
        prompt = f"""
        Generate four summaries of the following news article:
        1. Conservative View: Focus on arguments, priorities, and phrasing common in conservative outlets.
        2. Liberal View: Focus on arguments, priorities, and phrasing common in liberal outlets.
        3. Neutral View: An objective, balanced, and fact-focused summary.
        4. Consensus Summary: Highlights only the facts agreed upon across all common coverages.

        Output format must be valid JSON:
        {{
            "conservative": "...",
            "liberal": "...",
            "neutral": "...",
            "consensus": "..."
        }}

        Text:
        {text}
        """
        try:
            if self.provider == "gemini":
                res_text = self._call_gemini(prompt)
            else:
                res_text = self._call_openai(prompt, response_format_json=True)
            return json.loads(res_text)
        except Exception as e:
            print(f"Error parsing LLM summaries response: {e}")
            return self._mock_summaries(text)

    def generate_timeline(self, text: str) -> List[Dict[str, str]]:
        if self.provider == "mock":
            return self._mock_timeline(text)
            
        prompt = f"""
        Extract a chronological timeline of events mentioned in this article.
        For each event, extract a time (e.g. "08:00", "May 10, 2026"), the event name, and a short description.
        Output format must be valid JSON:
        {{
            "timeline": [
                {{"time": "08:00", "event": "Protest Starts", "description": "Demonstrators gather outside City Hall."}}
            ]
        }}

        Text:
        {text}
        """
        try:
            if self.provider == "gemini":
                res_text = self._call_gemini(prompt)
            else:
                res_text = self._call_openai(prompt, response_format_json=True)
            data = json.loads(res_text)
            return data.get("timeline", [])
        except Exception as e:
            print(f"Error parsing LLM timeline response: {e}")
            return self._mock_timeline(text)

    # --- MOCK GENERATION FALLBACKS ---

    def _mock_entities(self, text: str) -> List[Dict[str, Any]]:
        entities = []
        # Basic heuristic parsing for testing
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        people = ["President", "Prime Minister", "Minister", "CEO", "Secretary", "Senator", "Director"]
        
        # Pull consecutive capital words (like Google Inc or Joe Biden)
        phrases = re.findall(r'\b[A-Z][a-zA-Z]+\s+[A-Z][a-zA-Z]+\b', text)
        
        seen = set()
        for p in phrases:
            if p not in seen:
                seen.add(p)
                # Categorize
                if any(x in p for x in ["Inc", "Corp", "Company", "Association", "Organization", "Party", "Union"]):
                    entities.append({"name": p, "type": "Organization", "relevance": 0.8})
                elif any(x in p for x in ["Street", "City", "State", "Country", "New York", "London", "Paris", "Washington", "China", "Europe", "America"]):
                    entities.append({"name": p, "type": "Location", "relevance": 0.75})
                else:
                    entities.append({"name": p, "type": "Person", "relevance": 0.85})

        # Inject default mock entities if not enough found
        if len(entities) < 3:
            entities.extend([
                {"name": "Global News Forum", "type": "Organization", "relevance": 0.9},
                {"name": "Sarah Jenkins", "type": "Person", "relevance": 0.8},
                {"name": "Geneva, Switzerland", "type": "Location", "relevance": 0.7},
                {"name": "Energy Summit 2026", "type": "Event", "relevance": 0.85}
            ])
        return entities[:8]

    def _mock_claims(self, text: str) -> List[Dict[str, Any]]:
        # Mock claims based on text contents
        claims = []
        if "protest" in text.lower() or "demonstration" in text.lower():
            claims.append({"subject": "Protestors", "predicate": "demanded", "object": "policy reforms", "confidence": 0.9})
            claims.append({"subject": "Police", "predicate": "deployed", "object": "crowd control measures", "confidence": 0.85})
        if "climate" in text.lower() or "emission" in text.lower():
            claims.append({"subject": "Global Emissions", "predicate": "increased by", "object": "2.4% last year", "confidence": 0.95})
            claims.append({"subject": "Green Policy Accord", "predicate": "mandates", "object": "carbon neutrality by 2050", "confidence": 0.9})
        if "tax" in text.lower() or "economy" in text.lower():
            claims.append({"subject": "Tax Reform Bill", "predicate": "reduces", "object": "corporate tax to 15%", "confidence": 0.95})
            claims.append({"subject": "Opposition Parties", "predicate": "oppose", "object": "the deficit implications", "confidence": 0.9})
        
        # Ensure we always return at least some valid claims
        if len(claims) < 2:
            claims.extend([
                {"subject": "The Spokesperson", "predicate": "announced", "object": "the launch of the initiative", "confidence": 0.88},
                {"subject": "The Project", "predicate": "requires", "object": "additional infrastructure budget", "confidence": 0.8}
            ])
        return claims

    def _mock_bias_analysis(self, text: str, source: Optional[str]) -> Dict[str, Any]:
        # Generate some randomized but sensible values
        random.seed(hash(text))
        
        # Check text length and trigger words for bias scores
        bias_score = 35
        sentiment_bias = 30
        framing_bias = 40
        omission_bias = 35
        evidence = []
        
        # Triggers
        if any(w in text.lower() for w in ["shocking", "outrageous", "terrible", "incredible", "disaster", "historic", "scandal"]):
            bias_score += 25
            sentiment_bias += 35
            evidence.append("Use of emotionally loaded modifiers: " + ", ".join([w for w in ["shocking", "outrageous", "terrible", "historic", "scandal"] if w in text.lower()]))
            
        if any(w in text.lower() for w in ["militants", "regime", "insurgents", "far-left", "far-right", "radical"]):
            bias_score += 15
            framing_bias += 25
            evidence.append("Use of polarizing labels such as: " + ", ".join([w for w in ["militants", "regime", "insurgents", "radical"] if w in text.lower()]))

        if "only" in text.lower() or "failed to mention" in text.lower() or len(text) < 500:
            omission_bias += 20
            evidence.append("Lack of alternative viewpoint citations or expert counter-arguments.")
            
        bias_score = min(95, max(15, bias_score))
        sentiment_bias = min(95, max(10, sentiment_bias))
        framing_bias = min(95, max(15, framing_bias))
        omission_bias = min(95, max(10, omission_bias))
        
        if not evidence:
            evidence = ["Neutral presentation of data facts, minor selection of quotes from single source."]

        return {
            "biasScore": bias_score,
            "confidence": 88,
            "sentimentBias": sentiment_bias,
            "framingBias": framing_bias,
            "omissionBias": omission_bias,
            "sentimentExplanation": f"Sentiment score of {sentiment_bias}% indicates moderate emotional loading. The article uses active verbs and selective adverbs to frame events.",
            "framingExplanation": f"Framing score of {framing_bias}% shows thematic positioning. Subtitle or headlines present a slanted viewpoint rather than balanced statements.",
            "omissionExplanation": f"Omission score of {omission_bias}% reflects missing viewpoints. The article focuses heavily on primary source quotes with minimal space for opposing voices.",
            "evidence": evidence
        }

    def _mock_summaries(self, text: str) -> Dict[str, str]:
        # Generate generic but well-structured perspective summaries
        return {
            "conservative": "CONSERVATIVE PERSPECTIVE: The article highlights the importance of economic stability, reduced regulatory burdens, and national security/sovereignty. It cautions against massive government programs, high spending, or rapid alterations to social and institutional frameworks without thorough vetting.",
            "liberal": "LIBERAL PERSPECTIVE: The article emphasizes social justice, equity, government intervention to support marginalized communities, and rapid green transition policies. It calls for stricter environmental standards, corporate accountability, and immediate policy actions to resolve underlying systemic inequities.",
            "neutral": "NEUTRAL SUMMARY: The report details the factual development of the events, including statements from all primary stakeholders, data metrics without loaded modifiers, and the background context leading up to the current situation. It avoids value judgements or predictions.",
            "consensus": "CONSENSUS SUMMARY: All parties agree that the event took place, a public announcement was made, and there are substantial economic or social consequences that require attention. There is shared agreement on basic dates, locations, and major statistics involved."
        }

    def _mock_timeline(self, text: str) -> List[Dict[str, str]]:
        return [
            {"time": "09:00 AM", "event": "Initial Announcement", "description": "The agency released their policy draft to public channels, triggering immediate feedback."},
            {"time": "12:30 PM", "event": "Official Press Conference", "description": "Representatives addressed questions on budget, timing, and environmental impacts."},
            {"time": "03:00 PM", "event": "Public Reaction & Assembly", "description": "Local organizations and citizens gathered to voice concerns and support for the bill."},
            {"time": "06:00 PM", "event": "Government Statement", "description": "A follow-up statement was released to clarify disputed points regarding funding allocations."}
        ]
