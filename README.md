## Sistema di Gestione delle Spese Personali e del Budget

## Descrizione del progetto

Il progetto consiste nello sviluppo di un'applicazione da terminale scritta in Python per la gestione delle spese personali e dei budget mensili.

L'applicazione permette di registrare le spese, organizzarle per categoria, definire budget mensili e consultare report riepilogativi.

I dati vengono memorizzati in un database relazionale SQLite.

## Funzionalità principali

- **Gestione categorie:** inserimento e visualizzazione delle categorie di spesa.
- **Inserimento spese:** registrazione della data, dell'importo, della categoria e di una descrizione facoltativa.
- **Gestione budget:** definizione e aggiornamento del budget mensile per ciascuna categoria.
- **Report:** visualizzazione dei totali per categoria, confronto tra spese e budget mensile e storico delle spese.
- **Controllo degli input:** verifica dei dati inseriti per ridurre gli errori.
- **Integrità dei dati:** utilizzo di chiavi primarie, chiavi esterne e vincoli SQL.

## Tecnologie utilizzate

- Python 3
- SQLite
- SQL
- Visual Studio Code per lo sviluppo

## Requisiti

È necessario avere Python 3 installato. SQLite viene utilizzato tramite il modulo `sqlite3` incluso nella libreria standard di Python.

## Installazione e avvio

1. Scaricare o clonare la repository del progetto.
2. Aprire il terminale nella cartella del progetto.
3. Inizializzare il database:

   ```bash
   python3 init_db.py
   ```

4. Avviare l'applicazione:

   ```bash
   python3 main.py
   ```

## Struttura del progetto

- `main.py`: contiene il programma principale e le funzionalità dell'applicazione.
- `database.sql`: contiene la definizione delle tabelle, i vincoli e i dati di esempio.
- `init_db.py`: inizializza il database a partire dallo script SQL.
- `test_vincoli.py`: verifica alcuni vincoli di integrità del database.
- `verifica_db.py`: controlla la presenza delle tabelle.
- `spese.db`: database SQLite locale generato durante l'esecuzione.

## Database

Il database è composto da tre tabelle:

- `categorie`: memorizza le categorie di spesa.
- `spese`: memorizza le spese e la categoria associata.
- `budget`: memorizza il budget mensile per categoria.

Le chiavi esterne collegano le spese e i budget alle categorie. Un vincolo `UNIQUE` impedisce di definire più budget per la stessa categoria nello stesso mese.

## Test

Il file `test_vincoli.py` verifica il comportamento di alcuni vincoli SQL, tra cui l'unicità delle categorie, la positività degli importi e il riferimento a una categoria esistente.

## Autore

Progetto realizzato nell'ambito del corso universitario di programmazione.
