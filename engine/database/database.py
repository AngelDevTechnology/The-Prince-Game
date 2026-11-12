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
    "Plot": "idPlot",
    "Kingdom": "id",
}

TABLE_COLUMNS = {
    "PNJ": {
        "idPNJ",
        "name",
        "role",
        "ambition",
        "loyalty",
        "is_player",
    },
    "Plot": {
        "idPlot",
        "initiator_id",
        "target_id",
        "successful",
    },
    "Kingdom": {
        "id",
        "days",
    },
}

REQUIRED_COLUMNS = TABLE_COLUMNS
REQUIRED_TABLES = set(TABLE_COLUMNS)

# Compatibility aliases for modules that still import these names.
path_bdd = DATABASE_PATH
primary_keys = PRIMARY_KEYS


# ============================================================
# SCHEMA MIGRATION
# ============================================================

def _table_exists(connection: sqlite3.Connection, table: str) -> bool:
    """Return whether a table exists, ignoring identifier casing."""
    row = connection.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table' AND lower(name) = lower(?)
        LIMIT 1
        """,
        (table,),
    ).fetchone()
    return row is not None


def _table_columns(
    connection: sqlite3.Connection,
    table: str,
) -> set[str]:
    """Return the column names of a table."""
    rows = connection.execute(f'PRAGMA table_info("{table}")').fetchall()
    return {row[1] for row in rows}


def _rename_table_if_needed(
    connection: sqlite3.Connection,
    old_name: str,
    new_name: str,
) -> None:
    """Rename a legacy table, preserving its rows and relationships."""
    old_exists = _table_exists(connection, old_name)
    new_exists = _table_exists(connection, new_name)

    if old_exists and new_exists:
        raise RuntimeError(
            f"Both legacy table {old_name!r} and new table {new_name!r} "
            "exist. Resolve this database conflict before starting the game."
        )

    if old_exists:
        connection.execute(
            f'ALTER TABLE "{old_name}" RENAME TO "{new_name}"'
        )


def _rename_column_if_needed(
    connection: sqlite3.Connection,
    table: str,
    old_name: str,
    new_name: str,
) -> None:
    """Rename a legacy column without deleting its data."""
    if not _table_exists(connection, table):
        return

    columns = _table_columns(connection, table)
    has_old_name = old_name in columns
    has_new_name = new_name in columns

    if has_old_name and has_new_name:
        raise RuntimeError(
            f"Table {table!r} contains both {old_name!r} and {new_name!r}. "
            "Resolve this database conflict before starting the game."
        )

    if has_old_name:
        connection.execute(
            f'ALTER TABLE "{table}" '
            f'RENAME COLUMN "{old_name}" TO "{new_name}"'
        )


def migrate_legacy_schema(connection: sqlite3.Connection) -> None:
    """Migrate the original French database names to the English schema."""
    # Rename tables first. SQLite updates foreign-key references when a
    # table is renamed, so the relationships between plots and characters
    # remain intact.
    _rename_table_if_needed(connection, "complots", "Plot")
    _rename_table_if_needed(connection, "royaume", "Kingdom")

    # Migrate character columns.
    for old_name, new_name in (
        ("nom", "name"),
        ("loyaute", "loyalty"),
        ("est_joueur", "is_player"),
    ):
        _rename_column_if_needed(connection, "PNJ", old_name, new_name)

    # Migrate plot columns.
    for old_name, new_name in (
        ("idComplot", "idPlot"),
        ("initiateur_id", "initiator_id"),
        ("cible_id", "target_id"),
        ("reussi", "successful"),
    ):
        _rename_column_if_needed(connection, "Plot", old_name, new_name)

    # Migrate kingdom columns.
    _rename_column_if_needed(connection, "Kingdom", "jours", "days")


# ============================================================
# DATABASE SCHEMA INITIALIZATION
# ============================================================

def initialize_database(connection: sqlite3.Connection) -> None:
    """Migrate legacy names, apply schema.sql, and validate the schema."""
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(
            f"SQL schema not found: {SCHEMA_PATH.resolve()}"
        )

    connection.execute("PRAGMA foreign_keys = ON")

    try:
        migrate_legacy_schema(connection)
        connection.commit()

        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)

        existing_tables = {
            row[0]
            for row in connection.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        }
        existing_tables_lower = {name.lower() for name in existing_tables}
        missing_tables = {
            table
            for table in REQUIRED_TABLES
            if table.lower() not in existing_tables_lower
        }

        if missing_tables:
            raise RuntimeError(
                "Database schema initialization failed. "
                f"Missing tables: {sorted(missing_tables)}. "
                f"Database: {DATABASE_PATH}"
            )

        # Check the columns as well as the table names. CREATE TABLE IF NOT
        # EXISTS cannot update a table that already exists.
        for table, expected_columns in REQUIRED_COLUMNS.items():
            actual_columns = _table_columns(connection, table)
            missing_columns = expected_columns - actual_columns

            if missing_columns:
                raise RuntimeError(
                    f"Table {table!r} is missing columns: "
                    f"{sorted(missing_columns)}"
                )

        connection.commit()

    except Exception:
        connection.rollback()
        raise


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_connection() -> sqlite3.Connection:
    """Create a SQLite connection and initialize its schema."""
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
# DATABASE CLASS
# ============================================================

class Database:
    """Manage SQLite database operations for the game."""

    def __init__(
        self,
        connection: sqlite3.Connection | None = None,
    ) -> None:
        """Use the supplied connection or create an initialized one."""
        if connection is None:
            self.conn = create_connection()
        else:
            self.conn = connection
            initialize_database(self.conn)

        self.cur = self.conn.cursor()
        self.closed = False

    # ========================================================
    # CONNECTION VALIDATION
    # ========================================================

    def _ensure_open(self) -> None:
        """Raise an error when this database manager has been closed."""
        if self.closed:
            raise RuntimeError("The database connection is already closed.")

    # ========================================================
    # QUERY VALIDATION
    # ========================================================

    @staticmethod
    def _validate_table(table: str) -> None:
        """Validate a table name against the application whitelist."""
        if table not in TABLE_COLUMNS:
            raise ValueError(f"Unknown database table: {table!r}")

    @staticmethod
    def _validate_column(table: str, column: str) -> None:
        """Validate a column name against the application whitelist."""
        if column not in TABLE_COLUMNS[table]:
            raise ValueError(
                f"Unknown column {column!r} in table {table!r}"
            )

    # ========================================================
    # INTERNAL QUERY HELPERS
    # ========================================================

    def _fetch_all_as_dicts(self) -> list[dict[str, Any]]:
        """Convert all rows from the current query into dictionaries."""
        rows = self.cur.fetchall()

        if self.cur.description is None:
            return []

        columns = [description[0] for description in self.cur.description]
        return [dict(zip(columns, row)) for row in rows]

    def _fetch_one_as_dict(self) -> dict[str, Any] | None:
        """Convert one row from the current query into a dictionary."""
        row = self.cur.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in self.cur.description]
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
        """Update one column of a row."""
        self._ensure_open()
        self._validate_table(table)
        self._validate_column(table, column)

        primary_key = PRIMARY_KEYS[table]
        query = (
            f'UPDATE "{table}" '
            f'SET "{column}" = ? '
            f'WHERE "{primary_key}" = ?'
        )

        try:
            self.cur.execute(query, (value, row_id))
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise

    # ========================================================
    # ADD
    # ========================================================

    def add(self, table: str, data: Mapping[str, Any]) -> int:
        """Insert a row and return its generated primary-key value."""
        self._ensure_open()
        self._validate_table(table)

        if not isinstance(data, Mapping):
            raise TypeError("data must be a mapping of column names to values.")

        values = dict(data)
        if not values:
            raise ValueError("Cannot insert an empty database record.")

        for column in values:
            self._validate_column(table, column)

        columns_sql = ", ".join(f'"{column}"' for column in values)
        placeholders = ", ".join("?" for _ in values)
        query = (
            f'INSERT INTO "{table}" ({columns_sql}) '
            f"VALUES ({placeholders})"
        )

        try:
            self.cur.execute(query, tuple(values.values()))
            row_id = self.cur.lastrowid

            if row_id is None:
                raise RuntimeError("Unable to retrieve the inserted row ID.")

            self.conn.commit()
            return row_id
        except Exception:
            self.conn.rollback()
            raise

    # ========================================================
    # CHARACTERS
    # ========================================================

    def get_all_characters(self) -> list[dict[str, Any]]:
        """Retrieve all characters in ascending ID order."""
        self._ensure_open()
        self.cur.execute(
            "SELECT * FROM PNJ ORDER BY idPNJ ASC"
        )
        return self._fetch_all_as_dicts()

    def get_first_character(self) -> dict[str, Any] | None:
        """Retrieve the first character, or None when there are none."""
        self._ensure_open()
        self.cur.execute(
            "SELECT * FROM PNJ ORDER BY idPNJ ASC LIMIT 1"
        )
        return self._fetch_one_as_dict()

    # ========================================================
    # PLOTS
    # ========================================================

    def get_all_plots(self) -> list[dict[str, Any]]:
        """Retrieve plots with the names of their initiators and targets."""
        self._ensure_open()
        self.cur.execute(
            """
            SELECT
                plot.idPlot,
                plot.initiator_id,
                plot.target_id,
                plot.successful,
                initiator.name AS initiator_name,
                target.name AS target_name
            FROM Plot AS plot
            LEFT JOIN PNJ AS initiator
                ON plot.initiator_id = initiator.idPNJ
            LEFT JOIN PNJ AS target
                ON plot.target_id = target.idPNJ
            ORDER BY plot.idPlot DESC
            """
        )
        return self._fetch_all_as_dicts()

    # ========================================================
    # KINGDOM
    # ========================================================

    def get_kingdom(self) -> dict[str, Any]:
        """Retrieve the kingdom, creating its initial row when needed."""
        self._ensure_open()

        try:
            self.cur.execute(
                "INSERT OR IGNORE INTO Kingdom (id, days) VALUES (1, 1)"
            )
            self.conn.commit()
        except sqlite3.Error:
            self.conn.rollback()
            raise

        self.cur.execute("SELECT * FROM Kingdom WHERE id = 1")
        kingdom = self._fetch_one_as_dict()

        if kingdom is None:
            raise RuntimeError("Unable to initialize the kingdom.")

        return kingdom

    def advance_day(self) -> None:
        """Advance the kingdom by one day, up to the schema limit of 30."""
        self._ensure_open()

        try:
            self.cur.execute(
                "INSERT OR IGNORE INTO Kingdom (id, days) VALUES (1, 1)"
            )
            self.cur.execute("SELECT days FROM Kingdom WHERE id = 1")
            row = self.cur.fetchone()

            if row is None:
                raise RuntimeError("Unable to retrieve the kingdom day.")

            current_day = row[0]
            if current_day >= 30:
                raise ValueError("The kingdom has reached the maximum day (30).")

            self.cur.execute(
                "UPDATE Kingdom SET days = days + 1 WHERE id = 1"
            )
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    # ========================================================
    # DATABASE INFORMATION
    # ========================================================

    def get_tables(self) -> list[str]:
        """Return the names of all user tables in the database."""
        self._ensure_open()
        self.cur.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        return [row[0] for row in self.cur.fetchall()]

    def get_database_path(self) -> str:
        """Return the path of the SQLite main database file."""
        self._ensure_open()
        self.cur.execute("PRAGMA database_list")

        for database in self.cur.fetchall():
            if database[1] == "main":
                return database[2]

        return ""

    # ========================================================
    # RESOURCE DESTRUCTION
    # ========================================================

    def close(self) -> None:
        """Close the cursor and database connection safely."""
        if self.closed:
            return

        self.cur.close()
        self.conn.close()
        self.closed = True

    # ========================================================
    # REPRESENTATION
    # ========================================================

    def __repr__(self) -> str:
        """Return a concise representation of this database manager."""
        if self.closed:
            return "Database(closed=True)"

        return (
            f"Database(path={self.get_database_path()!r}, "
            f"tables={self.get_tables()!r})"
        )
