import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
import csv
import pandas as pd
Chemin_acces="Manip\Manip_24_03_2023\Fente_0_2mm"

# Lire le fichier ODS
data_solution_blanc = pd.read_csv(Chemin_acces +'\solution_blanc.csv', encoding='ISO-8859-1')
data_solution_echantillon= pd.read_csv(Chemin_acces +'\solution_echantillon.csv', encoding='ISO-8859-1')
#data_bruit_de_noir=pd.read_csv(Chemin_acces +'\Tension_de_noir_31_03_2023.csv', encoding='ISO-8859-1')



# Obtenir les colonnes 
Longueur_donde = data_solution_blanc['Longueur d\'onde (nm)']
Tension_blanc = data_solution_blanc['Tension blanc (Volt)']
Tension_echantillon= data_solution_echantillon['Tension échantillon (Volt)']
#pas_de_vis=data_solution_blanc['pas']
#Tension_de_noir=data_bruit_de_noir['Tension de noir (Volt)']
#pas_de_vis=caracterisation_du_pas_vis(DEPART_VIS, pas_de_vis)
Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))


def sauvegarder_donnees(nom_fichier, Liste,Liste_2, titre_1, titre_2 ): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    Liste=np.real(Liste)
    Liste=Liste.tolist()
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2])
        for i in range(len(Liste)):
            writer.writerow([Liste[i], Liste_2[i]])

# Création du spline
longueur_lisse = np.linspace(400, 667.8739000000007, 1000)
spline = UnivariateSpline(Longueur_donde, Absorbance, s=20)

# Prédictions à partir du spline
absorbance_lisse = spline(Longueur_donde)
print(len(Longueur_donde))
# Affichage des résultats
plt.figure()
plt.plot(Longueur_donde, Absorbance, '-', label='Données bruitées')
plt.plot(Longueur_donde, absorbance_lisse, '--', label='Spline')
plt.legend()
plt.xlabel('Longueur d\'onde')
plt.ylabel('Absorbance')
plt.show()
