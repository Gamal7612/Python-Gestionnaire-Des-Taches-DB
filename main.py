from fastapi import FastAPI
from gestionnaire_taches import GestionnaireTaches
from schemas import TacheCreation
from tache import Tache
from fastapi import HTTPException

app = FastAPI()
gestionnaire = GestionnaireTaches()

@app.get("/")
def accueil():
    return {"message": "Bienvenue sur l'API"}

@app.get("/taches")
def lister_taches():
    return [t.to_dict() for t in gestionnaire.taches]   # nécessite to_dict() vu en semaine 4

@app.get("/taches/{tache_id}")
def obtenir_tache(tache_id: int):
    for tache in gestionnaire.taches:
        if tache.id_tache == tache_id:
            return tache.to_dict()
    raise HTTPException(status_code=404, detail="Tâche introuvable.")

@app.patch("/taches/{tache_id}/terminer")
def marquer_tache_comme_terminee(tache_id: int):
    for tache in gestionnaire.taches:
        if tache.id_tache == tache_id:
            tache.marquer_comme_terminee()
            return tache.to_dict()
    raise HTTPException(status_code=404, detail="Tâche introuvable.")

@app.delete("/taches/{tache_id}")
def supprimer_tache(tache_id: int):
    for tache in gestionnaire.taches:
        if tache.id_tache == tache_id:
            gestionnaire.supprimer_tache(tache_id)
            return {"message": "Tâche supprimée avec succès."}
    raise HTTPException(status_code=404, detail="Tâche introuvable.")

@app.post("/taches")
def creer_tache(tache_data: TacheCreation):
    nouvelle_tache = Tache(tache_data.nom, tache_data.description, tache_data.date_echeance)
    gestionnaire.ajouter_tache(nouvelle_tache)
    return nouvelle_tache.to_dict()