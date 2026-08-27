import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHME = "HS256"
DUREE_VALIDITE_TOKEN_MINUTES=60

security=HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def creer_token(donnees: dict) -> str:
    """Génère un JWT signé, valide pour une durée limitée."""
    donnees_a_encoder=donnees.copy()
    expiration=datetime.utcnow()+timedelta(minutes=DUREE_VALIDITE_TOKEN_MINUTES)
    donnees_a_encoder.update({"exp":expiration})
    token=jwt.encode(donnees_a_encoder,SECRET_KEY,algorithm=ALGORITHME)
    return token

def verifier_token(token: str) -> dict|None:
    """Vérifie un JWT et retourne son contenu, ou None s'il est invalide/expiré."""
    try:
        payload= jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHME])
        return payload
    except JWTError:
        return None

def hasher_mot_de_passe(password: str) -> str:
    return pwd_context.hash(password)

def verifier_mot_de_passe(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def utilisateur_courant(credentials: HTTPAuthorizationCredentials=Depends(security)):
    """"""
    token=credentials.credentials
    payload=verifier_token(token)
    if payload is None :
        raise HTTPException(status_code=401,detail="Token invalide ou périmé")
    