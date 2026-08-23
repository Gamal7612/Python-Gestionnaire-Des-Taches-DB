# schemas.py
from pydantic import BaseModel

class TacheCreation(BaseModel):
    nom: str
    description: str
    date_echeance: str