-- ==========================================
-- DATABASE: SISTEMA SPESE PERSONALI
-- ==========================================

PRAGMA foreign_keys = ON;

-- 1. Tabella delle categorie
CREATE TABLE IF NOT EXISTS categorie (
    id_categoria INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE
        CHECK (length(trim(nome)) > 0)
);

-- 2. Tabella delle spese
CREATE TABLE IF NOT EXISTS spese (
    id_spesa INTEGER PRIMARY KEY,
    data TEXT NOT NULL,
    importo REAL NOT NULL CHECK (importo > 0),
    id_categoria INTEGER NOT NULL,
    descrizione TEXT,

    FOREIGN KEY (id_categoria)
        REFERENCES categorie(id_categoria)
);

-- 3. Tabella dei budget mensili
CREATE TABLE IF NOT EXISTS budget (
    id_budget INTEGER PRIMARY KEY,
    mese TEXT NOT NULL
        CHECK (
            length(mese) = 7
            AND substr(mese, 5, 1) = '-'
            AND substr(mese, 1, 4) NOT GLOB '*[^0-9]*'
            AND substr(mese, 6, 2) BETWEEN '01' AND '12'
        ),
    id_categoria INTEGER NOT NULL,
    importo_budget REAL NOT NULL CHECK (importo_budget > 0),

    FOREIGN KEY (id_categoria)
        REFERENCES categorie(id_categoria),

    UNIQUE (mese, id_categoria)
);


-- ==========================================
-- DATI DI ESEMPIO
-- ==========================================

-- Inserimento di alcune categorie.
-- OR IGNORE evita duplicati se lo script viene rieseguito.
INSERT OR IGNORE INTO categorie (nome)
VALUES
    ('Alimentari'),
    ('Trasporti'),
    ('Casa'),
    ('Svago');

-- Esempio di spesa per la categoria Alimentari.
-- NOT EXISTS evita di inserire nuovamente la stessa spesa.
INSERT INTO spese (data, importo, id_categoria, descrizione)
SELECT
    '2026-10-21',
    25.50,
    id_categoria,
    'Spesa al supermercato'
FROM categorie
WHERE nome = 'Alimentari'
AND NOT EXISTS (
    SELECT 1
    FROM spese
    WHERE data = '2026-10-21'
      AND importo = 25.50
      AND id_categoria = categorie.id_categoria
      AND descrizione = 'Spesa al supermercato'
);

-- Esempio di budget mensile per Alimentari.
-- Viene inserito soltanto se non esiste già.
INSERT OR IGNORE INTO budget (mese, id_categoria, importo_budget)
SELECT
    '2026-10',
    id_categoria,
    350.00
FROM categorie
WHERE nome = 'Alimentari';
