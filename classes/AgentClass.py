from pydantic import BaseModel, Field
from .ObjectIdClass import PyObjectId
from bson import ObjectId

class AgentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    matricule: str = Field(...)
    nom: str = Field(...)
    prenom: str = Field(...)
    age: int = Field(...)
    address: str = Field(...)
    tele: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "matricule": '1',
                "nom": 'Name 1',
                "prenom": 'First Name 1',
                "age": 25,
                "address": 'Adresse 1',
                "tele": "041981545"
            }
        }