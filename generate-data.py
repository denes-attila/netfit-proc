import csv
import random


fiuk = ["Bence", "Máté", "Dávid", "Ádám", "Péter", "Balázs", "Gábor", "László", "Tamás", "Zoltán"]
lanyok = ["Anna", "Eszter", "Réka", "Zsófia", "Kata", "Borbála", "Nóra", "Júlia", "Veronika", "Ágnes"]


students = []

for fiu in fiuk:
    dict = {
        "nev": fiu,
        "nem": "fiú",
        "kor": random.randint(10, 14),
        "sportolo": random.choice(["igen", "nem"]),
        "datum": "2025-03-01",
        "suly": random.randint(30, 100),
        "magassag": random.randint(155, 195),
        "testzsir": round(random.uniform(8, 25), 1),
        "tavolugrás": random.randint(120, 220),
        "ingafutas": random.randint(20, 80),
        "fekvotamasz": random.randint(5, 50),
        "hajlekonysag": random.randint(10, 50),
        "szoritoeró": random.randint(20, 60),
        "torzsemeles": random.randint(10, 40)
        }
    students.append(dict)
for lany in lanyok:
    dict = {
        "nev": lany,
        "nem": "lány",
        "kor": random.randint(10, 14),
        "sportolo": random.choice(["igen", "nem"]),
        "datum": "2025-03-01",
        "suly": random.randint(20, 100),
        "magassag": random.randint(155, 195),
        "testzsir": round(random.uniform(8, 25), 1),
        "tavolugrás": random.randint(120, 220),
        "ingafutas": random.randint(20, 80),
        "fekvotamasz": random.randint(5, 50),
        "hajlekonysag": random.randint(10, 50),
        "szoritoeró": random.randint(20, 60),
        "torzsemeles": random.randint(10, 40)
        }
    students.append(dict)

elso_meres = students.copy()


for student in elso_meres:
    dict = {
        "nev": student["nev"],
        "nem": student["nem"],
        "kor": student["kor"] +1,
        "sportolo": random.choice(["igen", "nem"]),
        "datum": "2026-03-01",
        "suly": student["suly"] +random.randint(-5, 5),
        "magassag": student["magassag"] + random.randint(0,10),
        "testzsir": round(random.uniform(8, 25), 1),
        "tavolugrás": student["tavolugrás"] +random.randint(0, 20),
        "ingafutas": random.randint(20, 80),
        "fekvotamasz": student["fekvotamasz"] + random.randint(-2, 5),
        "hajlekonysag": student["hajlekonysag"] + random.randint(-5,5),
        "szoritoeró": student["szoritoeró"] + random.randint(-5, 20),
        "torzsemeles": student["torzsemeles"] + random.randint(-5, 10)
        }
    students.append(dict)

with open("netfit.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames = students[0].keys())
    writer.writeheader()
    writer.writerows(students)