import sqlite3
from models.courtisan import  Courtisan
from pathlib import Path

chemin_bdd = Path(__file__).parent / "The_prince.db"
conn = sqlite3.connect(chemin_bdd)
cur = conn.cursor()


cur.execute("SELECT * FROM PNJ")
resultats = cur.fetchall()
print(resultats)





premier_tuple = resultats[0]
premier_courtisan = Courtisan(
    premier_tuple[0],
    premier_tuple[1],
    premier_tuple[2],
    premier_tuple[3],
    premier_tuple[4],
    premier_tuple[5]
)
print(premier_courtisan)
print(premier_courtisan.nom)