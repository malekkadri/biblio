import sqlite3
from datetime import datetime

class utilisateur:
    def __init__(self, bd):
        self.bd = bd
    
    def creer(self, id, nom, prenom, email, tel, mdp):
        try:
            with self.bd.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                "INSERT INTO utilisateur (id, nom, prenom, email, tel, mot_de_passe) VALUES (?, ?, ?, ?, ?, ?)",
                (id, nom, prenom, email, tel, mdp)
            )
            return {
                'success': True,
                'message': 'Utilisateur créé avec succès'
            }
        except sqlite3.IntegrityError:
            return {
                'success': False,
                'message': "cet email est deja utilisé"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur : {str(e)}'
            }

    def verifier_identifiants(self, email, mot_de_passe):
        try:
            with self.bd.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id, nom, prenom, mot_de_passe FROM utilisateur WHERE email = ?",
                    (email,)
                )
                row = cursor.fetchone()
                if row and row["mot_de_passe"] == mot_de_passe:
                    return {
                        'success': True,
                        'message': 'Connexion réussie',
                        'utilisateur': {
                            'id': row['id'],
                            'nom': row['nom'],
                            'prenom': row['prenom']
                        }
                    }
                return {
                    'success': False,
                    'message': 'Email ou mot de passe incorrect'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur : {str(e)}'
            }
        

class livre:
    def __init__(self, bd):
        self.bd = bd
    
    def get_disponibles(self):
        try:
            with self.bd.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT l.identifiant, l.titre, l.auteur, l.disponible, b.categorie 
                FROM livre l
                LEFT JOIN bibliotheque b ON l.categorie = b.categorie
                WHERE l.disponible = 1
                ORDER BY l.titre
                ''')
                livres = []
                for row in cursor.fetchall():
                    livres.append({
                        'identifiant': row['identifiant'],
                        'titre': row['titre'],
                        'auteur': row['auteur'],
                        'disponible': row['disponible'],
                        'categorie': row['categorie'] or 'Non spécifiée'
                    })
                return {
                    'success': True,
                    'livres': livres
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur : {str(e)}'
            }

# emprunt
class emprunt:
    def __init__(self, bd):
        self.bd = bd
    
    def creer(self, id_utilisateur, id_livre, date_remettre, num_biblio=None):
        try:
            with self.bd.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT disponible FROM livre WHERE identifiant = ?', (id_livre,))
                livre = cursor.fetchone()
                if not livre or not livre['disponible']:
                    return {
                        'success': False,
                        'message': "Ce livre n'est pas disponible"
                    }

                date_emprunter = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(
                    '''INSERT INTO emprunt (id_utilisateur, id_livre, num_biblio, date_emprunter, date_remettre, returned)
                    VALUES (?, ?, ?, ?, ?, 0)''',
                    (id_utilisateur, id_livre, num_biblio, date_emprunter, date_remettre)
                )

                cursor.execute('UPDATE livre SET disponible = 0 WHERE identifiant = ?', (id_livre,))
                return {
                    'success': True,
                    'message': 'Livre emprunté avec succès'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Erreur: {str(e)}'
            }

