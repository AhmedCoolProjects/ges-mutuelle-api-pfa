from fastapi import FastAPI, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
import motor.motor_asyncio
import os
from classes.AgentClass import AgentModel
from classes.PharmacieClass import PharmacyModel
from classes.MedecinClass import MedecinModel
from fastapi.middleware.cors import CORSMiddleware
from classes.DossierClass import DossierModel

app = FastAPI()

origins = [
    "https://ges-mutuelle-amendis.vercel.app",
    "https://get-mutuelle-api.herokuapp.com",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client["ges-mutuelle"]

# run 'make dev' to test the application


@app.get("/")
def welcome():
    return {"message": "Welcome to AMENDIS API"}


# AGENT OPERATIONS
@app.get("/agents/all", response_description="List all agents")
async def list_agents():
    agents = []
    for agent in await db["agents"].find().to_list(100):
        agents.append(agent)
    return agents

@app.get("/agents/{id}", response_description="Get a single agent", response_model=AgentModel)
async def show_agent(id: str):
    if (agent := await db["agents"].find_one({"_id": id})) is not None:
        return agent
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Agent not found")

@app.post("/agents/add", response_description="Add new agent", response_model=AgentModel)
async def create_agent(agent: AgentModel = Body(...)):
    agent = jsonable_encoder(agent)
    new_agent = await db["agents"].insert_one(agent)
    created_agent = await db["agents"].find_one({"_id": new_agent.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_agent)

@app.post("/agents/update/{id}", response_description="Update an agent", response_model=AgentModel)
async def update_agent(id: str, agent: AgentModel = Body(...)):
    agent = {k: v for k, v in agent.dict().items() if v is not None}
    if len(agent) >= 1:
        update_result = await db["agents"].update_one({"_id": id}, {"$set": agent})
        if update_result.modified_count == 1:
            if (
                updated_agent := await db["agents"].find_one({"_id": id})
            ) is not None:
                return updated_agent
    if (existing_agent := await db["agents"].find_one({"_id": id})) is not None:
        return existing_agent
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Agent not found")

@app.delete("/agents/delete/{id}", response_description="Delete an agent")
async def delete_agent(id: str):
    delete_result = await db["agents"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Agent not found")


# MEDECIN OPERATIONS
@app.get("/medecins/all", response_description="List all medecins")
async def list_medecins():
    medecins = []
    for medecin in await db["medecins"].find().to_list(100):
        medecins.append(medecin)
    return medecins

@app.get("/medecins/{id}", response_description="Get a single medecin", response_model=MedecinModel)
async def show_medecin(id: str):
    if (medecin := await db["medecins"].find_one({"_id": id})) is not None:
        return medecin
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Medecin not found")

@app.post("/medecins/add", response_description="Add new medecin", response_model=MedecinModel)
async def create_medecin(medecin: MedecinModel = Body(...)):
    medecin = jsonable_encoder(medecin)
    new_medecin = await db["medecins"].insert_one(medecin)
    created_medecin = await db["medecins"].find_one({"_id": new_medecin.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_medecin)

@app.post("/medecins/update/{id}", response_description="Update a medecin", response_model=MedecinModel)
async def update_medecin(id: str, medecin: MedecinModel = Body(...)):
    medecin = {k: v for k, v in medecin.dict().items() if v is not None}
    if len(medecin) >= 1:
        update_result = await db["medecins"].update_one({"_id": id}, {"$set": medecin})
        if update_result.modified_count == 1:
            if (
                updated_medecin := await db["medecins"].find_one({"_id": id})
            ) is not None:
                return updated_medecin
    if (existing_medecin := await db["medecins"].find_one({"_id": id})) is not None:
        return existing_medecin
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Medecin not found")

@app.delete("/medecins/delete/{id}", response_description="Delete a medecin")
async def delete_medecin(id: str):
    delete_result = await db["medecins"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Medecin not found")

# PHARMACIE OPERATIONS
@app.get("/pharmacies/all", response_description="List all pharmacies")
async def list_pharmacies():
    pharmacies = []
    for pharmacie in await db["pharmacies"].find().to_list(100):
        pharmacies.append(pharmacie)
    return pharmacies

@app.get("/pharmacies/{id}", response_description="Get a single pharmacie", response_model=PharmacyModel)
async def show_pharmacie(id: str):
    if (pharmacie := await db["pharmacies"].find_one({"_id": id})) is not None:
        return pharmacie
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="Pharmacie not found")

@app.post("/pharmacies/add", response_description="Add new pharmacie", response_model=PharmacyModel)
async def create_pharmacie(pharmacie: PharmacyModel = Body(...)):
    pharmacie = jsonable_encoder(pharmacie)
    new_pharmacie = await db["pharmacies"].insert_one(pharmacie)
    created_pharmacie = await db["pharmacies"].find_one({"_id": new_pharmacie.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_pharmacie)

@app.post("/pharmacies/update/{id}", response_description="Update a pharmacie", response_model=PharmacyModel)
async def update_pharmacie(id: str, pharmacie: PharmacyModel = Body(...)):
    pharmacie = {k: v for k, v in pharmacie.dict().items() if v is not None}
    if len(pharmacie) >= 1:
        update_result = await db["pharmacies"].update_one({"_id": id}, {"$set": pharmacie})
        if update_result.modified_count == 1:
            if (
                updated_pharmacie := await db["pharmacies"].find_one({"_id": id})
            ) is not None:
                return updated_pharmacie
    if (existing_pharmacie := await db["pharmacies"].find_one({"_id": id})) is not None:
        return existing_pharmacie
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Pharmacie not found")

@app.delete("/pharmacies/delete/{id}", response_description="Delete a pharmacie")
async def delete_pharmacie(id: str):
    delete_result = await db["pharmacies"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="Pharmacie not found")

# DOSSIER OPERATIONS
@app.get("/dossiers/all", response_description="List all dossiers")
async def list_dossiers():
    dossiers = []
    for dossier in await db["dossiers"].find().to_list(100):
        dossiers.append(dossier)
    return dossiers

@app.get("/dossiers/{id}", response_description="Get a single dossier", response_model=DossierModel)
async def show_dossier(id: str):
    if (dossier := await db["dossiers"].find_one({"_id": id})) is not None:
        return dossier
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content="dossier not found")

@app.post("/dossiers/add", response_description="Add new dossier", response_model=DossierModel)
async def create_dossier(dossier: DossierModel = Body(...)):
    dossier = jsonable_encoder(dossier)
    new_dossier = await db["dossiers"].insert_one(dossier)
    created_dossier = await db["dossiers"].find_one({"_id": new_dossier.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_dossier)

@app.post("/dossiers/update/{id}", response_description="Update a dossier", response_model=DossierModel)
async def update_dossier(id: str, dossier: DossierModel = Body(...)):
    dossier = {k: v for k, v in dossier.dict().items() if v is not None}
    if len(dossier) >= 1:
        update_result = await db["dossiers"].update_one({"_id": id}, {"$set": dossier})
        if update_result.modified_count == 1:
            if (
                updated_dossier := await db["dossiers"].find_one({"_id": id})
            ) is not None:
                return updated_dossier
    if (existing_dossier := await db["dossiers"].find_one({"_id": id})) is not None:
        return existing_dossier
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="dossier not found")

@app.delete("/dossiers/delete/{id}", response_description="Delete a dossier")
async def delete_dossier(id: str):
    delete_result = await db["dossiers"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_404_NOT_FOUND, content="dossier not found")