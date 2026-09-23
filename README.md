# Plateforme éditoriale — backend Django

Module 1 du projet : modèles de données. Correspond au MCD étudié dans le mémoire
(rôles, utilisateurs, dépêches, médias, historique/traçabilité, clients, abonnements, diffusion).

## Installation

```bash
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata roles_initiaux   # crée les 6 rôles métier
python manage.py createsuperuser           # pour accéder à /admin/
python manage.py runserver
```

Puis ouvrir http://127.0.0.1:8000/admin/ — tu peux créer des utilisateurs,
des dépêches, des catégories, des clients et des abonnements directement
depuis l'interface d'administration Django (déjà connectée aux modèles).

## Ce qui est fait (module 1)

- `editorial/models.py` — tous les modèles du MCD
- `editorial/admin.py` — interface de gestion (avec historique et médias inline sur chaque dépêche)
- Modèle utilisateur personnalisé (`Utilisateur`) rattaché à un `Role`
- Fixture de rôles initiaux

## À venir

- Module 2 : API REST (endpoints par rôle, permissions, transitions de statut)
- Module 3 : authentification JWT
- Module 4 : front-end React connecté à l'API
