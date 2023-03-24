import pandas as pd
import matplotlib.pyplot as plt
import ezodf

# Lire le fichier ODS
data = pd.read_excel("Manip\Manip_22_03_2023\expérience_1_echantillon.ods", engine="odf")

# Obtenir les colonnes D et E
col_D = data['Longueur d\'onde (nm)']
col_E = data['Tension échantillon (Volt)']

# Tracer le graphe
plt.plot(col_D, col_E)
plt.xlabel('Nombre de point')
plt.ylabel('Absorbance ')
plt.title('Absorbance du bromophenol')
plt.show()




"""
# Ouverture du fichier ODS
doc = ezodf.opendoc('Manip\Manip_22_03_2023\expérience_1_echantillon.ods')

# Sélection de la première feuille de calcul
sheet = doc.sheets[0]

# Récupération des données dans une liste
donnees = []
for row in sheet.rows():
    donnees.append([cell.value for cell in row])

# Affichage des données
for row in donnees:
    print(row)

"""