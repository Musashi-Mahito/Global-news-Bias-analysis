from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from ai_service.config import settings

class GraphService:
    def __init__(self):
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD
        self.driver = None
        
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Verify connectivity
            self.driver.verify_connectivity()
            print("Connected to Neo4j successfully.")
        except Exception as e:
            print(f"Failed to connect to Neo4j at {self.uri}: {e}. Graph database will operate in mock mode.")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def run_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self.driver:
            print(f"Mock Cypher Execution: {query} with params {parameters}")
            return []
            
        parameters = parameters or {}
        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [dict(record) for record in result]
        except Exception as e:
            print(f"Neo4j query execution error: {e}")
            return []

    def save_article_node(self, article_id: str, title: str, source: str, url: str, publish_date: str):
        query = """
        MERGE (a:Article {id: $article_id})
        SET a.title = $title,
            a.source = $source,
            a.url = $url,
            a.publishDate = $publish_date
        RETURN a
        """
        params = {
            "article_id": article_id,
            "title": title,
            "source": source,
            "url": url,
            "publish_date": publish_date
        }
        self.run_query(query, params)

    def save_entity_nodes_and_relationships(self, article_id: str, entities: List[Dict[str, Any]]):
        # Create entities and MENTIONS relationships
        for entity in entities:
            name = entity.get("name")
            ent_type = entity.get("type", "Other")
            relevance = entity.get("relevance", 0.5)
            
            # Map type to Neo4j Labels
            label = "Other"
            if ent_type.lower() == "person":
                label = "Person"
            elif ent_type.lower() == "organization":
                label = "Organization"
            elif ent_type.lower() == "location":
                label = "Location"
            elif ent_type.lower() == "event":
                label = "Event"
                
            query = f"""
            MATCH (a:Article {{id: $article_id}})
            MERGE (e:{label} {{name: $name}})
            MERGE (a)-[r:MENTIONS]->(e)
            SET r.relevance = $relevance
            """
            params = {
                "article_id": article_id,
                "name": name,
                "relevance": relevance
            }
            self.run_query(query, params)

    def save_claim_nodes_and_relationships(self, article_id: str, claims: List[Dict[str, Any]]):
        for i, claim in enumerate(claims):
            sub = claim.get("subject", "")
            pred = claim.get("predicate", "")
            obj = claim.get("object", "")
            conf = claim.get("confidence", 1.0)
            claim_id = f"{article_id}_claim_{i}"
            
            query = """
            MATCH (a:Article {id: $article_id})
            MERGE (c:Claim {id: $claim_id})
            SET c.subject = $sub,
                c.predicate = $pred,
                c.object = $obj,
                c.confidence = $conf
            MERGE (a)-[:SUPPORTS]->(c)
            """
            params = {
                "article_id": article_id,
                "claim_id": claim_id,
                "sub": sub,
                "pred": pred,
                "obj": obj,
                "conf": conf
            }
            self.run_query(query, params)

    def save_event_timeline(self, article_id: str, timeline: List[Dict[str, Any]]):
        # Connect article to events and timeline items
        for i, item in enumerate(timeline):
            time_str = item.get("time", "")
            event_name = item.get("event", "")
            desc = item.get("description", "")
            event_id = f"{article_id}_event_{i}"
            
            query = """
            MATCH (a:Article {id: $article_id})
            MERGE (e:Event {id: $event_id})
            SET e.name = $event_name,
                e.time = $time_str,
                e.description = $desc
            MERGE (e)-[:COVERED_BY]->(a)
            """
            params = {
                "article_id": article_id,
                "event_id": event_id,
                "event_name": event_name,
                "time_str": time_str,
                "desc": desc
            }
            self.run_query(query, params)

    def get_article_graph(self, article_id: str) -> Dict[str, Any]:
        # Retrieve graph nodes and edges centered around a specific article
        nodes_query = """
        MATCH (a:Article {id: $article_id})-[r:MENTIONS|SUPPORTS|COVERED_BY]-(n)
        RETURN labels(n) as label, properties(n) as props, id(n) as id
        UNION
        MATCH (a:Article {id: $article_id})
        RETURN labels(a) as label, properties(a) as props, id(a) as id
        """
        
        edges_query = """
        MATCH (a:Article {id: $article_id})-[r]-(n)
        RETURN id(a) as source, id(n) as target, type(r) as type
        """
        
        nodes = self.run_query(nodes_query, {"article_id": article_id})
        edges = self.run_query(edges_query, {"article_id": article_id})
        
        # If Neo4j is mock or empty, return standard mock nodes/edges
        if not nodes:
            return self._get_mock_article_graph(article_id)
            
        formatted_nodes = []
        for n in nodes:
            label = n["label"][0] if n["label"] else "Node"
            props = n["props"]
            name = props.get("title") or props.get("name") or props.get("subject") or "Node"
            formatted_nodes.append({
                "id": str(n["id"]),
                "label": label,
                "name": name,
                "properties": props
            })
            
        formatted_edges = []
        for e in edges:
            formatted_edges.append({
                "source": str(e["source"]),
                "target": str(e["target"]),
                "type": e["type"]
            })
            
        return {"nodes": formatted_nodes, "edges": formatted_edges}

    def _get_mock_article_graph(self, article_id: str) -> Dict[str, Any]:
        # Deterministic mock graph based on article_id
        nodes = [
            {"id": "1", "label": "Article", "name": "Main Article", "properties": {"title": "Main Article Analysis"}},
            {"id": "2", "label": "Organization", "name": "Global News Forum", "properties": {"name": "Global News Forum"}},
            {"id": "3", "label": "Person", "name": "Sarah Jenkins", "properties": {"name": "Sarah Jenkins"}},
            {"id": "4", "label": "Location", "name": "Geneva, Switzerland", "properties": {"name": "Geneva, Switzerland"}},
            {"id": "5", "label": "Claim", "name": "Policy reform draft", "properties": {"subject": "Policy reform", "predicate": "drafted", "object": "by summit leaders"}},
            {"id": "6", "label": "Claim", "name": "Budget discrepancy", "properties": {"subject": "Budget", "predicate": "increased", "object": "by 10%"}}
        ]
        edges = [
            {"source": "1", "target": "2", "type": "MENTIONS"},
            {"source": "1", "target": "3", "type": "MENTIONS"},
            {"source": "1", "target": "4", "type": "MENTIONS"},
            {"source": "1", "target": "5", "type": "SUPPORTS"},
            {"source": "1", "target": "6", "type": "SUPPORTS"}
        ]
        return {"nodes": nodes, "edges": edges}
