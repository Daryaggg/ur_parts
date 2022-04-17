from databases import Database
from fastapi import FastAPI

app = FastAPI()
database = Database(f"sqlite:///UrParts.db")


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
