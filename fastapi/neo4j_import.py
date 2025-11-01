from neo4j import GraphDatabase
import os
import requests

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

HA_TOKEN = os.getenv("HA_TOKEN")
HA_URL = "http://192.168.1.23:8123" 

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def import_trisensors_to_neo4j():
    print("🔄 SYNC with Home Assistant & Neo4j")

    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    response = requests.get(f"{HA_URL}/api/states", headers=headers)

    if response.status_code != 200:
        return {"error": f"Home Assistant error: {response.text}"}

    states = response.json()

    trisensors = []
    for entity in states:
        entity_id = entity["entity_id"]

        # Sélectionne uniquement les TriSensors Aeotec
        if "sensor" in entity_id and (
            "air_temperature" in entity_id
            or "illuminance" in entity_id
            or "motion" in entity_id
        ):
            trisensors.append(entity)

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")  # reset graph avant rédaction

        session.run("""
            CALL n10s.graphconfig.init({
              handleVocabUris: "SHORTEN",
              keepLangTag: false,
              handleMultival: "OVERWRITE",
              keepCustomDataTypes: true
            })
        """)

        for s in trisensors:
            sensor_id = s["entity_id"]
            value = s["state"]
            unit = s.get("attributes", {}).get("unit_of_measurement", "")
            name = s.get("attributes", {}).get("friendly_name", "TriSensor")

            session.run(
                """
                MERGE (sensor:Sensor {id:$id})
                SET sensor.hasName = $name

                MERGE (m:Measurement {id:$id + "_measurement"})
                SET m.hasValue = $value, m.hasUnit = $unit

                MERGE (room:Room {name:"Salon"})

                MERGE (sensor)-[:MEASURES]->(m)
                MERGE (sensor)-[:LOCATED_IN]->(room)
                """,
                id=sensor_id,
                name=name,
                value=value,
                unit=unit,
            )

    return {"status": "✅ Sync OK", "count": len(trisensors)}
