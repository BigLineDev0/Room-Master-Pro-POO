from config.database import get_connection
from Models.utilisateur import Utilisateur

class UserRepository:
    def trouver_par_email(self, email):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT nom, prenom, email, mot_de_passe, role FROM utilisateurs WHERE email = %s",
                (email,))
            row = cursor.fetchone()

            if not row:
                
                return None

            return Utilisateur(*row)
        
        except ValueError as e:
            print("ERREUR : ", e)
        finally:
            cursor.close()
            conn.close()

    def enregistrer(self, nom, prenom, email, password_hash):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe) VALUES(%s,%s,%s,%s)",
                (nom, prenom, email, password_hash)
            )

            conn.commit()

        except ValueError as e:
            print("ERREUR : ", e)
        finally:
            cursor.close()
            conn.close()
