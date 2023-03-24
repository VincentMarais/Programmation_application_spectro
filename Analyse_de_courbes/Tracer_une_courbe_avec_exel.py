import pandas as pd
import matplotlib.pyplot as plt
import ezodf

# Lire le fichier ODS
data_1 = pd.read_csv('Manip\Manip_22_03_2023\solution_blanc.csv', encoding='ISO-8859-1')
data_2= pd.read_csv('Manip\Manip_22_03_2023\expérience_1_echantillon_csv.csv', encoding='ISO-8859-1')
# Obtenir les colonnes D et E
col_D = data_1['Longueur d\'onde (nm)']
col_E = data_2['log']

# Tracer le graphe
plt.plot(col_D, col_E)
plt.xlabel('Nombre de point')
plt.ylabel('Absorbance ')
plt.title('Absorbance du bromophenol')
plt.show()

def maximum(liste):
    maxi = liste[0]
    p=0
    for i in range(len(liste)):
        if liste[i] > maxi:
            p = i
            maxi=liste[i]

    return p

print(col_D[maximum(col_E)]) # Pic d'absorbance




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