from Repositories.creneaux_repository import CreneauRpository
from datetime import date

class CreneauService:
    def __init__(self):
        self.creneau_repo = CreneauRpository()

    def creer_creneau(self, creneau):
        if self.creneau_repo.creneau_exist(creneau.heure_debut, creneau.heure_fin):
            raise Exception("Ce creneau existe deja.")
        
        self.creneau_repo.enregistrer(creneau)

    def lister_creneaux(self):
        return self.creneau_repo.afficher_tout()
    
    def lister_creneau_disponible(self):
        return self.creneau_repo.creneau_disponibles()
    
    def planing(sefl):
        return sefl.creneau_repo.afficher_planing()
    
    def obtenir_disponibles_par_date(self, date_choisie):
        if date_choisie < date.today():
            raise Exception("Impossible de réserver dans le passé")

        return self.creneau_repo.creneau_disponibles_par_date(date_choisie)