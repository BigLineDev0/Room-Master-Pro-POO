from Services.auth_service import AuthService
from Services.creneau_service import CreneauService
from Services.groupe_service import GroupeService
from Services.reservation_service import ReservationService
from Models.creneaux import Creneau
from Models.groupe import Groupe
from datetime import datetime

class Application:
    def __init__(self):
        self.auth_service = AuthService()
        self.creneau_service = CreneauService()
        self.groupe_service = GroupeService()
        self.res_service = ReservationService()

        self.user_connecte = None

    def menu_auth(self):
        while not self.user_connecte:
            print("\n", "-" * 10, "AUTHENTIFICATION", "-" * 10)
            print("1. Inscription")
            print("2. Connexion \n")
            

            choix = input("Choix: ")

            match choix:
                case '1':
                    nom = input("Nom : ")
                    prenom = input("Prénom : ")
                    email = input("Email : ")
                    password = input("Mot de passe : ")

                    self.auth_service.inscription(nom, prenom, email, password)
                    print("Inscription reussie")

                case '2':
                    email = input("Email : ")
                    password = input("Mot de passe : ")

                    user = self.auth_service.connexion(email, password)

                    if user:
                        self.user_connecte = user
                        print(f"Bienvenue {user.prenom} {user.nom}")
                        self.menu_principale()
                    else:
                        print("Email ou Mot de passe incorrect.")
                        self.menu_auth()

                case _:
                    print("Choix invalide")


    def menu_principale(self):

        while True:
            print("\n", "-" * 10, "ROOM MASTER PRO", "-" * 10)

            print("1: Créer un groupe  \n" \
                "2. Créer un créneaux \n" \
                "3. Voir les groupes \n" \
                "4. Planing journalier \n" \
                "5. Effecturer une réservation \n" \
                "6. Vue Disponibilités \n" \
                "7. Voir Reservations \n" \
                "8. Export planning journalier \n" \
                "0. Quitter"
            )
            print("-" * 40)

            choix = input("\nChoix: ")

            match choix:

                case '1':
                    try:
                        nom = input("Nom du Groupe : ")
                        responsable = input("Responsable : ")

                        self.groupe_service.creer_groupe(Groupe(nom, responsable))
                        print("Groupe créé avec succès")
                        
                    except Exception as e:
                        print("ERREUR : ",e)

                case '2':
                    try:
                       
                        heure_debut_str = input("Heure début (HH:MM) : ")
                        heure_fin_str = input("Heure fin (HH:MM) : ")

                        # convertir heure
                        heure_debut = datetime.strptime(heure_debut_str, "%H:%M").time()
                        heure_fin = datetime.strptime(heure_fin_str, "%H:%M").time()
                        
                        self.creneau_service.creer_creneau(Creneau(heure_debut, heure_fin))
                        print("Créneau créé avec succès")
                    
                    except ValueError:
                        print("Format d'heure invalide. Utilise HH:MM")
                    except Exception as e:
                        print("Erreur :", e)

                case '3':
                    print("\nGROUPES")
                    groupes = self.groupe_service.lister_groupe()

                    if not groupes:
                        print("Aucun groupe trouvé.")
                    else:
                        for g in groupes:
                            print(f"{g['id']} | Groupe: {g['nom']} - Responsable: {g['responsable']}")

                case '4':
                             
                    print("\nPLANING JOURNALIER")
                    planing = self.creneau_service.planing()

                    if not planing:
                        print("Aucun planing.")
                    else:
                        for p in planing:
                            if p['nom_groupe']:
                                statut = p['nom_groupe']
                            else:
                                statut = '[LIBRE]'

                            print(f"{p['id']} | {p['heure_debut']} - {p['heure_fin']} - {statut}")
                
                case '5':
                    try:
                        date_str = input("Entrer la date (YYYY-MM-DD): ")
                        date_choisie = datetime.strptime(date_str, "%Y-%m-%d").date()

                        print("\nCrenaux")
                        creneaux_disponibles = self.creneau_service.obtenir_disponibles_par_date(date_choisie)

                        if not creneaux_disponibles:
                            print("Aucun creneau disponible pour cette date.")
                        else:
                            for c in creneaux_disponibles:
                                print(f"{c['id']} | {c['heure_debut']} - {c['heure_fin']}")

                        id_creneau = int(input("ID Créneau: "))

                        print("\nGroupes")
                        groupes = self.groupe_service.lister_groupe()

                        if not groupes:
                            print("Aucun groupe trouvé.")
                        else:
                            for g in groupes:
                                print(f"{g['id']} | Groupe: {g['nom']} - Responsable: {g['responsable']}")

                        id_groupe = int(input("ID Groupe: "))

                        type_evenement = input("Type événement: ")

                        self.res_service.reserver(date_choisie, id_creneau, id_groupe, type_evenement)
                        print("Réservation créé avec succès")
                        
                    except Exception as e:
                        print("ERREUR : ",e)

                case '6':
                    print("\nCRENEAUX DISPONIBLES")
                    creneaux_disponibles = self.creneau_service.lister_creneau_disponible()

                    if not creneaux_disponibles:
                        print("Aucun creneau disponible.")
                    else:
                        for c in creneaux_disponibles:
                            print(f"{c['id']} | {c['heure_debut']} - {c['heure_fin']}")

                case '7':
                    reservations = self.res_service.lister_reservations()

                    if not reservations:
                        print("Aucune réservation")
                    else:
                        for r in reservations:
                            print(f"{r['nom_groupe']}: [{r['heure_debut']} - {r['heure_fin']}] - Evenement: {r['type_evenement']} - Date: {r['date']}")

                case '8':
                    try:
                        date_str = input("Entrer la date (YYYY-MM-DD): ")
                        date_choisie = datetime.strptime(date_str, "%Y-%m-%d").date()
                    
                        self.res_service.export_planing_csv(date_choisie)
                    except ValueError:
                        print("Format de date invalide.")
                        return
                    
                case '0':
                    print('Au revoir')
                    break
                case _:
                    print("Choix invalide.")

app = Application()
app.menu_auth()