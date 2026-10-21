import sqlite3
from pathlib import Path

# Percorso dei file nella cartella del progetto
cartella_progetto = Path(__file__).parent
percorso_sql = cartella_progetto / "database.sql"
percorso_db = cartella_progetto / "spese.db"

# Verifica che lo script SQL esista
if not percorso_sql.exists():
    raise FileNotFoundError("Il file database.sql non esiste.")

# Connessione al database SQLite
connessione = sqlite3.connect(percorso_db)

try:
    # Attiva i controlli delle chiavi esterne
    connessione.execute("PRAGMA foreign_keys = ON")

    # Legge ed esegue lo script SQL
    script_sql = percorso_sql.read_text(encoding="utf-8")
    connessione.executescript(script_sql)

    print("Database creato e tabelle inizializzate correttamente.")

finally:
    connessione.close()
