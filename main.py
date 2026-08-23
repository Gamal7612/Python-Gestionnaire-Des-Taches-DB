from fastapi import FastAPI
from schemas import TacheCreation
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import TacheModel

Base.metadata.create_all(bind=engine)   # crée la table "taches" si elle n'existe pas encore

app = FastAPI()

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API"}

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
def supprimer_tache(tache_id: int, db: Session = Depends(get_db)):
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