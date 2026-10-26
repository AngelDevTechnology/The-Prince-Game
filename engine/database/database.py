import sqlite3
from pathlib import Path

from engine.models.courtier import Courtier

path_bdd = Path(__file__).parent / "The_prince.db"
conn = sqlite3.connect(path_bdd)


"""
cur.execute("SELECT * FROM PNJ")
result = cur.fetchall()
print(result)


first_tuple = result[0]
first_courtier = Courtier(
    first_tuple[0],
    first_tuple[1],
    first_tuple[2],
    first_tuple[3],
    first_tuple[4],
    first_tuple[5],
)
print(first_tuple)
print(first_courtier)
print(first_courtier.name)
"""

primary_keys = {'PNJ' : 'idPNJ', 'complots' : 'idComplot', 'royaume' : 'id'}


class Database:
    def __init__(self, conn):
        self.conn = conn
        self.cur = self.conn.cursor()

    def update(self, value, table, column, row_id):
        self.cur.execute(f"UPDATE {table} SET {column} = ? WHERE {primary_keys[table]} = ?", (value, row_id))
        self.conn.commit()  


    def close(self):
        self.conn.close()

    def add(self, table, data):
        if table not in primary_keys:
            raise ValueError("table inconnue")
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        self.cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(data.values()))
        self.conn.commit()
        return self.cur.lastrowid

    def get_all_characters(self):
        self.cur.execute("SELECT * FROM PNJ")
        rows = self.cur.fetchall()
        characters = []
        for row in rows:
            characters.append(Courtier(row[0], row[1], row[2], row[3], row[4], row[5]))
        return characters

"""
if __name__ == "__main__":
    db = Database(conn)
    new_id = db.add("PNJ", {"nom": "Ardouin", "role": "courtier"})
    print(new_id)
    db.add("PNJ", {"role": "king"})
    db.close()
"""

if __name__ == "__main__":
    db = Database(conn)
    print(db.get_all_characters())
    db.close()
