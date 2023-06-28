import numpy as np
import matplotlib.pyplot as plt
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


# Calculer la transformée de Fourier du signal
fourier_transform = np.fft.fft(Tension_echantillon, n=4096) # 4096 Pour plus de précision fft (zero padding) cf https://www.youtube.com/watch?v=LAswxBR513M&t=582s&ab_channel=VincentChoqueuse
f=10*np.arange(4096)/4096  # 10: Fréquence d'échantillonage Phidget 
nom_fichier=Chemin_acces+'\Transforme_de_fourier_Manip_24_03_2023_Fente_0_2mm.csv'
titre_2='Transforme_de_fourier'
titre='Frequence_(Hz)'
fourier_transform=np.abs(fourier_transform) 
"""
sauvegarder_donnees(nom_fichier, f, fourier_transform, titre,titre_2)
Chemin_Latex= Chemin_acces + '\signal_Manip_24_03_2023_Fente_0_2mm.csv'
sauvegarder_donnees(Chemin_Latex, Longueur_donde, Absorbance, "Longueur_d_onde_(nm)", "Absorbance")
"""
plt.plot(f,fourier_transform, color='red')
plt.xlabel('Fréquence (Hz)')
plt.ylabel('Module de la transformée de Fourier')
plt.xlim([0,5])

plt.show()
plt.plot(Longueur_donde,Tension_blanc)
plt.xlabel('Longueur d\'onde (nm)')
plt.ylabel('Absorbance')
plt.show()
# Comparer les signaux original et filtré (par exemple, en les traçant)


