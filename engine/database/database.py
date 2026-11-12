
# ============================================================
# IMPORTS
# ============================================================

import sqlite3
from collections.abc import Mapping
from pathlib import Path
from typing import Any

# ============================================================
# DATABASE PATHS
# ============================================================

DATABASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = DATABASE_DIR / "The_prince.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

PRIMARY_KEYS = {
    "PNJ": "idPNJ",
    "complots": "idComplot",
    "royaume": "id",
}

TABLE_COLUMNS = {
    "PNJ": {
        "idPNJ",
        "nom",
        "role",
        "ambition",
        "loyaute",
        "est_joueur",
    },

    "complots": {
        "idComplot",
        "initiateur_id",
        "cible_id",
        "reussi",
    },

    "royaume": {
        "id",
        "jours",
    },
}

REQUIRED_TABLES = {
    "PNJ",
    "complots",
    "royaume",
}


# ============================================================
# DATABASE SCHEMA INITIALIZATION
# ============================================================

def initialize_database(
    connection: sqlite3.Connection,
) -> None:
    """
    Apply schema.sql to the supplied SQLite connection.

    Missing tables are created automatically.
    Existing tables and their data are preserved.
    """

    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(
            f"SQL schema not found: {SCHEMA_PATH.resolve()}"
        )

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    # Enable foreign key constraints.
    connection.execute("PRAGMA foreign_keys = ON")

    # Execute the SQL schema.
    connection.executescript(schema)

    # Verify the database structure.
    cursor = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)

    existing_tables = {
        row[0] for row in cursor.fetchall()
    }

    missing_tables = REQUIRED_TABLES - existing_tables

    if missing_tables:
        raise RuntimeError(
            "Database schema initialization failed. "
            f"Missing tables: {sorted(missing_tables)}. "
            f"Database: {DATABASE_PATH}"
        )

    connection.commit()


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_connection() -> sqlite3.Connection:
    """
    Create and configure the SQLite connection.

    The database schema is applied before returning the connection.
    """

    connection = sqlite3.connect(
        str(DATABASE_PATH),
        timeout=10.0,
    )

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        initialize_database(connection)

    except Exception:
        connection.close()
        raise

    return connection


# ============================================================
# GLOBAL DATABASE CONNECTION
# ============================================================

# Keep compatibility with the original architecture.
conn = create_connection()

# Preserve the original variable name if other modules use it.
path_bdd = DATABASE_PATH

# Compatibility with the original table configuration.
primary_keys = PRIMARY_KEYS


# ============================================================
# DATABASE CLASS
# ============================================================

class Database:
    """Manage SQLite database operations for the game."""

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(
        self,
        connection: sqlite3.Connection | None = None,
    ):
        """
        Initialize the database manager.

        If a connection is supplied, the schema is also applied
        to that exact connection.
        """

        self.conn = connection if connection is not None else conn

        # Initialize the schema on the connection actually used.
        initialize_database(self.conn)

        self.cur = self.conn.cursor()

        self.closed = False

    # ========================================================
    # CONNECTION VALIDATION
    # ========================================================

    def _ensure_open(self) -> None:
        """Ensure that the database connection is still open."""

        if self.closed:
            raise RuntimeError(
                "The database connection is already closed."
            )

    # ========================================================
    # QUERY VALIDATION
    # ========================================================

    @staticmethod
    def _validate_table(table: str) -> None:
        """Validate a database table name."""

        if table not in TABLE_COLUMNS:
            raise ValueError(
                f"Unknown database table: {table!r}"
            )

    # --------------------------------------------------------

    @staticmethod
    def _validate_column(
        table: str,
        column: str,
    ) -> None:
        """Validate a column name against its table."""

        if column not in TABLE_COLUMNS[table]:
            raise ValueError(
                f"Unknown column {column!r} in table {table!r}"
            )

    # ========================================================
    # INTERNAL QUERY HELPERS
    # ========================================================

    def _fetch_all_as_dicts(
        self,
    ) -> list[dict[str, Any]]:
        """Convert all query results into dictionaries."""

        rows = self.cur.fetchall()

        if self.cur.description is None:
            return []

        columns = [
            description[0]
            for description in self.cur.description
        ]

        return [
            dict(zip(columns, row))
            for row in rows
        ]

    # --------------------------------------------------------

    def _fetch_one_as_dict(
        self,
    ) -> dict[str, Any] | None:
        """Convert one query result into a dictionary."""

        row = self.cur.fetchone()

        if row is None:
            return None

        columns = [
            description[0]
            for description in self.cur.description
        ]

        return dict(zip(columns, row))

    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        value: Any,
        table: str,
        column: str,
        row_id: int,
    ) -> None:
        """Update a specific column in a database row."""

        self._ensure_open()

        self._validate_table(table)
        self._validate_column(table, column)

        primary_key = PRIMARY_KEYS[table]

        query = f"""
            UPDATE "{table}"
            SET "{column}" = ?
            WHERE "{primary_key}" = ?
        """

        try:
            self.cur.execute(
                query,
                (value, row_id),
            )

            self.conn.commit()

        except sqlite3.Error:
            self.conn.rollback()
            raise

    # ========================================================
    # ADD
    # ========================================================

    def add(
        self,
        table: str,
        data: Mapping[str, Any],
    ) -> int:
        """Insert a new record and return its generated ID."""

        self._ensure_open()

        self._validate_table(table)

        if not isinstance(data, Mapping):
            raise TypeError(
                "data must be a mapping of column names to values."
            )

        data = dict(data)

        if not data:
            raise ValueError(
                "Cannot insert an empty database record."
            )

        # Validate all supplied columns.
        for column in data:
            self._validate_column(table, column)

        columns = ", ".join(
            f'"{column}"'
            for column in data
        )

        placeholders = ", ".join(
            "?" for _ in data
        )

        query = (
            f'INSERT INTO "{table}" ({columns}) '
            f"VALUES ({placeholders})"
        )

        try:
            self.cur.execute(
                query,
                tuple(data.values()),
            )

            row_id = self.cur.lastrowid

            self.conn.commit()

            if row_id is None:
                raise RuntimeError(
                    "Unable to retrieve the inserted row ID."
                )

            return row_id

        except Exception:
            self.conn.rollback()
            raise

    # ========================================================
    # CHARACTERS
    # ========================================================

    def get_all_characters(
        self,
    ) -> list[dict[str, Any]]:
        """Retrieve all characters as dictionaries."""

        self._ensure_open()

        self.cur.execute("""
            SELECT *
            FROM PNJ
            ORDER BY idPNJ ASC
        """)

        return self._fetch_all_as_dicts()

    # --------------------------------------------------------

    def get_first_character(
        self,
    ) -> dict[str, Any] | None:
        """Retrieve the first character, or None if none exists."""

        self._ensure_open()

        self.cur.execute("""
            SELECT *
            FROM PNJ
            ORDER BY idPNJ ASC
            LIMIT 1
        """)

        return self._fetch_one_as_dict()

    # ========================================================
    # PLOTS
    # ========================================================

    def get_all_plots(
        self,
    ) -> list[dict[str, Any]]:
        """Retrieve plots with their initiator and target names."""

        self._ensure_open()

        self.cur.execute("""
            SELECT
                c.idComplot,
                c.initiateur_id,
                c.cible_id,
                c.reussi,

                p1.nom AS initiateur_nom,
                p2.nom AS cible_nom

            FROM complots c

            LEFT JOIN PNJ p1
                ON c.initiateur_id = p1.idPNJ

            LEFT JOIN PNJ p2
                ON c.cible_id = p2.idPNJ

            ORDER BY c.idComplot DESC
        """)

        return self._fetch_all_as_dicts()

    # ========================================================
    # KINGDOM
    # ========================================================

    def get_kingdom(self) -> dict[str, Any]:
        """Retrieve or initialize the kingdom."""

        self._ensure_open()

        try:
            self.cur.execute("""
                INSERT OR IGNORE INTO royaume (id, jours)
                VALUES (1, 1)
            """)

            self.conn.commit()

        except sqlite3.Error:
            self.conn.rollback()
            raise

        self.cur.execute("""
            SELECT *
            FROM royaume
            WHERE id = 1
        """)

        kingdom = self._fetch_one_as_dict()

        if kingdom is None:
            raise RuntimeError(
                "Unable to initialize the kingdom."
            )

        return kingdom

    # --------------------------------------------------------

    def advance_day(self) -> None:
        """Advance the kingdom calendar by one day."""

        self._ensure_open()

        try:
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

        except sqlite3.Error:
            self.conn.rollback()
            raise

    # ========================================================
    # DATABASE INFORMATION
    # ========================================================

    def get_tables(self) -> list[str]:
        """Return the names of all database tables."""

        self._ensure_open()

        self.cur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            ORDER BY name
        """)

        return [
            row[0]
            for row in self.cur.fetchall()
        ]

    # --------------------------------------------------------

    def get_database_path(self) -> str:
        """Return the actual SQLite database path."""

        self._ensure_open()

        self.cur.execute("PRAGMA database_list")

        databases = self.cur.fetchall()

        for database in databases:
            if database[1] == "main":
                return database[2]

        return ""

    # ========================================================
    # RESOURCE DESTRUCTION
    # ========================================================

    def close(self) -> None:
        """Close the cursor and database connection."""

        if self.closed:
            return

        self.cur.close()
        self.conn.close()

        self.closed = True

    # ========================================================
    # REPRESENTATION
    # ========================================================

    def __repr__(self) -> str:
        """Return a representation of the database."""

        return (
            f"Database("
            f"path={self.get_database_path()!r}, "
            f"tables={self.get_tables()!r}"
            f")"
        )
