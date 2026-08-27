from fastapi import FastAPI
from schemas import TacheCreation,UtilisateurCreation,Token
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import TacheModel, UtilisateurModel
from security import hasher_mot_de_passe, verifier_mot_de_passe, creer_token, utilisateur_courant

Base.metadata.create_all(bind=engine)   # crée la table "taches" si elle n'existe pas encore

app = FastAPI()

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API"}

@app.post("/register", response_model=Token)
def inscrire(utilisateur_data:UtilisateurCreation, db: Session=Depends(get_db)):
    #Verifie que l'email n'existe pas deja
    utilisateur_existant = db.query(UtilisateurModel).filter(UtilisateurModel.email==utilisateur_data.email).first()
    if utilisateur_existant:
        raise HTTPException(status_code=400,detail="Cet email est déjà utilisé")

    nouvel_utilisateur=UtilisateurModel(
        email=utilisateur_data.email,
        mot_de_passe_hash=hasher_mot_de_passe(utilisateur_data.mot_de_passe)
    )

    db.add(nouvel_utilisateur)
    db.commit()
    db.refresh(nouvel_utilisateur)

    token=creer_token({"sub":nouvel_utilisateur.email})
    return {"access_token":token,"token_type":"bearer"}

@app.post("/login",response_model=Token)
def connecter(utilisateur_data:UtilisateurCreation,db:Session = Depends(get_db)):
    utilisateur=db.query(UtilisateurModel).filter(UtilisateurModel.email==utilisateur_data.email).first()
    if not utilisateur or not verifier_mot_de_passe(utilisateur_data.mot_de_passe, utilisateur.mot_de_passe_hash):
        raise HTTPException(status_code=401,detail="Mot de passe incorrect")

    token=creer_token({"sub":utilisateur.email})
    return {"access_token":token,"token_type":"bearer"}




@app.get("/taches")
def lister_taches(db: Session = Depends(get_db)):
    taches = db.query(TacheModel).all()
    return taches

@app.post("/taches")
def creer_tache(tache: TacheCreation, db: Session = Depends(get_db)):
    nouvelle_tache = TacheModel(
        nom=tache.nom,
        description=tache.description,
        date_echeance=tache.date_echeance
    )
    db.add(nouvelle_tache)
    db.commit()
    db.refresh(nouvelle_tache)
    return nouvelle_tache

@app.get("/taches/{tache_id}")
def obtenir_tache(tache_id: int, db: Session = Depends(get_db)):
    tache = db.query(TacheModel).filter(TacheModel.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return tache

@app.delete("/taches/{tache_id}")
def supprimer_tache(tache_id: int, db: Session = Depends(get_db), utilisateur=Depends(utilisateur_courant)):
    tache = db.query(TacheModel).filter(TacheModel.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    db.delete(tache)
    db.commit()
    return {"message": "Tâche supprimée avec succès"}

@app.patch("/taches/{tache_id}/terminer")
def terminer_tache(tache_id: int, db: Session = Depends(get_db)):
    tache = db.query(TacheModel).filter(TacheModel.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    tache.terminee = True
    db.commit()
    db.refresh(tache)
    return tache