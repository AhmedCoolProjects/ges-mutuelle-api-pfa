from pydantic import BaseModel, Field
from .ObjectIdClass import PyObjectId
from bson import ObjectId

class MedecinModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    speciality: str = Field(...)
    nom: str = Field(...)
    prenom: str = Field(...)
    address: str = Field(...)
    tele: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "speciality": 'Speciality 1',
                "nom": 'Name 1',
                "prenom": 'First Name 1',
                "adresse": 'Adresse 1',
                "tele": 'Télé 1'
            }
        }