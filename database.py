import sqlite3
import pandas as pd

df = pd.read_csv("netfit.csv")

conn = sqlite3.connect("netfit.db")

df.to_sql("meresek", conn, if_exists="replace", index=False)

conn.close()

print("Adatbázis létrehozva")

#Lekérdezés

conn = sqlite3.connect("netfit.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM meresek LIMIT 5")

sorok = cursor.fetchall()

for sor in sorok:
    print(sor)

conn.close()

#2 lekérdezés: fiúk fekvőtámasz

conn = sqlite3.connect("netfit.db")
cursor = conn.cursor()
cursor.execute("SELECT nev, fekvotamasz FROM meresek WHERE nem = 'fiú' AND datum = '2025-03-01'")
sorok = cursor.fetchall()
for sor in sorok:
    print(sor)

conn.close()


#fekvőtámasz átlag nemek szerint

print("=====Fekvő átlag első mérés nemek szerint ====")

conn = sqlite3.connect("netfit.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT nem, AVG(fekvotamasz)
    FROM meresek
    WHERE datum = '2025-03-01'
    GROUP BY nem
""")

sorok = cursor.fetchall()
for sor in sorok:
    print(sor)

conn.close()

#Sportoló tanulók átlagos súlya első mérés nemek szerint

print("Sportoló tanulók átlagos súlya első mérés nemek szerint")

conn = sqlite3.connect("netfit.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT nem, AVG(suly)
    FROM meresek
    WHERE datum = '2025-03-01' AND sportolo = 'igen'
    GROUP BY nem
""")
sorok = cursor.fetchall()

for sor in sorok:
    print(sor)

conn.close()

#összes tanuló neve első mérés fekvőtámasz order legjobb --> leggyengébb

print("======Fekvő, első mérés legjobb ---> leggyengébb===")


conn = sqlite3.connect("netfit.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT nev, fekvotamasz
    FROM meresek
    WHERE datum = '2025-03-01'
    ORDER BY fekvotamasz DESC
""")

sorok = cursor.fetchall()

for sor in sorok:
    print(sor)

conn.close()


#Top 3 tanuló neve első mérés fekvőtámasz order legjobb --> leggyengébb

print("====== 3 legjobb fekvőtámaszos első mérésből===")


conn = sqlite3.connect("netfit.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT nev
    FROM meresek
    WHERE datum = '2025-03-01'
    ORDER BY fekvotamasz DESC
    Limit 3
""")

sorok = cursor.fetchall()

for sor in sorok:
    print(sor[0])

conn.close()


#Top 5 lány tanuló neve második mérés távolugrás order legjobb --> leggyengébb

print("====== Top 5 lány tanuló neve második mérés távolugrás order legjobb --> leggyengébb ===")


conn = sqlite3.connect("netfit.db")
cursor = conn.cursor()
cursor.execute("""
    SELECT nev, tavolugrás
    FROM meresek
    WHERE datum = '2026-03-01' AND nem = 'lány'
    ORDER BY tavolugrás DESC
    Limit 5
""")

sorok = cursor.fetchall()

for sor in sorok:
    print(sor)

conn.close()