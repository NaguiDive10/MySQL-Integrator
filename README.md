# MySQL-integrator

**MySQL-integrator** est un script Python qui parcourt un dossier de données, détecte les fichiers `.csv`, `.xlsx` et `.xls`, déduit le nom de chaque table MySQL à partir du nom de fichier (segment commençant par `dim_` ou `fact_`), puis charge le contenu dans la base via pandas et SQLAlchemy. La connexion s’appuie sur des variables d’environnement (fichier `.env`) pour ne pas exposer les identifiants dans le code. L’objectif est de préparer rapidement des tables analytiques pour la BI (par ex. Power BI) ou tout autre consommateur SQL.

*En bref : chargement automatisé de fichiers plats vers MySQL avec règles de nommage `dim_*` / `fact_*` et configuration externalisée.*

## Prérequis

- Python 3.10+ recommandé
- Un serveur MySQL accessible (local ou distant)
- Les tables sont créées ou remplacées par le script (`if_exists="replace"`)

## Installation

À la racine du projet :

```bash
pip install -r requirements.txt
```

## Configuration (`.env`)

Copiez `.env_example` vers `.env` et renseignez les valeurs :

| Variable | Obligatoire | Description |
|----------|-------------|-------------|
| `MYSQL_USER` | oui | Utilisateur MySQL |
| `MYSQL_PASSWORD` | oui | Mot de passe |
| `MYSQL_DATABASE` | oui | Nom de la base cible |
| `MYSQL_HOST` | non | Défaut : `localhost` |
| `MYSQL_PORT` | non | Défaut : `3306` |

Le script charge automatiquement le fichier `.env` placé **dans le même dossier** que `script_integration.py` (pratique avec l’extension Code Runner de VS Code / Cursor).

## Dossier `data/` et nommage des tables

- Fichiers pris en compte : extensions `.csv`, `.xlsx`, `.xls`.
- Le **nom de table** est extrait du nom de fichier : première occurrence d’une chaîne du type `dim_...` ou `fact_...` (lettres minuscules, chiffres, underscores), jusqu’à la fin du nom **sans** l’extension. Tout préfixe avant `dim_` / `fact_` est ignoré.

Exemples :

- `250619_cap_rh_dim_absences.xlsx` → table `dim_absences`
- `cap_rh dim_grades.csv` → table `dim_grades` (espaces normalisés en `_` avant analyse)

Les fichiers dont le nom ne contient ni `dim_` ni `fact_` sont ignorés (message dans la console).

## Exécution

```bash
python script_integration.py
```

Ou via Code Runner dans l’éditeur (bouton lecture sur le fichier).

## Fichier principal

- `script_integration.py` — point d’entrée MySQL-integrator : connexion MySQL, parcours de `data/`, lecture CSV/Excel, écriture avec pandas / SQLAlchemy.

## Dépendances

Voir `requirements.txt` (pandas, SQLAlchemy, PyMySQL, openpyxl, python-dotenv).
