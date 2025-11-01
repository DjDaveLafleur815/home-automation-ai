from neo4j import GraphDatabase
import os

# 🔥 Toujours utiliser le nom du service Docker, pas localhost
NEO4J_URI = os.getenv("NEO4J_URI") or "bolt://neo4j:7687"
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "davdu815")

print(f"[Neo4j] Connecting to {NEO4J_URI} with user {NEO4J_USER}")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def insert_trisensor(entity_id, name, value, unit, location="Salon"):
    with driver.session() as session:
        session.run("""
            MERGE (s:Sensor {id: $entity_id})
            SET s.name = $name

            MERGE (m:Measurement {unit: $unit})
            SET m.value = $value

            MERGE (r:Room {name: $location})

            MERGE (s)-[:MEASURES]->(m)
            MERGE (s)-[:LOCATED_IN]->(r)
        """, entity_id=entity_id, name=name, value=value, unit=unit, location=location)
