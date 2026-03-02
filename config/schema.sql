CREATE DATABASE room_master;
USE room_master;

CREATE TABLE utilisateurs(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100)  NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(200) NOT NULL,
    role ENUM('admin', 'manager') DEFAULT 'admin'
);

CREATE TABLE groupes(
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    responsable VARCHAR(100) NOT NULL
);

CREATE TABLE creneaux (
    id INT AUTO_INCREMENT PRIMARY KEY,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL
);

CREATE TABLE reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    id_creneau INT NOT NULL,
    id_groupe INT NOT NULL,
    type_evenement VARCHAR(100),
    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('Valide','Annule') DEFAULT 'Valide',
    UNIQUE (date, id_creneau),
    FOREIGN KEY (id_creneau) REFERENCES creneaux(id),
    FOREIGN KEY (id_groupe) REFERENCES groupes(id)
);
-- ON GERE JUSTE LE PLANNING JOURNALIER UNE SEULE DATE
-- RESERVER POUR UNE DATE DONNEE

SELECT c.id, c.heure_debut, c.heure_fin
FROM creneaux c
LEFT JOIN reservations r
    ON c.id = r.id_creneau
    AND r.date = '2026-03-02'
    AND r.statut = 'Valide'
WHERE r.id IS NULL;

SELECT 
    c.heure_debut,
    c.heure_fin,
    g.nom AS groupe,
    r.type_evenement,
    g.responsable
FROM reservations r
INNER JOIN creneaux c ON c.id = r.id_creneau
INNER JOIN groupes g ON g.id = r.id_groupe
WHERE r.statut = 'Valide'
ORDER BY c.heure_debut;

