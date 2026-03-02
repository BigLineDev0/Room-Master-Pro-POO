from Models.groupe import Groupe
from config.database import get_connection

class GroupeRepository:
    
    def enregistrer(self, groupe: Groupe):
        conn = get_connection()
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO groupes(nom, responsable) VALUES(%s,%s)",
                (groupe.nom, groupe.responsable)
            )
            conn.commit()
        except ValueError as e:
            print("ERREUR : ", e)

        finally:
            cursor.close()
            conn.close()

    def exist_groupe(self, nom, responsable):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM groupes WHERE nom=%s AND responsable=%s",
                (nom, responsable)
            )
            result = cursor.fetchone()

            return result is not None
        
        except ValueError as e:
            print("ERREUR : ", e)

        finally:
            cursor.close()
            conn.close()

    def trouver_par_id(self, id_groupe):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, nom, responsable FROM groupes WHERE id=%s", 
                (id_groupe,)
            )
            result = cursor.fetchone()

            return result is not None
            
        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def afficher_tout(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM groupes")
            return cursor.fetchall()

            
        except ValueError as e:
            print("ERREUR : ", e)

        finally:
            cursor.close()
            conn.close()
