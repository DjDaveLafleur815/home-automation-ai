from fastapi import FastAPI, HTTPException
import os
import requests
from neo4j import GraphDatabase

app = FastAPI()

HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

@app.get("/trisensors")
def get_trisensors():
    """Récupère uniquement les TriSensors depuis Home Assistant"""
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{HA_URL}/api/states", headers=headers)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Home Assistant error: {e}")

    states = response.json()

    trisensors = []

    for entity in states:
        if (
            entity["entity_id"].startswith("sensor.sensor_")
            and ("air_temperature" in entity["entity_id"] or "illuminance" in entity["entity_id"])
        ):
            trisensors.append({
                "id": entity["entity_id"],
                "name": entity["attributes"].get("friendly_name"),
                "value": entity["state"],
                "unit": entity["attributes"].get("unit_of_measurement"),
            })

    return {"trisensors": trisensors}

@app.get("/sync_trisensors")
@app.post("/sync_trisensors")
def sync_to_neo4j():
    """Importe les capteurs dans Neo4j"""
    trisensors = get_trisensors()["trisensors"]

    with driver.session() as session:
        for sensor in trisensors:
            session.run(
                """
                MERGE (t:TriSensor {id: $id})
                SET t.name = $name, t.value = $value, t.unit = $unit
                """,
                id=sensor["id"], name=sensor["name"], value=sensor["value"], unit=sensor["unit"]
            )

    return {"status": "ok", "imported": len(trisensors)}


