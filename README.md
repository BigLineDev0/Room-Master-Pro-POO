# Room Master - Système de Gestion de Réservations de Salle

## Decscription

Room Master est une application en ligne de commande développée en Python permettant de gérer un planning journalier de réservation de créneaux horaires pour des groupes.

Le système permet :

- Gestion des utilisateurs (admin / manager)
- Gestion des groupes
- Gestion des créneaux horaires
- Réservation simple ou multiple de créneaux
- Vérification des disponibilités par date
- Affichage du planning journalier
- Export CSV des réservations validées

---

## Architecture du Projet

Le projet suit une architecture en couches :

### Couches

- **Repository** → Accès aux données (requêtes SQL)
- **Service** → Logique métier
- **Main/Menu** → Interface utilisateur (terminal)

---

## Base de Données

### Tables principales

#### `utilisateurs`
- id
- nom
- prenom
- email
- mot_de_passe
- role (admin / manager)

#### `groupes`
- id
- nom
- responsable

#### `creneaux`
- id
- heure_debut
- heure_fin

#### `reservations`
- id
- date
- id_groupe
- type_evenement
- statut (Valide / Annule)
- date_creation

#### `reservation_creneaux`
- id_reservation
- id_creneau

---

## Modèle Relationnel

- Une réservation peut contenir **plusieurs créneaux**
- Un créneau peut être utilisé dans plusieurs réservations (à des dates différentes)
- Relation Many-to-Many via `reservation_creneaux`

---

## Fonctionnalités principales

### Vérifier les créneaux disponibles

Affiche les créneaux libres pour une date donnée.

### Réservation simple ou multiple

- Sélection d'une date
- Sélection d'un groupe
- Sélection de plusieurs créneaux
- Vérification des conflits
- Transaction sécurisée

### Planning Journalier

Affichage complet des créneaux avec statut :

- LIBRE
- OCCUPE

### Export CSV

Export des réservations validées dans : planning_journalier_YYYY-MM-DD.csv


Contient :

- Heure début
- Heure fin
- Groupe
- Motif
- Responsable

---

## Sécurité & Bonnes Pratiques

- ✔ Requêtes paramétrées (anti SQL injection)
- ✔ Transactions pour réservation multiple
- ✔ Index SQL pour optimisation
- ✔ Contrainte d’unicité logique (date + créneau)
- ✔ Séparation des responsabilités

---

## Installation

### 1 Cloner le projet
- git clone <repo_url>
- cd room-master


### 2 Créer la base de données

Exécuter le script SQL fourni :
CREATE DATABASE room_master;
USE room_master;
-- Exécuter les tables

# Lancement du programme
Exécuter le fichier :
python main.py

Le menu interactif s’affiche et guide l’utilisateur.