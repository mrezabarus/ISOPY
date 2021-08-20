from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from databases import Database

app = FastAPI()

database = Database('mysql://root:admin@localhost/articulate')

@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()


@app.get("/jadwalelearning")
async def fetch_data():
    query = """SELECT 
            id_kursus
            , kursus
            from eknowledge_library
            where hide is null"""
    results = await database.fetch_all(query=query)

@app.post("/pilihjadwalelearning")
async def fetch_data(id: int):
    query = "SELECT id_kursus , kursus FROM eknowledge_library WHERE id_kursus={}".format(str(id))
    results = await database.fetch_all(query=query)

    return  results

    return  results