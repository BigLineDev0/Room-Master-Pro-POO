from config.database import get_connection
from Models.creneaux import Creneau

class CreneauRpository:
    
    def enregistrer(self, creneau: Creneau):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO creneaux (heure_debut, heure_fin) VALUES(%s,%s)",
                (creneau.heure_debut, creneau.heure_fin)
            )
            conn.commit()

        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def creneau_exist(self, heure_debut, heure_fin):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            query = """
                SELECT id FROM creneaux
                WHERE heure_debut=%s AND heure_fin=%s
            """

            cursor.execute(query, (heure_debut, heure_fin))
            result = cursor.fetchone()

            return result is not None
            
        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def trouver_par_id(self, id_creneau):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id, heure_debut, heure_fin FROM creneaux WHERE id=%s", 
                (id_creneau,)
            )
            result = cursor.fetchone()

            return result is not None
            
        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def verifier_creneau_disponible(self, date_choisie):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # cursor.execute(
            #     """
            #     # SELECT c.id, c.heure_debut, c.heure_fin
            #     # FROM creneaux c
            #     # INNER JOIN reservations r
            #     #     ON c.id = r.id_creneau
            #     #     AND r.statut = 'Valide'
            #     # WHERE r.date = %s

            #     """
            #     (date_choisie,)
            # )

            query = """
                SELECT 
                    c.id,
                    c.heure_debut,
                    c.heure_fin
                FROM reservations r
                JOIN reservation_creneaux rc 
                    ON r.id = rc.id_reservation
                JOIN creneaux c 
                    ON c.id = rc.id_creneau
                WHERE r.date = %s
                AND r.statut = 'Valide'
                ORDER BY c.heure_debut
                """
            cursor.execute(query, (date_choisie,))

            result = cursor.fetchone()

            return result is not None
            
        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def creneau_disponibles(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT c.*
                FROM creneaux c
                LEFT JOIN reservations r 
                    ON c.id = r.id_creneau 
                    AND r.statut = 'Valide'
                WHERE r.id IS NULL
                """
            )


            return cursor.fetchall()
        
        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def creneau_disponibles_par_date(self, date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # query = """
            #     SELECT c.id, c.heure_debut, c.heure_fin
            #     FROM creneaux c
            #     LEFT JOIN reservations r
            #         ON c.id = r.id_creneau
            #         AND r.date = %s
            #         AND r.statut = 'Valide'
            #     WHERE r.id IS NULL
            #     """
            
            query = """
                SELECT c.id, c.heure_debut, c.heure_fin
                FROM creneaux c
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM reservations r
                    JOIN reservation_creneaux rc 
                        ON r.id = rc.id_reservation
                    WHERE r.date = %s
                    AND r.statut = 'Valide'
                    AND rc.id_creneau = c.id
                )
                ORDER BY c.heure_debut
                """
            cursor.execute(query, (date,))

            return cursor.fetchall()
        
        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def afficher_tout(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM creneaux")
            return cursor.fetchall()

        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def afficher_planing(self, date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # cursor.execute(
            #     """
            #     SELECT 
            #         c.id,
            #         c.heure_debut,
            #         c.heure_fin,
            #         g.nom AS nom_groupe
            #     FROM creneaux c
            #     LEFT JOIN reservations r 
            #         ON c.id = r.id_creneau 
            #         AND r.statut = 'Valide'
            #     LEFT JOIN groupes g 
            #         ON r.id_groupe = g.id
            #     """
            # )

            query = """
            SELECT 
                c.heure_debut,
                c.heure_fin,
                g.nom AS nom_groupe,
                r.type_evenement,
                r.date
            FROM creneaux c
            LEFT JOIN reservation_creneaux rc 
                ON c.id = rc.id_creneau
            LEFT JOIN reservations r 
                ON r.id = rc.id_reservation
                AND r.date = %s
                AND r.statut = 'Valide'
            LEFT JOIN groupes g 
                ON g.id = r.id_groupe
            ORDER BY c.heure_debut
            """
            cursor.execute(query, (date,))
            return cursor.fetchall()

        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()