# schemas.py
from pydantic import BaseModel

class TacheCreation(BaseModel):
    nom: str
    description: str
    date_echeance: str

class UtilisateurCreation(BaseModel):
    email: str
    mot_de_passe: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"