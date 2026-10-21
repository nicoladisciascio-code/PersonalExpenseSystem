import sqlite3
from pathlib import Path

percorso_db = Path(__file__).parent / "spese.db"

connessione = sqlite3.connect(percorso_db)
connessione.execute("PRAGMA foreign_keys = ON")

try:
    cursore = connessione.cursor()

    # Test 1: inserimento di una categoria valida
    cursore.execute(
    "INSERT OR IGNORE INTO categorie (nome) VALUES (?)",
    ("Alimentari",)
)
    connessione.commit()
    print("TEST 1 SUPERATO: categoria di test disponibile.")


    # Test 2: categoria duplicata
    try:
        cursore.execute(
            "INSERT INTO categorie (nome) VALUES (?)",
            ("Alimentari",)
        )
        connessione.commit()
        print("TEST 2 FALLITO: categoria duplicata accettata.")
    except sqlite3.IntegrityError:
        connessione.rollback()
        print("TEST 2 SUPERATO: categoria duplicata rifiutata.")

    # Test 3: importo negativo
    id_categoria = cursore.execute(
        "SELECT id_categoria FROM categorie WHERE nome = ?",
        ("Alimentari",)
    ).fetchone()[0]

    try:
        cursore.execute(
            """INSERT INTO spese
               (data, importo, id_categoria, descrizione)
               VALUES (?, ?, ?, ?)""",
            ("2026-01-15", -10.00, id_categoria, "Test negativo")
        )
        connessione.commit()
        print("TEST 3 FALLITO: importo negativo accettato.")
    except sqlite3.IntegrityError:
        connessione.rollback()
        print("TEST 3 SUPERATO: importo negativo rifiutato.")

    # Test 4: categoria inesistente
    try:
        cursore.execute(
            """INSERT INTO spese
               (data, importo, id_categoria, descrizione)
               VALUES (?, ?, ?, ?)""",
            ("2026-01-15", 10.00, -999, "Test FK")
        )
        connessione.commit()
        print("TEST 4 FALLITO: categoria inesistente accettata.")
    except sqlite3.IntegrityError:
        connessione.rollback()
        print("TEST 4 SUPERATO: categoria inesistente rifiutata.")

finally:
    connessione.close()
