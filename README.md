# Congel API

API FastAPI (Python) avec connexion PostgreSQL — backend pour l'app Flutter de gestion de congélateur.

## Structure

```
congelApi/
├── main.py                # Point d'entrée (importe app.main:app)
├── app/
│   ├── config.py          # Réglages (variables d'env / .env)
│   ├── database.py        # Moteur SQLAlchemy + session + get_db()
│   ├── models.py          # Modèles ORM (table produits)
│   ├── schemas.py         # Schémas Pydantic (entrée/sortie)
│   ├── main.py            # App FastAPI + routes racine + CORS
│   └── routers/
│       └── produits.py    # CRUD /produits
├── docker-compose.yml     # PostgreSQL local
├── requirements.txt
└── .env.example
```

## Démarrage

1. Configurer l'environnement :
   ```bash
   cp .env.example .env      # adapter DATABASE_URL si besoin
   ```

2. Lancer PostgreSQL :
   ```bash
   docker compose up -d db
   ```

3. Installer les dépendances (si pas déjà fait) :
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Lancer l'API en développement :
   ```bash
   fastapi dev main.py
   ```

- API : http://127.0.0.1:8000
- Documentation interactive (Swagger) : http://127.0.0.1:8000/docs

## Routes

| Méthode | Chemin                  | Description                |
|---------|-------------------------|----------------------------|
| GET     | `/`                     | Message de bienvenue       |
| GET     | `/health`               | Contrôle de santé          |
| GET     | `/produits`             | Liste des produits         |
| POST    | `/produits`             | Créer un produit           |
| GET     | `/produits/{id}`        | Détail d'un produit        |
| PATCH   | `/produits/{id}`        | Modifier un produit        |
| DELETE  | `/produits/{id}`        | Supprimer un produit       |

## Migrations (optionnel)

Les tables sont créées automatiquement au démarrage (pratique en dev). Pour la
production, utiliser Alembic (déjà installé) : `alembic init migrations`.
