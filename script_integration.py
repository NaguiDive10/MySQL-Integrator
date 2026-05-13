"""
MySQL-integrator — import des fichiers CSV / Excel du dossier data/ vers MySQL.

Les noms de tables sont dérivés des noms de fichiers (portion dim_* ou fact_*).
Voir README.md pour la description du projet et la configuration (.env).
"""

import os
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

# Charge les variables MYSQL_* depuis le .env à côté de ce script (important pour Code Runner).
load_dotenv(Path(__file__).resolve().parent / ".env")

# Identifiants MySQL (obligatoires dans .env sauf host/port qui ont des défauts).
user = os.environ["MYSQL_USER"].strip()
password = os.environ["MYSQL_PASSWORD"].strip()
host = os.environ.get("MYSQL_HOST", "localhost").strip()
port = int(os.environ.get("MYSQL_PORT", "3306").strip())
database = os.environ["MYSQL_DATABASE"].strip()

# URL.create évite de mettre user/mot de passe dans une chaîne URL (ex. @ dans le mot de passe).
engine = create_engine(
    URL.create("mysql+pymysql", username=user, password=password, host=host, port=port, database=database)
)

# Dossier contenant les fichiers à importer (chemin relatif = portable ; sinon chemin absolu possible).
dossier = Path(r"C:\Users\User\Desktop\PROJETS WEB\Power BI\demo\data")
# dossier = Path(__file__).resolve().parent / "data"
EXTENSIONS = {".csv", ".xlsx", ".xls"}


def table_depuis_nom_fichier(chemin: Path) -> str | None:
    """
    Retourne le nom de table MySQL à partir du nom de fichier.

    On prend la sous-chaîne commençant par dim_ ou fact_ jusqu'à la fin du nom sans extension.
    Tout ce qui précède (préfixe projet, date, etc.) est ignoré. Les espaces sont remplacés par _.
    """
    stem = re.sub(r"\s+", "_", chemin.stem.strip())
    m = re.search(r"(dim_[a-z0-9_]+|fact_[a-z0-9_]+)", stem.lower())
    return m.group(1) if m else None


# Liste triée des fichiers supportés dans data/.
fichiers = sorted(
    p for p in dossier.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS
)

for chemin in fichiers:
    fichier = chemin.name
    table = table_depuis_nom_fichier(chemin)
    if table is None:
        print(f"Ignoré (aucun dim_/fact_ dans le nom) : {fichier}")
        continue

    suffix = chemin.suffix.lower()
    if suffix == ".csv":
        try:
            df = pd.read_csv(chemin)
        except Exception as err:
            print(f"Ignoré (CSV illisible) : {fichier} - {err}")
            continue
    else:
        df = pd.read_excel(chemin)

    print(f"Import de {fichier} -> {table} ({len(df)} lignes)")
    # Remplace la table si elle existe déjà ; pas de colonne d'index pandas en base.
    df.to_sql(table, con=engine, if_exists="replace", index=False)

print("Terminé !")
