import sqlite3
from pathlib import Path

percorso_db = Path(__file__).parent / "spese.db"

connessione = sqlite3.connect(percorso_db)
connessione.execute("PRAGMA foreign_keys = ON")

try:
    cursore = connessione.cursor()

    cursore.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)

    tabelle = cursore.fetchall()

    print("Tabelle presenti nel database:")

    for tabella in tabelle:
        print("-", tabella[0])

finally:
    connessione.close()
