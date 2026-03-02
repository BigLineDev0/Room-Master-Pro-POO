from Services.auth_service import AuthService
from Services.creneau_service import CreneauService
from Services.groupe_service import GroupeService
from Services.reservation_service import ReservationService
from Models.creneaux import Creneau
from Models.utilisateur import Utilisateur
from Models.groupe import Groupe
from datetime import datetime

from validation.chaine_valide import valider_chaine, valider_email, valider_pwd

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
                    try:
                        nom = valider_chaine("Nom : ").strip()
                        prenom = valider_chaine("Prénom : ").strip()
                        email = valider_email("Email : ").strip()
                        password = valider_pwd("Mot de passe : ").strip()

                        self.auth_service.inscription(nom, prenom, email, password)
                        print("Inscription reussie")

                    except Exception as e:
                        print("ERREUR : ",e)

                case '2':
                    email = input("Email : ").strip()
                    password = input("Mot de passe : ").strip()

                    user = self.auth_service.connexion(email, password)

                    if user and user.role == 'admin':
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
            print("\n", "-" * 10, "ROOM MASTER PRO GESTION PLANING", "-" * 10)

            print("1: Créer un groupe  \n" \
                "2. Créer un créneaux \n" \
                "3. Voir les groupes \n" \
                "4. Planing journalier \n" \
                "5. Effecturer une réservation \n" \
                "6. Voir Reservations \n" \
                "7. Export planning journalier \n" \
                "0. Quitter"
            )
            print("-" * 40)

            choix = input("\nChoix: ")

            match choix:

                case '1':
                    try:
                        nom = input('Nom du groupe: ').strip()
                        responsable = input("Responsable : ").strip()

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
                             
                    date_str = input("Entrer la date (YYYY-MM-DD): ")
                    date_choisie = datetime.strptime(date_str, "%Y-%m-%d").date()

                    print("\nPLANING DU ", date_choisie)
                    planing = self.creneau_service.planing(date_choisie)

                    if not planing:
                        print("Aucun planing.")
                    else:
                        for p in planing:
                            if p['nom_groupe']:
                                statut = p['nom_groupe']
                            else:
                                statut = '[LIBRE]'

                            if p['date']:
                                statut_date = p['date']
                            else:
                                statut_date = '[Non Programme]'

                            print(f"{p['heure_debut']} - {p['heure_fin']} - {statut_date}- {statut} - {p['type_evenement']}")
                

                case '5':
                    try:
                        date_str = input("Entrer la date (YYYY-MM-DD): ")
                        date_choisie = datetime.strptime(date_str, "%Y-%m-%d").date()

                        print("\nGroupes")
                        groupes = self.groupe_service.lister_groupe()

                        if not groupes:
                            print("Aucun groupe trouvé.")
                        else:
                            for g in groupes:
                                print(f"{g['id']} | Groupe: {g['nom']} - Responsable: {g['responsable']}")

                        id_groupe = int(input("ID Groupe: "))

                        print("\nCrenaux")
                        creneaux_disponibles = self.creneau_service.obtenir_disponibles_par_date(date_choisie)

                        if not creneaux_disponibles:
                            print("Aucun creneau disponible pour cette date.")
                        else:
                            for c in creneaux_disponibles:
                                print(f"{c['id']} | {c['heure_debut']} - {c['heure_fin']}")

                        # id_creneau = int(input("ID Créneau: "))

                        saisie = input("ID Créneaux plussieurs creneaux separe par des virgules (1,2,3) : ")

                        # Transformer "1,2,3" en liste [1,2,3]
                        liste_creneaux = [int(x.strip()) for x in saisie.split(",")]

                        type_evenement = input("Type événement: ")

                        self.res_service.reservation_multiple(date_choisie, id_groupe, type_evenement, liste_creneaux)
                        print("Réservation créé avec succès")

                    except Exception as e:
                        print("ERREUR : ",e)

                        for c in creneaux_disponibles:
                            print(f"{c['id']} | {c['heure_debut']} - {c['heure_fin']}")

                case '6':
                    reservations = self.res_service.lister_reservations()

                    if not reservations:
                        print("Aucune réservation")
                    else:
                        for r in reservations:
                            print(f"Date: {r['date']} | {r['nom_groupe']}: [{r['heure_debut']} - {r['heure_fin']}] - Evenement: {r['type_evenement']}")

                case '7':
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