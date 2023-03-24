
import pandas as pd
import matplotlib.pyplot as plt
import ezodf
import numpy as np


# Lire le fichier ODS
data_1 = pd.read_csv('Fente_0_5mm\solution_blanc.csv', encoding='ISO-8859-1')
data_2= pd.read_csv('Fente_0_5mm\solution_echantillon1.csv', encoding='ISO-8859-1')
# Obtenir les colonnes D et E
Longueur_donde = data_1['Longueur d\'onde (nm)']
Tension_blanc = data_1['Tension blanc (Volt)']
Tension_echantillon= data_2['Tension échantillon (Volt)']
Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))

plt.plot(Longueur_donde, Absorbance)
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

print(max(Absorbance))
print(maximum(Absorbance))
print(Longueur_donde[maximum(Absorbance)]) # Pic d'absorbance

