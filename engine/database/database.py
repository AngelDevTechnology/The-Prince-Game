import sqlite3
from engine.models.courtier import  Courtier
from pathlib import Path

path_bdd = Path(__file__).parent / "The_prince.db"
conn = sqlite3.connect(path_bdd)
cur = conn.cursor()


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
    first_tuple[5]
)
print(first_courtier) 
print(first_courtier.name)