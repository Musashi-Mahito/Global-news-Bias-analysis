import re
import requests
from typing import Dict, Any, Optional
from datetime import datetime

class ExtractorAgent:
    def __init__(self):
        pass

    def extract(self, text: str, url: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract article details from text and/or URL.
        """
        if url and (url.startswith("http://") or url.startswith("https://")):
            return self._extract_from_url(url)
        else:
            return self._extract_from_text(text)

    def _extract_from_url(self, url: str) -> Dict[str, Any]:
        try:
            # Simple request to extract main body text
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            res = requests.get(url, headers=headers, timeout=10)
            html = res.text
            
            # Clean simple HTML extraction using regex
            title_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
            title = title_match.group(1).strip() if title_match else "Extracted Article from Link"
            
            # Remove scripts and styles
            clean_html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
            clean_html = re.sub(r"<style.*?>.*?</style>", "", clean_html, flags=re.DOTALL | re.IGNORECASE)
            
            # Extract text blocks
            paragraphs = re.findall(r"<p.*?>(.*?)</p>", clean_html, flags=re.DOTALL | re.IGNORECASE)
            text_blocks = []
            for p in paragraphs:
                # remove inner tags
                p_text = re.sub(r"<.*?>", "", p).strip()
                # resolve HTML entities
                p_text = p_text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&quot;", '"')
                if len(p_text) > 40:
                    text_blocks.append(p_text)
                    
            content = "\n\n".join(text_blocks)
            if not content:
                # fallback to raw tag stripping
                content = re.sub(r"<.*?>", "", html)[:1500]
                
            # Extract source domain name
            source = url.split("//")[-1].split("/")[0]
            source = source.replace("www.", "")
            
            return {
                "title": title[:200],
                "content": content,
                "source": source,
                "publish_date": datetime.utcnow().strftime("%Y-%m-%d"),
                "language": "en"
            }
        except Exception as e:
            print(f"Error scraping url {url}: {e}. Falling back to text-based extraction.")
            return {
                "title": "Failed to Scrape URL",
                "content": f"Could not scrape {url}. Error: {e}",
                "source": "Scraper Error",
                "publish_date": datetime.utcnow().strftime("%Y-%m-%d"),
                "language": "en"
            }

    def _extract_from_text(self, text: str) -> Dict[str, Any]:
        # Extract title from first line
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        title = lines[0] if lines else "Untitled News Article"
        
        # If title is too long, truncate it
        if len(title) > 100:
            title = title[:97] + "..."
            
        content = text
        source = "User Upload"
        
        # Simple heuristic to check language
        language = "en"
        # If we have non-latin characters dominant, we can tag it, but English is default.

        return {
            "title": title,
            "content": content,
            "source": source,
            "publish_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "language": language
        }
c = ExtractorAgent()
