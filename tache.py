class Tache:
    compteur_id=0 #compteur_id est un attribut de classe qui sert à générer des identifiants uniques pour chaque tâche
    # La classe Tache représente une tâche avec un nom, une description,
    # une date d'échéance et un statut de complétion.
    def __init__(self, nom, description, date_echeance):
        Tache.compteur_id += 1
        self.id_tache = Tache.compteur_id #self.id est un attribut d'instance qui stocke l'identifiant unique de la tâche
        self.nom = nom #self.nom est un attribut d'instance qui stocke le nom de la tâche
        self.description = description #self.description est un attribut d'instance qui stocke la description de la tâche
        self.date_echeance = date_echeance #self.date_echeance est un attribut d'instance qui stocke la date d'échéance de la tâche
        self.terminee = False #self.terminee est un attribut d'instance qui stocke le statut de la tâche

    def marquer_comme_terminee(self):
        self.terminee = True

    def __str__(self):
        statut = "Terminé" if self.terminee else "En cours"# statut est une variable locale qui stocke le statut de la tâche sous forme de chaîne de caractères
        return f"Tâche: {self.nom}\nDescription: {self.description}\nDate d'échéance: {self.date_echeance}\nStatut: {statut}\nID: {self.id_tache}"# La méthode __str__ retourne une représentation sous forme de chaîne de caractères de l'objet Tache, incluant le nom, la description, la date d'échéance et le statut de la tâche.

    def to_dict(self):
        return {
            "id": self.id_tache,
            "nom": self.nom,
            "description": self.description,
            "date_echeance": self.date_echeance,
            "terminee": self.terminee
        }