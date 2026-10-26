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
    def __init__(self, conn): # initializes the Database object with a connection to the database
        self.conn = conn
        self.cur = self.conn.cursor()

    def update(self, value, table, column, row_id): # update the specified column of the specified table for the row with the given id
        self.cur.execute(f"UPDATE {table} SET {column} = ? WHERE {primary_keys[table]} = ?", (value, row_id))
        self.conn.commit()  


    def close(self): # closes the database connection
        self.conn.close()

    def add(self, table, data): # add a new row to the specified table with the provided data
        if table not in primary_keys:
            raise ValueError("table inconnue")
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        self.cur.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", tuple(data.values()))
        self.conn.commit()
        return self.cur.lastrowid

    def get_all_characters(self): # returns a list of all characters in the PNJ table as Courtier objects
        self.cur.execute("SELECT * FROM PNJ")
        loops = self.cur.fetchall()
        characters = []
        for loop in loops:
            characters.append(f"|{Courtier(loop[0], loop[1], loop[2], loop[3], loop[4], loop[5])}|")
        return characters

    def get_first_character(self): # returns the first character in the PNJ table as a Courtier object
        return self.get_all_characters()[0] if self.get_all_characters() else None

    def __repr__(self):
        return str(self.get_all_characters())

""" tests pour le update (.update)
if __name__ == "__main__":
    db = Database(conn)
    db.update("Ardinus", "PNJ", "nom", 1)
    print(db)
    db.close()
"""

""" tests pour l'ajout d'un personnage (.add)
if __name__ == "__main__":
    db = Database(conn)
    new_id = db.add("PNJ", {"nom": "Ardouin", "role": "courtier"})
    print(new_id)
    db.add("PNJ", {"role": "king"})
    db.close()
"""
""" tests pour le get_all_characters (.get_all_characters)
if __name__ == "__main__":
    db = Database(conn)
    print(db)
    db.close()
"""

""" tests pour le get_first_character (.get_first_character)
if __name__ == "__main__":
    db = Database(conn)
    print(db.get_first_character())
    db.close()
"""