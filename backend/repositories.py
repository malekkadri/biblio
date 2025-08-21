from typing import List, Tuple
from database import Database

class UtilisateurRepo:
    def __init__(self, db: Database):
        self.db = db

    def create(self, id: int, nom: str, prenom: str, email: str, tel: str, mdp: str):
        self.db.query(
            "INSERT INTO utilisateur (id, nom, prenom, email, tel, mot_de_passe) VALUES (?, ?, ?, ?, ?, ?);",
            (id, nom, prenom, email, tel, mdp)
        )

    def all(self) -> List[Tuple]:
        return self.db.query("SELECT id, nom, prenom, email, tel FROM utilisateur;", fetch=True)

class LivreRepo:
    # Sans changement

    def __init__(self, db: Database):
        self.db = db

    def disponibles(self) -> List[Tuple]:
        return self.db.query(
            "SELECT identifiant, titre, auteur, disponible, categorie FROM livre WHERE disponible = 1;",
            fetch=True
        )

    def all(self) -> List[Tuple]:
        return self.db.query(
            "SELECT identifiant, titre, auteur, disponible, categorie FROM livre;",
            fetch=True
        )

    def set_disponible(self, identifiant: int, dispo: int):
        self.db.query("UPDATE livre SET disponible = ? WHERE identifiant = ?;", (dispo, identifiant))

class BibliothequeRepo:
    def __init__(self, db: Database):
        self.db = db

    def all(self) -> List[Tuple]:
        return self.db.query("SELECT num, categorie FROM bibliotheque;", fetch=True)

class EmpruntRepo:
    def __init__(self, db: Database):
        self.db = db

    def create(self, id_livre: int, id_utilisateur: int, num_biblio: int, date_emprunter: str, date_remettre: str):
        self.db.query(
            "INSERT INTO emprunt (id_livre, id_utilisateur, num_biblio, date_emprunter, date_remettre) VALUES (?, ?, ?, ?, ?);",
            (id_livre, id_utilisateur, num_biblio, date_emprunter, date_remettre)
        )

    def mark_returned(self, emprunt_id: int):
        self.db.query("UPDATE emprunt SET returned = 1 WHERE id = ?;", (emprunt_id,))

    def all(self) -> List[Tuple]:
        return self.db.query(
            "SELECT id, id_livre, id_utilisateur, num_biblio, date_emprunter, date_remettre, returned FROM emprunt;",
            fetch=True
        )