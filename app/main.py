import os
from typing import Optional

from databases import Database
from fastapi import FastAPI

PG_DB_NAME = os.environ.get("POSTGRES_DB", "ur_parts")
PG_USER = os.environ.get("POSTGRES_USER")
PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
PG_HOST = os.environ.get("POSTGRES_HOST")
PG_PORT = int(os.environ.get("POSTGRES_PORT"))


app = FastAPI()
database = Database(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB_NAME}")


@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/ur_parts/")
async def fetch_data(
    limit: int = 10,
    vehicle_brand: Optional[str] = None,
    vehicle_category: Optional[str] = None,
    vehicle_model: Optional[str] = None,
    part_name: Optional[str] = None,
    part_category: Optional[str] = None,
):
    """
    Load data of UrParts with parameters:

    - **limit**: Data limit. To specify no limit, set -1.
    - **vehicle_brand**: Vehicle brand. e.g. 'Ammann'
    - **vehicle_category**: Vehicle category/type. e.g. 'Roller Parts'
    - **vehicle_model**: Vehicle model name. e.g. 'ASC100'
    - **part_name**: Part model name. e.g. 'ND021197'
    - **part_category**: Part category/type. e.g. 'bolt'
    """
    conditions = {
        "vehicle_brand": vehicle_brand,
        "vehicle_category": vehicle_category,
        "vehicle_model": vehicle_model,
        "part_name": part_name,
        "part_category": part_category,
    }
    query = "SELECT * FROM parts_v WHERE 1=1"

    for col in conditions:
        if conditions[col]:
            query += f" AND {col}={conditions[col]}"

    if limit != -1:
        query += f" LIMIT {limit}"
    results = await database.fetch_all(query=query)
    return results
