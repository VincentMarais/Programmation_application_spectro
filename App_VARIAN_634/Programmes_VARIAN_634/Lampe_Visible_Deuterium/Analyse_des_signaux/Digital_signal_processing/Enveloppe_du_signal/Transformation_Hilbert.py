import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import hilbert, find_peaks
import csv


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
def correction_absorbance_negative(Tension_blanc, Tension_echantillon):
    for i in range (len(Tension_blanc)):
        if np.abs(Tension_blanc[i]) < np.abs(Tension_echantillon[i]): # Ce qui est possible s'il y a du bruit de mesure 
            Tension_echantillon[i]=Tension_blanc[i]
    return Tension_blanc,Tension_echantillon


Tension=correction_absorbance_negative(Tension_blanc,Tension_echantillon)

Absorbance=np.log10(np.abs(Tension[0])/np.abs(Tension[1]))


def sauvegarder_donnees(nom_fichier, Liste, titre): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    Liste=np.real(Liste)
    Liste=Liste.tolist()
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre])
        for i in range(len(Liste)):
            writer.writerow([Liste[i]])

analytic_signal = hilbert(Absorbance)
amplitude_envelope = np.abs(analytic_signal)

plt.figure(figsize=(12, 6))
plt.plot(Longueur_donde, Absorbance, label='Signal original')
plt.plot(Longueur_donde, amplitude_envelope, label="Enveloppe du signal", linestyle='--', color='red')
plt.xlabel("Temps")
plt.ylabel("Amplitude")
plt.legend()
plt.show()

