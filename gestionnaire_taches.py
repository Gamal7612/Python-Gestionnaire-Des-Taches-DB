from tache import Tache
class GestionnaireTaches:
    # La classe GestionnaireTaches représente un gestionnaire de tâches 
    # qui peut ajouter, supprimer et afficher des tâches.

    def __init__(self):
        self.taches = [] #self.taches est un attribut d'instance qui stocke une liste de tâches

    def ajouter_tache(self, tache):
        self.taches.append(tache) #ajoute une tâche à la liste des tâches

    def supprimer_tache(self, id_tache):
        for tache in self.taches:
            if tache.id == id_tache:
                self.taches.remove(tache)
                print("Tâche supprimée avec succès.")
                return
        print("Tâche introuvable.")

    def afficher_taches(self):
        if not self.taches:
            print("Aucune tâche à afficher.") #affiche un message si la liste des tâches est vide
        else:
            for tache in self.taches:
                print(tache) #affiche chaque tâche dans la liste des tâches
                print("-" * 40) #séparateur visuel entre les tâches

    def marquer_tache_comme_terminee(self, id_tache):
        for tache in self.taches:
            if tache.id == id_tache:
                tache.marquer_comme_terminee()
                print("Tâche marquée comme terminée.")
                return
        print("Tâche introuvable.")