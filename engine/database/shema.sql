-- database: The_prince.db
CREATE TABLE IF NOT EXISTS PNJ (
    idPNJ INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    role TEXT DEFAULT 'peasant',
    ambition INTEGER DEFAULT 20 CHECK(ambition BETWEEN 0 AND 100),
    loyaute INTEGER DEFAULT 70 CHECK(loyaute BETWEEN 0 AND 100),
    est_joueur BOOLEAN DEFAULT 0

);



CREATE TABLE IF NOT EXISTS complots (
    idComplot INTEGER PRIMARY KEY AUTOINCREMENT,
    initiateur_id INTEGER,
    cible_id INTEGER,
    reussi BOOLEAN,
    FOREIGN KEY (initiateur_id) REFERENCES PNJ(idPNJ),
    FOREIGN KEY (cible_id) REFERENCES PNJ(idPNJ)
);


CREATE TABLE IF NOT EXISTS royaume (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    jours INTEGER DEFAULT 1
);

