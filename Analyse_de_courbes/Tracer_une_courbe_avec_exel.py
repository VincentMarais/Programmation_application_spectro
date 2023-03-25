
import pandas as pd
import matplotlib.pyplot as plt
import ezodf
import numpy as np
from scipy.signal import find_peaks

def maximum(liste):
    maxi = liste[0]
    p=0
    for i in range(len(liste)):
        if liste[i] > maxi:
            p = i
            maxi=liste[i]

    return p

Chemin_acces="Manip\Manip_24_03_2023\Fente_0_2mm"

# Lire le fichier ODS
data_1 = pd.read_csv(Chemin_acces +'\solution_blanc.csv', encoding='ISO-8859-1')
data_2= pd.read_csv(Chemin_acces +'\solution_echantillon1.csv', encoding='ISO-8859-1')


# Obtenir les colonnes D et E
Longueur_donde = data_1['Longueur d\'onde (nm)']
Tension_blanc = data_1['Tension blanc (Volt)']
Tension_echantillon= data_2['Tension échantillon (Volt)']
Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))
Pic_d_absorbance=max(Absorbance)
Pic_longueur_donde=Longueur_donde[maximum((Absorbance))]

# Création du graphique
plt.plot(Longueur_donde, Absorbance)
plt.xlabel('Longueur d\'onde (nm)')
plt.ylabel('Absorbance')
plt.title('Absorbance du bromophenol')

# Mise en évidence du point de pic en rouge
plt.scatter(Pic_longueur_donde, Pic_d_absorbance, color='red')


# Annotation des coordonnées du point
plt.annotate('({:.2f} nm, {:.2f})'.format(Pic_longueur_donde, Pic_d_absorbance),
             xy=(Pic_longueur_donde , Pic_d_absorbance),
             xytext=(Pic_longueur_donde + 10 , Pic_d_absorbance),
             fontsize=10,
             color='red',
             arrowprops=dict(facecolor='red', arrowstyle='->'))

# Ligne pointillée reliant le point de pic à l'axe des x
plt.hlines(y=Pic_d_absorbance, xmin=Longueur_donde[0] , xmax=Pic_longueur_donde, linestyle='dashed', color='red')

# Ligne pointillée reliant le point de pic à l'axe des y
plt.vlines(x=Pic_longueur_donde, ymin=min(Absorbance), ymax=Pic_d_absorbance, linestyle='dashed', color='red')
# Affichage du graphique
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