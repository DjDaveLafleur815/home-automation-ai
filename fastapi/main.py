from fastapi import FastAPI
import httpx
from neo4j import GraphDatabase

app = FastAPI()

# ---------------------------
# Configuration
# ---------------------------

HA_URL = "http://192.168.1.23:8123/api"  # ← remplace ici par ton IP Home Assistant
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIwMmFmMmIzZDM5NjU0OTVkODM4MDUwNWE1ZTkyOTkxMiIsImlhdCI6MTc2MTcwMzYxNSwiZXhwIjoyMDc3MDYzNjE1fQ.m_DwP-8cw0d2TPi7IFDgxK1gERcHhHYLgYJsxsOsK2c"              # ← met ton token API

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "davdu815"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


# ---------------------------
# Synchronisation Home Assistant → Neo4j
# ---------------------------

@app.get("/sync")
async def sync_devices():
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{HA_URL}/states", headers=headers)

    if response.status_code != 200:
        return {"error": "Impossible de se connecter à Home Assistant"}

    devices = response.json()

    with driver.session() as session:
        for d in devices:
            entity_id = d["entity_id"]
            name = d["attributes"].get("friendly_name", entity_id)
            dev_type = entity_id.split(".")[0]

            session.run("""
                MERGE (d:Device {id: $entity_id})
                SET d.name = $name, d.type = $type
            """, entity_id=entity_id, name=name, type=dev_type)

    return {"status": "synchronisé ✅", "count": len(devices)}


# ---------------------------
# Retourner uniquement les TriSensors
# ---------------------------

@app.get("/trisensors")
async def get_trisensors():
    query = """
    MATCH (d:Device)
    WHERE d.id CONTAINS 'aeotec' OR d.id CONTAINS 'trisensor'
    RETURN d.id AS id, d.name AS name, d.type AS type
    """

    with driver.session() as session:
        res = session.run(query)
        trisensors = [record.data() for record in res]

    return {"trisensors": trisensors}
