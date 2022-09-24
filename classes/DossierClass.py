from pydantic import BaseModel, Field
from .ObjectIdClass import PyObjectId
from bson import ObjectId

class DossierModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    matricule: str = Field(...)
    medecinId: PyObjectId = Field(default_factory=PyObjectId)
    maladie: str = Field(...)
    montant: float = Field(...)
    date: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "matricule": '1',
                "medecinId": '5f9f1b9c1c9d440000f1b5f5',
                "maladie": 'Maladie 1',
                "montant": 1000.0,
                "date": '2020-10-27'
            }
        }