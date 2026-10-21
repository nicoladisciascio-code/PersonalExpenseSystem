import sqlite3
from datetime import datetime
from pathlib import Path


# Percorso del database nella cartella del progetto
PERCORSO_DB = Path(__file__).parent / "spese.db"


def crea_connessione():
    connessione = sqlite3.connect(PERCORSO_DB)
    connessione.execute("PRAGMA foreign_keys = ON")
    return connessione


def aggiungi_categoria():
    nome = input("Inserisci il nome della nuova categoria: ").strip()

    if not nome:
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    connessione = crea_connessione()

    try:
        connessione.execute(
            "INSERT INTO categorie (nome) VALUES (?)",
            (nome,)
        )
        connessione.commit()
        print(f"Categoria '{nome}' aggiunta correttamente.")

    except sqlite3.IntegrityError:
        print("Errore: questa categoria esiste già.")

    finally:
        connessione.close()




def visualizza_categorie():
    connessione = crea_connessione()

    try:
        cursore = connessione.cursor()

        cursore.execute("""
            SELECT id_categoria, nome
            FROM categorie
            ORDER BY nome;
        """)

        categorie = cursore.fetchall()

        if not categorie:
            print("Non ci sono ancora categorie registrate.")
        else:
            print("\n--- CATEGORIE DISPONIBILI ---")

            for id_categoria, nome in categorie:
                print(f"{id_categoria}. {nome}")

    finally:
        connessione.close()



def gestione_categorie():
    while True:
        print("\n--- GESTIONE CATEGORIE ---")
        print("1. Aggiungi categoria")
        print("2. Visualizza categorie")
        print("3. Torna al menu principale")

        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            aggiungi_categoria()
        elif scelta == "2":
            visualizza_categorie()
        elif scelta == "3":
            break
        else:
            print("Scelta non valida. Riprovare.")


def inserisci_spesa():

    print("\n--- INSERIMENTO NUOVA SPESA ---")

    # 1. Inserimento e controllo della data
    data_spesa = input("Inserisci la data (AAAA-MM-GG): ").strip()

    try:
        datetime.strptime(data_spesa, "%Y-%m-%d")
    except ValueError:
        print("Errore: formato data non valido. Usa AAAA-MM-GG.")
        return

    # 2. Inserimento e controllo dell'importo
    try:
        importo = float(input("Inserisci l'importo in euro: ").replace(",", "."))
    except ValueError:
        print("Errore: devi inserire un importo numerico.")
        return

    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return

    # 3. Connessione al database e visualizzazione categorie

    connessione = crea_connessione()
    
    try:
        cursore = connessione.cursor()

        cursore.execute("""
            SELECT id_categoria, nome
            FROM categorie
            ORDER BY nome;
        """)

        categorie = cursore.fetchall()

        if not categorie:
            print("Non ci sono categorie. Aggiungine prima una.")
            return

        print("\nCategorie disponibili:")
        for id_categoria, nome in categorie:
            print(f"{id_categoria}. {nome}")

        # 4. Scelta della categoria
        try:
            id_categoria = int(input("Inserisci l'ID della categoria: "))
        except ValueError:
            print("Errore: devi inserire un ID numerico.")
            return

        id_validi = [categoria[0] for categoria in categorie]

        if id_categoria not in id_validi:
            print("Errore: la categoria selezionata non esiste.")
            return

        # 5. Descrizione facoltativa
        descrizione = input("Inserisci una descrizione (facoltativa): ").strip()
        if not descrizione:
            descrizione = None

        # 6. Salvataggio nel database
        cursore.execute("""
            INSERT INTO spese (data, importo, id_categoria, descrizione)
            VALUES (?, ?, ?, ?);
        """, (data_spesa, importo, id_categoria, descrizione))

        connessione.commit()
        print("Spesa registrata correttamente!")

    except sqlite3.Error as errore:
        print(f"Errore durante il salvataggio della spesa: {errore}")

    finally:
        connessione.close()


def definisci_budget():
    print("\n--- DEFINIZIONE BUDGET MENSILE ---")

    # 1. Inserimento e controllo del mese
    mese = input("Inserisci il mese (AAAA-MM): ").strip()

    try:
        datetime.strptime(mese, "%Y-%m")
    except ValueError:
        print("Errore: formato mese non valido. Usa AAAA-MM.")
        return

    # 2. Connessione al database
    connessione = crea_connessione()
    
    try:
        cursore = connessione.cursor()

        # 3. Visualizzazione delle categorie disponibili
        cursore.execute("""
            SELECT id_categoria, nome
            FROM categorie
            ORDER BY nome;
        """)

        categorie = cursore.fetchall()

        if not categorie:
            print("Non ci sono categorie. Aggiungine prima una.")
            return

        print("\nCategorie disponibili:")
        for id_categoria, nome in categorie:
            print(f"{id_categoria}. {nome}")

        # 4. Scelta della categoria
        try:
            id_categoria = int(
                input("Inserisci l'ID della categoria: ")
            )
        except ValueError:
            print("Errore: devi inserire un ID numerico.")
            return

        id_validi = [categoria[0] for categoria in categorie]

        if id_categoria not in id_validi:
            print("Errore: la categoria selezionata non esiste.")
            return

        # 5. Inserimento e controllo dell'importo del budget
        try:
            importo_budget = float(
                input("Inserisci l'importo del budget in euro: ")
                .replace(",", ".")
            )
        except ValueError:
            print("Errore: devi inserire un importo numerico.")
            return

        if importo_budget <= 0:
            print("Errore: il budget deve essere maggiore di zero.")
            return

        # 6. Verifica se esiste già un budget per mese e categoria
        cursore.execute("""
            SELECT id_budget
            FROM budget
            WHERE mese = ? AND id_categoria = ?;
        """, (mese, id_categoria))

        budget_esistente = cursore.fetchone()

        if budget_esistente:
            cursore.execute("""
                UPDATE budget
                SET importo_budget = ?
                WHERE mese = ? AND id_categoria = ?;
            """, (importo_budget, mese, id_categoria))

            print("Budget aggiornato correttamente!")

        else:
            cursore.execute("""
                INSERT INTO budget (mese, id_categoria, importo_budget)
                VALUES (?, ?, ?);
            """, (mese, id_categoria, importo_budget))

            print("Budget definito correttamente!")

        connessione.commit()

    except sqlite3.Error as errore:
        print(f"Errore durante la gestione del budget: {errore}")

    finally:
        connessione.close()


def visualizza_report():
    while True:
        print("\n--- VISUALIZZAZIONE REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili rispetto al budget")
        print("3. Elenco di tutte le spese")
        print("4. Torna al menu principale")

        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            report_per_categoria()
        elif scelta == "2":
            report_budget_mensile()
        elif scelta == "3":
            report_tutte_le_spese()
        elif scelta == "4":
            break
        else:
            print("Scelta non valida. Riprovare.")


def report_per_categoria():
    connessione = crea_connessione()
    
    try:
        cursore = connessione.cursor()

        cursore.execute("""
            SELECT
                categorie.nome,
                COALESCE(SUM(spese.importo), 0)
            FROM categorie
            LEFT JOIN spese
                ON categorie.id_categoria = spese.id_categoria
            GROUP BY categorie.id_categoria, categorie.nome
            ORDER BY categorie.nome;
        """)

        risultati = cursore.fetchall()

        print("\n--- TOTALE SPESE PER CATEGORIA ---")

        for nome, totale in risultati:
            print(f"{nome}: {totale:.2f} euro")

    except sqlite3.Error as errore:
        print(f"Errore durante la generazione del report: {errore}")

    finally:
        connessione.close()


def report_budget_mensile():
    print("\n--- SPESE MENSILI RISPETTO AL BUDGET ---")

    mese = input("Inserisci il mese da analizzare (AAAA-MM): ").strip()

    try:
        datetime.strptime(mese, "%Y-%m")
    except ValueError:
        print("Errore: formato mese non valido. Usa AAAA-MM.")
        return

    connessione = crea_connessione()
    
    try:
        cursore = connessione.cursor()

        cursore.execute("""
            SELECT
                categorie.nome,
                budget.importo_budget,
                COALESCE(SUM(spese.importo), 0)
            FROM budget
            JOIN categorie
                ON budget.id_categoria = categorie.id_categoria
            LEFT JOIN spese
                ON spese.id_categoria = budget.id_categoria
                AND substr(spese.data, 1, 7) = budget.mese
            WHERE budget.mese = ?
            GROUP BY
                categorie.id_categoria,
                categorie.nome,
                budget.importo_budget
            ORDER BY categorie.nome;
        """, (mese,))

        risultati = cursore.fetchall()

        if not risultati:
            print(f"Non ci sono budget definiti per il mese {mese}.")
            return

        print(f"\nRiepilogo del mese {mese}:")

        for nome, budget, speso in risultati:
            differenza = budget - speso

            print(f"\nCategoria: {nome}")
            print(f"Budget: {budget:.2f} euro")
            print(f"Speso: {speso:.2f} euro")

            if differenza > 0:
                print(f"Disponibile: {differenza:.2f} euro")
            elif differenza < 0:
                print(f"Budget superato di: {abs(differenza):.2f} euro")
            else:
                print("Budget esaurito esattamente.")

    except sqlite3.Error as errore:
        print(f"Errore durante il report: {errore}")

    finally:
        connessione.close()


def report_tutte_le_spese():
    connessione = crea_connessione()

    try:
        cursore = connessione.cursor()

        cursore.execute("""
            SELECT
                spese.data,
                spese.importo,
                categorie.nome,
                spese.descrizione
            FROM spese
            JOIN categorie
                ON spese.id_categoria = categorie.id_categoria
            ORDER BY spese.data DESC, spese.id_spesa DESC;
        """)

        spese = cursore.fetchall()

        print("\n--- ELENCO DI TUTTE LE SPESE ---")

        if not spese:
            print("Non ci sono ancora spese registrate.")
            return

        for data, importo, categoria, descrizione in spese:
            descrizione = descrizione or "Nessuna descrizione"

            print(f"\nData: {data}")
            print(f"Importo: {importo:.2f} euro")
            print(f"Categoria: {categoria}")
            print(f"Descrizione: {descrizione}")

    except sqlite3.Error as errore:
        print(f"Errore durante la visualizzazione delle spese: {errore}")

    finally:
        connessione.close()


def mostra_menu():
    print("\n-------------------------")
    print(" SISTEMA SPESE PERSONALI")
    print("-------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-------------------------")


def main():
    print("Benvenuto nel sistema di gestione delle spese!")

    scelta = ""

    while scelta != "5":
        mostra_menu()
        scelta = input("Inserisci la tua scelta: ").strip()

        if scelta == "1":
            gestione_categorie()

        elif scelta == "2":
            inserisci_spesa()

        elif scelta == "3":
            definisci_budget()

        elif scelta == "4":
            visualizza_report()
            
        elif scelta == "5":
            print("Arrivederci!")

        else:
            print("Scelta non valida. Riprovare.")


if __name__ == "__main__":
    main()
