import os

from databases import Database
from fastapi import FastAPI

PG_DB_NAME = os.environ.get("POSTGRES_DB")
PG_HOST = os.environ.get("POSTGRES_HOST")
PG_PORT = os.environ.get("POSTGRES_PORT")

app = FastAPI()
database = Database(f"postgresql://{PG_HOST}:{PG_PORT}/{PG_DB_NAME}")


@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/")
async def fetch_data(id: int):
    query = "SELECT * FROM parts_v WHERE part_id={}".format(str(id))
    results = await database.fetch_all(query=query)

    return results
