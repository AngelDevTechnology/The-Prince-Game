import sqlite3
from pathlib import Path


# ==================================================
# DATABASE CONFIGURATION
# ==================================================

path_bdd = Path(__file__).parent / "The_prince.db"
conn = sqlite3.connect(path_bdd)

primary_keys = {
    "PNJ": "idPNJ",
    "complots": "idComplot",
    "royaume": "id",
}


class Database:
    """Manage SQLite database operations for the game."""

    def __init__(self, conn):
        """Initialize the database connection and cursor."""

        self.conn = conn
        self.cur = self.conn.cursor()

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, value, table, column, row_id):
        """Update a specific column in a database row."""

        self.cur.execute(
            f"UPDATE {table} SET {column} = ? WHERE {primary_keys[table]} = ?",
            (value, row_id),
        )

        self.conn.commit()

    # ==================================================
    # ADD
    # ==================================================

    def add(self, table, data):
        """Insert a new record and return its generated primary key."""

        if table not in primary_keys:
            raise ValueError("Table inconnue")

        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)

        self.cur.execute(
            f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
            tuple(data.values()),
        )

        self.conn.commit()

        return self.cur.lastrowid

    # ==================================================
    # CHARACTERS
    # ==================================================

    def get_all_characters(self):
        """Retrieve all characters and return them as dictionaries."""

        self.cur.execute("SELECT * FROM PNJ")

        rows = self.cur.fetchall()
        columns = [column[0] for column in self.cur.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    def get_first_character(self):
        """Retrieve the first character, or None if no characters exist."""

        characters = self.get_all_characters()

        return characters[0] if characters else None

    # ==================================================
    # PLOTS
    # ==================================================

    def get_all_plots(self):
        """Retrieve all plots with their initiator and target names."""

        self.cur.execute("""
            SELECT
                c.idComplot,
                c.initiateur_id,
                c.cible_id,
                c.reussi,
                p1.nom AS initiateur_nom,
                p2.nom AS cible_nom
            FROM complots c
            LEFT JOIN PNJ p1 ON c.initiateur_id = p1.idPNJ
            LEFT JOIN PNJ p2 ON c.cible_id = p2.idPNJ
            ORDER BY c.idComplot DESC
        """)

        rows = self.cur.fetchall()
        columns = [column[0] for column in self.cur.description]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    # ==================================================
    # KINGDOM
    # ==================================================

    def get_kingdom(self):
        """Retrieve kingdom data and initialize it if it does not exist."""

        self.cur.execute(
            "SELECT * FROM royaume WHERE id = 1"
        )

        row = self.cur.fetchone()

        # Initialize the kingdom if it does not exist.
        if row is None:
            self.cur.execute(
                "INSERT INTO royaume (id, jours) VALUES (1, 1)"
            )

            self.conn.commit()

            return {"id": 1, "jours": 1}

        columns = [column[0] for column in self.cur.description]

        return dict(zip(columns, row))

    def advance_day(self):
        """Advance the kingdom calendar by one day."""

        self.cur.execute("""
            INSERT OR IGNORE INTO royaume (id, jours)
            VALUES (1, 1)
        """)

        self.cur.execute("""
            UPDATE royaume
            SET jours = jours + 1
            WHERE id = 1
        """)

        self.conn.commit()

    # ==================================================
    # CLOSE
    # ==================================================

    def close(self):
        """Close the database connection."""

        self.conn.close()

    def __repr__(self):
        """Return a string representation of all characters."""

        return str(self.get_all_characters())