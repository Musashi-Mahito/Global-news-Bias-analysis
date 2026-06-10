from typing import List, Dict, Any
from ai_service.services.graph_service import GraphService

class GraphAgent:
    def __init__(self, graph_service: GraphService):
        self.graph_service = graph_service

    def build_graph(self, article_id: str, article_data: Dict[str, Any], entities: List[Dict[str, Any]], claims: List[Dict[str, Any]], timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Creates/updates the Knowledge Graph for the analyzed article in Neo4j.
        """
        # 1. Create Article Node
        self.graph_service.save_article_node(
            article_id=article_id,
            title=article_data.get("title", ""),
            source=article_data.get("source", ""),
            url=article_data.get("url", ""),
            publish_date=article_data.get("publish_date", "")
        )
        
        # 2. Create Entities and MENTIONS relations
        self.graph_service.save_entity_nodes_and_relationships(article_id, entities)
        
        # 3. Create Claims and SUPPORTS relations
        self.graph_service.save_claim_nodes_and_relationships(article_id, claims)
        
        # 4. Create Events and COVERED_BY relations
        self.graph_service.save_event_timeline(article_id, timeline)
        
        # 5. Fetch and return visual representation of the graph
        return self.graph_service.get_article_graph(article_id)
        
    def link_related_articles(self, original_id: str, related_ids: List[str]):
        """
        Links related articles together using RELATED_TO relationship.
        """
        for rid in related_ids:
            query = """
            MATCH (a1:Article {id: $original_id})
            MATCH (a2:Article {id: $related_id})
            MERGE (a1)-[:RELATED_TO]->(a2)
            """
            self.graph_service.run_query(query, {"original_id": original_id, "related_id": rid})
