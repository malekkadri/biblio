import sqlite3
from contextlib import contextmanager

class Database:
    def __init__(self, db_path: str = "database/biblio.db"):
        self.db_path = db_path
        self.verifier_structure()

    @contextmanager
    def connect(self):
        conn = None
        try:
            conn=sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.commit()
                conn.close()

    def verifier_structure(self):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables_existantes = [row[0] for row in cursor.fetchall()]
                if len(tables_existantes) != 4:
                    print(f"Attention: Tables trouvées: {tables_existantes}")
                
        except sqlite3.Error as e:
            print(f"Erreur la connexion a la base {e}")
            raise e
