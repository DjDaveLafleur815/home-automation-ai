from fastapi import FastAPI, HTTPException
from neo4j_main import insert_trisensor
import httpx
import os

app = FastAPI()

HA_TOKEN = os.getenv("HA_TOKEN")
HA_URL = "http://192.168.1.23:8123/api"  # <-- PAS ENTRE GUILLEMETS AVEC { }

@app.get("/trisensors")
async def get_trisensors():
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{HA_URL}/states", headers=headers)

        data = response.json()
        print(data)  # <- debug

        devices = []

        for entity in data:
            if entity["entity_id"].startswith("sensor.") and any(
                key in entity["attributes"].get("friendly_name", "").lower()
                for key in ["temperature", "lumin", "motion"]
            ):
                devices.append({
                    "id": entity["entity_id"],
                    "name": entity["attributes"].get("friendly_name"),
                    "value": entity["state"],
                    "unit": entity["attributes"].get("unit_of_measurement"),
                })
        for s in devices:
            insert_trisensor(
                s["id"],
                s["name"],
                s["value"],
                s["unit"]
            )

        return {"trisensors": devices}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur Home Assistant: {str(e)}")

