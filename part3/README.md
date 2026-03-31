# HBnB — AirBnB Clone

> RESTful API · Flask · SQLAlchemy · JWT · RBAC  
> **Valentin Dardenne** — Holberton School — 2026

---

## Table of Contents

- [Project Structure](#project-structure)
- [Installation & Launch](#installation--launch)
- [API Endpoints](#api-endpoints)
- [Database Design — Merise Diagram](#database-design--merise-diagram)
- [SQL — Tables & Constraints](#sql--tables--constraints)
- [Architecture](#architecture)
- [Authentication & RBAC](#authentication--rbac)

---

## Project Structure

```
hbnb/
├── app/
│   ├── __init__.py              # Application Factory (create_app)
│   ├── api/
│   │   └── v2/
│   │       ├── auth.py          # POST /auth/login → JWT token
│   │       ├── users.py         # CRUD users + PATCH /<id>/admin
│   │       ├── places.py        # CRUD places
│   │       ├── reviews.py       # CRUD reviews
│   │       ├── amenities.py     # CRUD amenities (admin-only write)
│   │       └── bookings.py      # CRUD bookings + status lifecycle
│   ├── models/
│   │   ├── base_model.py        # BaseModel abstrait : id UUID, timestamps
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   │   └── booking.py
│   ├── services/
│   │   ├── __init__.py          # Singleton facade
│   │   └── facade.py            # HBnBFacade — orchestration + règles métier
│   └── persistence/
│       └── repository.py        # SQLAlchemyRepository + UserRepository
├── sql/
│   ├── create_tables.sql        # DDL — structure complète
│   ├── insert_initial_data.sql  # DML — données initiales (admin, amenities)
│   └── test_crud.sql            # DML — tests SELECT/INSERT/UPDATE/DELETE
├── instance/
│   └── hbnb_dev.db              # SQLite (développement)
├── run.py                       # Point d'entrée
├── config.py                    # DevelopmentConfig / ProductionConfig
└── requirements.txt
```

---

## Installation & Launch

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python run.py
```

Swagger UI disponible sur : **http://localhost:5000/api/v2/**

---

## API Endpoints

| Ressource  | Méthode  | Route                                  | Description                         | Auth        |
|------------|----------|----------------------------------------|-------------------------------------|-------------|
| **Auth**   | POST     | `/api/v2/auth/login`                  | Connexion → token JWT               | Public      |
| **Users**  | POST     | `/api/v2/users/`                      | Créer un compte                     | Public      |
|            | GET      | `/api/v2/users/`                      | Lister tous les users               | Admin       |
|            | GET      | `/api/v2/users/<id>`                  | Détail d'un user                    | Token       |
|            | PUT      | `/api/v2/users/<id>`                  | Modifier un user                    | Owner/Admin |
|            | PATCH    | `/api/v2/users/<id>/admin`            | Promouvoir/rétrograder admin        | Admin       |
| **Places** | POST     | `/api/v2/places/`                     | Créer un logement                   | Token       |
|            | GET      | `/api/v2/places/`                     | Lister tous les logements           | Public      |
|            | GET      | `/api/v2/places/<id>`                 | Détail d'un logement                | Public      |
|            | PUT      | `/api/v2/places/<id>`                 | Modifier un logement                | Owner/Admin |
| **Reviews**| POST     | `/api/v2/reviews/`                    | Créer une review                    | Token       |
|            | GET      | `/api/v2/reviews/`                    | Lister toutes les reviews           | Public      |
|            | GET      | `/api/v2/reviews/<id>`                | Détail d'une review                 | Public      |
|            | PUT      | `/api/v2/reviews/<id>`                | Modifier une review                 | Owner/Admin |
|            | DELETE   | `/api/v2/reviews/<id>`                | Supprimer une review                | Owner/Admin |
|            | GET      | `/api/v2/places/<id>/reviews`         | Reviews d'un logement               | Public      |
| **Amenities** | POST  | `/api/v2/amenities/`                  | Créer une amenity                   | Admin       |
|            | GET      | `/api/v2/amenities/`                  | Lister toutes les amenities         | Public      |
|            | GET      | `/api/v2/amenities/<id>`              | Détail d'une amenity                | Public      |
|            | PUT      | `/api/v2/amenities/<id>`              | Modifier une amenity                | Admin       |
| **Bookings** | POST   | `/api/v2/bookings/`                   | Créer une réservation               | Token       |
|            | GET      | `/api/v2/bookings/`                   | Lister toutes les réservations      | Admin       |
|            | GET      | `/api/v2/bookings/<id>`               | Détail d'une réservation            | Owner/Admin |
|            | PUT      | `/api/v2/bookings/<id>`               | Modifier les dates / guests         | Owner/Admin |
|            | DELETE   | `/api/v2/bookings/<id>`               | Supprimer une réservation           | Owner/Admin |
|            | PATCH    | `/api/v2/bookings/<id>/status`        | Confirmer ou annuler                | Owner/Admin |
|            | GET      | `/api/v2/bookings/users/<id>`         | Réservations d'un user              | Owner/Admin |
|            | GET      | `/api/v2/bookings/places/<id>`        | Réservations d'un logement          | Token       |

---

## Database Design — Merise Diagram

Le schéma suit la méthode **Merise** en trois niveaux : MCD (conceptuel) → MLD (logique) → MPD (physique, fichier `create_tables.sql`).

### Entités

| Entité           | Attributs clés                                                                                        |
|------------------|-------------------------------------------------------------------------------------------------------|
| **USER**         | `id` CHAR(36) PK · `email` VARCHAR(120) UNIQUE · `password` VARCHAR(128) · `is_admin` BOOLEAN DEFAULT FALSE |
| **PLACE**        | `id` CHAR(36) PK · `title` VARCHAR(100) · `price` DECIMAL(10,2) · `latitude/longitude` FLOAT · `owner_id` FK→USER |
| **REVIEW**       | `id` CHAR(36) PK · `text` TEXT · `rating` INT(1–5) · `user_id` FK→USER · `place_id` FK→PLACE · UNIQUE(user_id, place_id) |
| **AMENITY**      | `id` CHAR(36) PK · `name` VARCHAR(50) UNIQUE                                                         |
| **PLACE_AMENITY**| `place_id` FK→PLACE · `amenity_id` FK→AMENITY · PK composite (place_id, amenity_id)                 |
| **BOOKING**      | `id` CHAR(36) PK · `place_id` FK→PLACE · `user_id` FK→USER · `check_in/check_out` DATE · `guests` INT≥1 · `status` pending/confirmed/cancelled |

### Associations & cardinalités

| Association                  | Type          | Implémentation SQL                                    |
|------------------------------|---------------|-------------------------------------------------------|
| USER `1` → PLACE `0,N`       | One-to-Many   | `owner_id` dans `places`                             |
| USER `1` → REVIEW `0,N`      | One-to-Many   | `user_id` dans `reviews`                             |
| USER `1` → BOOKING `0,N`     | One-to-Many   | `user_id` dans `bookings`                            |
| PLACE `1` → REVIEW `0,N`     | One-to-Many   | `place_id` dans `reviews`                            |
| PLACE `1` → BOOKING `0,N`    | One-to-Many   | `place_id` dans `bookings`                           |
| PLACE `0,N` ↔ AMENITY `0,N`  | Many-to-Many  | Table pivot `place_amenity` avec PK composite        |

### Règles de transformation MCD → MLD

1. **Règle 1** — Toute entité devient une table avec sa PK.
2. **Règle 2** — Association One-to-Many → FK dans la table côté *Many*.
3. **Règle 3** — Association Many-to-Many → table pivot avec PK composite.
4. **Règle 4** — Contrainte métier unique → contrainte `UNIQUE` (simple ou composite).

---

## SQL — Tables & Constraints

### create_tables.sql (DDL)

```sql
-- Table users
CREATE TABLE users (
    id           CHAR(36)     PRIMARY KEY,
    first_name   VARCHAR(50)  NOT NULL,
    last_name    VARCHAR(50)  NOT NULL,
    email        VARCHAR(120) NOT NULL UNIQUE,
    password     VARCHAR(128) NOT NULL,
    is_admin     BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table places
CREATE TABLE places (
    id           CHAR(36)      PRIMARY KEY,
    title        VARCHAR(100)  NOT NULL,
    description  TEXT,
    price        DECIMAL(10,2) NOT NULL,
    latitude     FLOAT         NOT NULL,
    longitude    FLOAT         NOT NULL,
    owner_id     CHAR(36)      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table reviews — 1 review max par user par place
CREATE TABLE reviews (
    id         CHAR(36) PRIMARY KEY,
    text       TEXT     NOT NULL,
    rating     INT      NOT NULL CHECK (rating BETWEEN 1 AND 5),
    user_id    CHAR(36) NOT NULL REFERENCES users(id)  ON DELETE CASCADE,
    place_id   CHAR(36) NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_review UNIQUE (user_id, place_id)
);

-- Table amenities
CREATE TABLE amenities (
    id         CHAR(36)    PRIMARY KEY,
    name       VARCHAR(50) NOT NULL UNIQUE,
    created_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Table pivot Many-to-Many Place ↔ Amenity
CREATE TABLE place_amenity (
    place_id   CHAR(36) REFERENCES places(id)    ON DELETE CASCADE,
    amenity_id CHAR(36) REFERENCES amenities(id) ON DELETE CASCADE,
    PRIMARY KEY (place_id, amenity_id)
);

-- Table bookings
CREATE TABLE bookings (
    id         CHAR(36) PRIMARY KEY,
    place_id   CHAR(36) NOT NULL REFERENCES places(id) ON DELETE CASCADE,
    user_id    CHAR(36) NOT NULL REFERENCES users(id)  ON DELETE CASCADE,
    check_in   DATE     NOT NULL,
    check_out  DATE     NOT NULL,
    guests     INT      NOT NULL DEFAULT 1 CHECK (guests >= 1),
    status     VARCHAR(20) NOT NULL DEFAULT 'pending'
                   CHECK (status IN ('pending', 'confirmed', 'cancelled')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_dates CHECK (check_out > check_in)
);
```

### Contraintes utilisées

| Contrainte          | Où                                      | Pourquoi                                                 |
|---------------------|-----------------------------------------|----------------------------------------------------------|
| `PRIMARY KEY`       | `id` CHAR(36) UUID dans chaque table    | Identifiant unique, non-null, non-dupliqué               |
| `UNIQUE`            | `users.email`, `amenities.name`         | Empêche les doublons métier                              |
| `UNIQUE` composite  | `reviews(user_id, place_id)`            | 1 review max par user par place                          |
| `FOREIGN KEY`       | Toutes les relations                    | Intégrité référentielle                                  |
| `ON DELETE CASCADE` | Toutes les FK                           | Suppression en cascade — pas d'orphelins                 |
| `CHECK`             | `rating`, `status`, `guests`, `dates`   | Validation des valeurs au niveau base de données         |
| `NOT NULL`          | Tous les champs obligatoires            | Cohérence des données                                    |
| `DEFAULT`           | `is_admin`, `status`, `created_at`      | Valeurs initiales automatiques                           |

### Pourquoi `ON DELETE CASCADE` ?

Si un `USER` est supprimé → toutes ses `PLACES`, `REVIEWS` et `BOOKINGS` sont supprimées automatiquement. Cela évite les **enregistrements orphelins** (places sans propriétaire). L'alternative `ON DELETE RESTRICT` interdirait la suppression si des enfants existent.

### Pourquoi des UUID CHAR(36) comme PK ?

Les UUID v4 sont non-prédictibles (sécurité contre l'énumération), générables sans requête DB, et compatibles avec le sharding distribué. Inconvénient : l'index B-Tree se fragmente car les UUIDs sont aléatoires (non-séquentiels).

### Normalisation 3NF

HBnB respecte la **Troisième Forme Normale** : aucun attribut non-clé ne dépend d'un autre attribut non-clé. Par exemple, `place.owner_email` n'existe pas dans `places` — ce serait une dépendance transitive via `owner_id → users.email`. Chaque attribut dépend uniquement de la PK de sa table.

> Règle mémo : *"Dépendre de la clé, toute la clé, rien que la clé."*

---

## Architecture

HBnB suit une **Three-Tier Architecture** :

```
┌─────────────────────────────────────────────┐
│  Présentation   api/v2/*.py                 │  Reçoit HTTP, valide payloads, retourne JSON
├─────────────────────────────────────────────┤
│  Logique métier  models/ + services/facade  │  Règles métier, validations, RBAC
├─────────────────────────────────────────────┤
│  Persistance    persistence/repository.py   │  SQLAlchemy, requêtes SQL, sessions DB
└─────────────────────────────────────────────┘
```

### Facade Pattern

`HBnBFacade` est un **singleton** qui découple la couche API de la persistance. L'API ne sait jamais si les données sont en mémoire, SQLite ou MySQL — elle appelle uniquement les méthodes de la Facade.

### Repository Pattern

Le `SQLAlchemyRepository` expose une interface CRUD standardisée (`add`, `get`, `get_all`, `update`, `delete`). `UserRepository` en hérite et ajoute `get_user_by_email()` pour le login. Ce pattern a rendu la migration **Part 2 (InMemory) → Part 3 (SQLAlchemy)** transparente.

### Application Factory

```python
# app/__init__.py
def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    jwt.init_app(app)
    ...
    return app
```

Permet de créer plusieurs instances avec des configs différentes (dev, test, prod) et évite les imports circulaires.

### SQLite (dev) vs MySQL (prod)

| Environnement | SGBD   | URI SQLAlchemy                                      |
|---------------|--------|-----------------------------------------------------|
| Développement | SQLite | `sqlite:///instance/hbnb_dev.db`                   |
| Production    | MySQL  | `mysql+pymysql://user:password@host/hbnb_db`        |

---

## Authentication & RBAC

### JWT — JSON Web Token

Le token est **stateless** : le serveur ne stocke aucune session. Structure : `HEADER.PAYLOAD.SIGNATURE`.

```python
# Génération du token à la connexion
access_token = create_access_token(
    identity=str(user.id),
    additional_claims={"is_admin": user.is_admin}
)

# Récupération dans un endpoint protégé
current_user_id = get_jwt_identity()   # UUID de l'utilisateur
claims = get_jwt()                     # {"is_admin": True/False, ...}
```

### RBAC — Role-Based Access Control

Deux rôles : **utilisateur normal** et **admin** (`is_admin=True`).

```python
# Pattern RBAC appliqué dans chaque endpoint sensible
is_admin = claims.get("is_admin", False)
if resource.owner_id != current_user_id and not is_admin:
    abort(403, "Unauthorized action")
```

Les admins bypasse toutes les vérifications d'ownership.

### Codes d'erreur HTTP

| Code | Signification                          | Exemple dans HBnB                                |
|------|----------------------------------------|--------------------------------------------------|
| 400  | Bad Request — données invalides        | Review sur sa propre place, `is_admin` dans PUT  |
| 401  | Unauthorized — token manquant/invalide | Accès sans token à un endpoint protégé           |
| 403  | Forbidden — droits insuffisants        | Modifier la place d'un autre user                |
| 409  | Conflict — état incompatible           | Dates de réservation qui se chevauchent          |

### Sécurité des mots de passe

Les mots de passe sont hashés avec **bcrypt** (salt automatique, facteur de coût réglable, irréversible). Le hash n'est **jamais** retourné dans les réponses API, même dans les GET.

### Cycle de vie d'un Booking

```
pending ──→ confirmed
   └──────→ cancelled
confirmed ──→ cancelled
```

La vérification de chevauchement (`_check_overlap`) exclut les bookings annulés et retourne `409 Conflict` si deux intervalles vérifient : `check_in_A < check_out_B AND check_out_A > check_in_B`.

---

*Valentin Dardenne — Holberton School — 2026*
