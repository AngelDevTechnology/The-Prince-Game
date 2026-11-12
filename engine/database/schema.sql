-- ============================================================
-- THE PRINCE - DATABASE SCHEMA
-- ============================================================

CREATE TABLE IF NOT EXISTS PNJ (
    idPNJ INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'peasant',
    ambition INTEGER NOT NULL DEFAULT 20
        CHECK (ambition BETWEEN 0 AND 100),
    loyalty INTEGER NOT NULL DEFAULT 70
        CHECK (loyalty BETWEEN 0 AND 100),
    is_player INTEGER NOT NULL DEFAULT 0
        CHECK (is_player IN (0, 1))
);

CREATE TABLE IF NOT EXISTS Plot (
    idPlot INTEGER PRIMARY KEY AUTOINCREMENT,
    initiator_id INTEGER,
    target_id INTEGER,
    successful INTEGER
        CHECK (successful IS NULL OR successful IN (0, 1)),
    FOREIGN KEY (initiator_id) REFERENCES PNJ(idPNJ),
    FOREIGN KEY (target_id) REFERENCES PNJ(idPNJ)
);

CREATE TABLE IF NOT EXISTS Kingdom (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    days INTEGER NOT NULL DEFAULT 1
        CHECK (days BETWEEN 0 AND 30)
);
