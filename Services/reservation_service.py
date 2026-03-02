from Repositories.reservation_repository import ReservationRepository
from Repositories.creneaux_repository import CreneauRpository
from Repositories.groupe_repository import GroupeRepository
import csv

class ReservationService:
    def __init__(self):
        self.res_repo = ReservationRepository()
        self.creneau_repo = CreneauRpository()
        self.groupe_repo = GroupeRepository()

    def reserver(self, date, id_creneau, id_groupe, type_evenement):
        creneau = self.creneau_repo.trouver_par_id(id_creneau)

        if not creneau:
            raise Exception("Créneau introuvable")
        
        groupe = self.groupe_repo.trouver_par_id(id_groupe)
        if not groupe:
            raise Exception("Groupe introuvable")
        
        if self.creneau_repo.verifier_creneau_disponible(date):
            raise Exception("Ce créneau est déjà réservé.")
        
        self.res_repo.enregistrer(date, id_creneau, id_groupe, type_evenement)

    def reservation_multiple(self, date, id_groupe, type_evenement, liste_creneaux):
        # creneau = self.creneau_repo.trouver_par_id(id_creneau)

        # if not creneau:
        #     raise Exception("Créneau introuvable")
        
        groupe = self.groupe_repo.trouver_par_id(id_groupe)
        if not groupe:
            raise Exception("Groupe introuvable")
        
        if self.creneau_repo.verifier_creneau_disponible(date):
            raise Exception("Ce créneau est déjà réservé.")
        
        self.res_repo.reserver_plusieurs_creneaux(date, id_groupe, type_evenement, liste_creneaux)

    def lister_reservations(self):
        return self.res_repo.afficher_reservations()
    
    def export_planing_csv(self, date):

        result = self.res_repo.recuperer_planning_par_date(date)

        if not result:
            print("Aucune réservation trouvée pour cette date.")
            return

        nom_fichier = f"planning_journalier_{date}.csv"

        with open(nom_fichier, mode="w", newline="", encoding="utf-8") as file:
            ecrire = csv.writer(file, delimiter=';')

            # En-têtes
            ecrire.writerow([
                "Heure début",
                "Heure fin",
                "Groupe",
                "Motif",
                "Responsable"
            ])

            # Lignes
            for ligne in result:
                ecrire.writerow([
                    ligne["heure_debut"],
                    ligne["heure_fin"],
                    ligne["groupe"],
                    ligne["type_evenement"],
                    ligne["responsable"]
                ])

        print(f"Export terminé : {nom_fichier}")