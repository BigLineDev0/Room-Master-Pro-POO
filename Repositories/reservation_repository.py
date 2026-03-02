from config.database import get_connection

class ReservationRepository:

    def enregistrer(self, date, id_creneau, id_groupe, type_evenement):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO reservations (date, id_creneau, id_groupe, type_evenement) VALUES(%s,%s,%s,%s)",
                (date, id_creneau, id_groupe, type_evenement)
            )
            conn.commit()

        except ValueError as e:
            print("ERREUR : ", e)
        finally:
            cursor.close()
            conn.close()

    def reserver_plusieurs_creneaux(self, date, id_groupe, type_evenement, liste_creneaux):
        conn = get_connection()
        cursor = conn.cursor()

        try:
            conn.start_transaction()

            # Vérifier conflits
            format_strings = ','.join(['%s'] * len(liste_creneaux))
            query = f"""
                SELECT rc.id_creneau
                FROM reservations r
                JOIN reservation_creneaux rc ON r.id = rc.id_reservation
                WHERE r.date = %s
                AND r.statut = 'Valide'
                AND rc.id_creneau IN ({format_strings})
            """
            
            cursor.execute(query, [date] + liste_creneaux)
            conflits = cursor.fetchall()

            if conflits:
                print("Certains créneaux sont déjà réservés.")
                conn.rollback()
                return

            # Créer réservation
            cursor.execute("""
                INSERT INTO reservations (date, id_groupe, type_evenement)
                VALUES (%s, %s, %s)
            """, (date, id_groupe, type_evenement))

            reservation_id = cursor.lastrowid

            # Insérer créneaux
            for creneau_id in liste_creneaux:
                cursor.execute("""
                    INSERT INTO reservation_creneaux (id_reservation, id_creneau)
                    VALUES (%s, %s)
                """, (reservation_id, creneau_id))

            conn.commit()

        except Exception as e:
            conn.rollback()
            print("Erreur :", e)

        finally:
            cursor.close()
            conn.close()
    
    def afficher_reservations(self):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # cursor.execute(
            #     """
            #     SELECT 
            #         r.id,
            #         r.date,
            #         r.type_evenement,
            #         g.nom AS nom_groupe,
            #         c.heure_debut AS heure_debut,
            #         c.heure_fin AS heure_fin
            #     FROM reservations r
            #     JOIN creneaux c
            #         ON r.id_creneau = c.id
            #     JOIN groupes g 
            #         ON r.id_groupe = g.id
            #     ORDER BY r.date
            #     """
            # )

            cursor.execute("""
                SELECT 
                    r.id,
                    r.date,
                    r.type_evenement,
                    g.nom AS nom_groupe,
                    c.heure_debut AS heure_debut,
                    c.heure_fin AS heure_fin
                FROM creneaux c
                JOIN reservation_creneaux rc 
                    ON c.id = rc.id_creneau
                JOIN reservations r
                    ON r.id = rc.id_reservation
                JOIN groupes g 
                    ON r.id_groupe = g.id
                ORDER BY r.date
                """
            )

            return cursor.fetchall()

        except ValueError as e:
            print("ERREUR : ",e)
        
        finally:
            cursor.close()
            conn.close()

    def recuperer_planning_par_date(self, date):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # query = """
            #     SELECT 
            #         c.heure_debut,
            #         c.heure_fin,
            #         g.nom AS groupe,
            #         r.type_evenement,
            #         g.responsable
            #     FROM reservations r
            #     INNER JOIN creneaux c ON c.id = r.id_creneau
            #     INNER JOIN groupes g ON g.id = r.id_groupe
            #     WHERE r.statut = 'Valide'
            #     AND r.date = %s
            #     ORDER BY c.heure_debut
            # """
            query = """
                SELECT 
                    c.heure_debut,
                    c.heure_fin,
                    g.nom AS groupe,
                    r.type_evenement,
                    g.responsable
                FROM reservations r
                JOIN reservation_creneaux rc 
                    ON r.id = rc.id_reservation
                JOIN groupes g
                    ON g.id = r.id_groupe
                JOIN creneaux c 
                    ON c.id = rc.id_creneau
                WHERE r.date = %s
                AND r.statut = 'Valide'
                ORDER BY c.heure_debut
                """
            
            cursor.execute(query, (date,))
            return cursor.fetchall()
        
        except ValueError as e:
            print("ERREUR : ",e)

        finally:
            cursor.close()
            conn.close()