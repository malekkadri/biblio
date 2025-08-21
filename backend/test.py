from fastapi import FastAPI, HTTPException , Form 
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import Database
from repositories import UtilisateurRepo, LivreRepo, BibliothequeRepo, EmpruntRepo  
from models import UtilisateurCreate, UtilisateurRead, LivreRead, BibliothequeRead, EmpruntCreate, EmpruntRead

app = FastAPI(title="Bibliotheque API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database("biblio.db")
user = UtilisateurRepo(db)
livre = LivreRepo(db)
bibo = BibliothequeRepo(db)
emprunt = EmpruntRepo(db)

@app.post("/utilisateur", response_model=dict)
def create_user_form(
    id: int = Form(...),
    nom: str = Form(...),
    prenom: str = Form(...),
    email: str = Form(...),
    tel: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Les mots de passe ne correspondent pas")
    try:
        user.create(id, nom, prenom, email, tel, password)
        return {"message": "Utilisateur créé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/utilisateur", response_model=List[UtilisateurRead])
def list_users():
    rows = user.all()
    return [UtilisateurRead(id=r[0], nom=r[1], prenom=r[2], email=r[3], tel=r[4]) for r in rows]

@app.get("/livre", response_model=List[LivreRead])
def list_livres(disponible: int | None = None):
    rows = livre.disponibles() if disponible == 1 else livre.all()
    return [LivreRead(identifiant=r[0], titre=r[1], auteur=r[2], disponible=r[3], categorie=r[4]) for r in rows]

@app.get("/bibliotheque", response_model=List[BibliothequeRead])
def list_bibo():
    rows = bibo.all()
    return [BibliothequeRead(num=r[0], categorie=r[1]) for r in rows]
@app.post("/emprunt", response_model=dict)
def create_emprunt_form(
    id_livre: int = Form(...),
    id_utilisateur: int = Form(...),
    num_biblio: int = Form(...),
    date_emprunter: str = Form(...),
    date_remettre: str = Form(...)
):
    all_books = livre.all()
    found = [r for r in all_books if r[0] == id_livre]
    if not found:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    if found[0][3] == 0:
        raise HTTPException(status_code=400, detail="Livre déjà emprunté")
    
    emprunt.create(id_livre, id_utilisateur, num_biblio, date_emprunter, date_remettre)
    livre.set_disponible(id_livre, 0)
    return {"message": "Emprunt enregistré"}

@app.get("/emprunt", response_model=List[EmpruntRead])
def list_emprunt():
    rows = emprunt.all()
    return [EmpruntRead(id=r[0], id_livre=r[1], id_user=r[2],
            num_biblio=r[3], date_emprunter=r[4], 
            date_remettre=r[5], returned=r[6]) for r in rows]
@app.post("/retours/{emprunt_id}", response_model=dict)
def retour_emprunt(emprunt_id: int):
    emprunt.mark_returned(emprunt_id)
    rows = emprunt.all()
    row = next((r for r in rows if r[0] == emprunt_id), None)
    if row:
        livre.set_disponible(row[1], 1)
    return {"message": "Retour enregistré"}

@app.get("/emprunt", response_model=List[EmpruntRead])
def list_emprunt():
    rows = emprunt.all()
    return [EmpruntRead(id=r[0], id_livre=r[1], id_user=r[2], num_biblio=r[3], date_emprunter=r[4], date_remettre=r[5], returned=r[6]) for r in rows]

@app.get("/")
def root():
    return {"message": "Bienvenue à l'API de la Bibliothèque!"}
