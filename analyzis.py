from datetime import date
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("netfit.csv")
elso_meres = df[df["datum"] == "2025-03-01"]
masodik_meres = df[df["datum"] == "2026-03-01"]


fejlodes = elso_meres.merge(masodik_meres, on ="nev" , suffixes=("_1", "_2"))

meresek = ["suly", "magassag", "testzsir", "tavolugrás", "ingafutas",
           "fekvotamasz", "hajlekonysag", "szoritoeró", "torzsemeles"]

for m in meresek:
    fejlodes[f"{m}_valtozas"] = fejlodes[f"{m}_2"] - fejlodes[f"{m}_1"]


valtozas_oszlopok = ["nev"] + [f"{m}_valtozas" for m in meresek]

#print(fejlodes[valtozas_oszlopok].to_string(index=False))


legjobb_idx = fejlodes["fekvotamasz_valtozas"].idxmax()
legjobb_tanulo = fejlodes.loc[legjobb_idx, "nev"]
legjobb_ertek = fejlodes.loc[legjobb_idx, "fekvotamasz_valtozas"]

print(f"Legjobban fejlődött fekvőtámaszban: {legjobb_tanulo} (+ {legjobb_ertek})")


print("=== Legjobban fejlődő tanulók területenként ====")
for m in meresek:
    idx = fejlodes[f"{m}_valtozas"].idxmax()
    nev = fejlodes.loc[idx, "nev"]
    ertek = fejlodes.loc[idx, f"{m}_valtozas"]

    print(f"{m:15} -> {nev} (+ {ertek})")


print("=====Fiú lány átlagok első mérés.====")
atlagok = elso_meres.groupby("nem")[meresek].mean().round(1)
print(atlagok)

#Átalgos fejlődés nemek szerint:

print("===Átlagos fejlődés nemek szerint====")

valtozas_oszlopok = [f"{m}_valtozas" for m in meresek]
fejlodes_atlag = fejlodes.groupby("nem_1")[valtozas_oszlopok].mean().round(1)
print(fejlodes_atlag)


print("====Sportoló és nem sportoló tanulók átlagai (első mérés)")

atlagok_sport = elso_meres.groupby("sportolo")[meresek].mean().round(1)
print(atlagok_sport)

#Sportoló/nem sportolók változásainak átlaga

print("Sportolók nem sportolók változásainak átlaga")
fejlodes_sport = fejlodes.groupby("sportolo_1")[valtozas_oszlopok].mean().round(1)
print(fejlodes_sport)


#BMI számítás első mérésből
elso_meres = elso_meres.copy()
elso_meres["bmi"] = elso_meres["suly"] / (elso_meres["magassag"] / 100)**2
elso_meres["bmi"] = elso_meres["bmi"].round(1)

print("===Első mérés bmi:")
print (elso_meres[["nev","suly","magassag", "bmi"]])


#masodik mérés
masodik_meres = masodik_meres.copy()
masodik_meres["bmi"] = masodik_meres["suly"] / (masodik_meres["magassag"] / 100) ** 2
masodik_meres["bmi"] = masodik_meres["bmi"].round(1)
print("===Második mérés bmi:")
print (masodik_meres[["nev","suly","magassag", "bmi"]])


print("============Első grafikon =======")

atlagok.T.plot(kind= "bar", figsize=(12,5))
plt.title("Fiú/lány átlagok első mérés")
plt.xlabel("Mért értékek")
plt.ylabel("Átlag")
plt.xticks(rotation=45, ha="right")
plt.savefig("fiu_lany_diagram.png", dpi=150)
plt.close()


nev = "Bence"
tanulo = df[df["nev"] == nev]

x = tanulo["datum"]
y = tanulo["fekvotamasz"]

plt.plot(x,y, marker="o")
plt.title(f"{nev} - fekvőtámasz fejlődése")
plt.ylabel("ismétlés")
plt.grid(True)
plt.savefig("Bence_diagram.png", dpi=150)
plt.close()


#Sportoló/nem sportoló átlagok diagrammja

atlagok_sport.T.plot(kind = "bar", figsize=(12,5))
plt.title("Sportoló/nem sportoló első mérés átlagai")
plt.xlabel("Mért értékek")
plt.ylabel("Átlag")
plt.xticks(rotation = 45, ha = "right")
plt.tight_layout()
plt.savefig("sportolo_nem_sportolo_diagram.png", dpi = 150)
plt.close()

pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
c = canvas.Canvas("netfit_report.pdf")

c.setFont("DejaVu", 16)
c.drawString(50, 800, "NETFIT Report")

c.setFont("DejaVu", 12)
c.drawString(50, 770, "Osztály összesítő - 2026")

c.drawImage("fiu_lany_diagram.png", 50, 400, width=500, height=250)
c.showPage()
c.drawImage("sportolo_nem_sportolo_diagram.png", 50, 400, width=500, height=250)
c.showPage()
c.drawImage("Bence_diagram.png", 50, 400, width=500, height=250)
c.showPage()
c.save()


def tanulo_riport(nev):
    #adatok kiszure
    tanulo_adatok = fejlodes[fejlodes["nev"] == nev].iloc[0]

    c = canvas.Canvas(f"riport_{nev}.pdf")
    c.setFont("DejaVu", 20)
    c.drawString(50, 800, f"NETFIT Report - {nev}")

    c.setFont("DejaVu", 12)
    c.drawString(50, 760, f"Kor: {tanulo_adatok["kor_1"]} Nem: {tanulo_adatok["nem_1"]} Sportoló: {tanulo_adatok["sportolo_1"]}")

    #mérések táblázat
    y = 720
    c.drawString(50, y, f"{'Mutató':<20} {'2025':>10} {'2026':>10} {'Változás':>10}")
    y -= 20
    
    for m in meresek:
        sor = f"{m:<20} {tanulo_adatok[f'{m}_1']:>10} {tanulo_adatok[f'{m}_2']:>10} {tanulo_adatok[f'{m}_valtozas']:>10}"
        c.drawString(50, y, sor)
        y -= 20
    
    c.save()

tanulo_riport("Bence")


for nev in df["nev"].unique():
    tanulo_riport(nev)

def osztaly_riport():
    c = canvas.Canvas("osztaly_riport.pdf")

    #Cím:
    c.setFont("DejaVu", 22)
    c.drawString(50, 800, "NETFIT Osztály összesítő riport")

    c.setFont("DejaVu", 12)
    c.drawString(50, 765, f"Dátum: {date.today()}")
    c.drawString(50, 745, f"Tanulók száma: {len(df['nev'].unique())}")
    c.drawString(50, 725, f"Első mérés: 2025-03-01  Második mérés: 2026-03-01")

    # Új oldal – táblázat
    c.showPage()
    c.setFont("DejaVu", 16)
    c.drawString(50, 800, "Fiú/lány átlagok – első mérés")

    atlagok = elso_meres.groupby("nem")[meresek].mean().round(1)

    y =760
    c.setFont("DejaVu", 11)
    c.drawString(50, y, f"{'Mutato': <20} {'Fiú': >10} {'Lány': >10}")

    y -=20

    for m in meresek:
        sor = sor = f"{m:<20} {atlagok.loc['fiú', m]:>10} {atlagok.loc['lány', m]:>10}"
        c.drawString(50, y, sor)
        y -= 20

    c.showPage()
    c.setFont("DejaVu", 16)
    c.drawString(50,800, "Fiú/Lány átlagok-diagram")
    c.drawImage("fiu_lany_diagram.png", 50, 450, width=500, height=250)

    c.showPage()
    c.drawString(50,800, "Sportoló/Nem sportoló - diagram")
    c.drawImage("sportolo_nem_sportolo_diagram.png", 50, 450, width=500, height=250)
    
    c.save()

osztaly_riport()

