import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# Définir la largeur de la fenêtre de recherche des pics
window_width = 10


# Définir la taille de la fenêtre de lissage
smoothing_window_size = 5

Chemin_acces="Manip\Manip_22_03_2023"

# Lire le fichier ODS
data_1 = pd.read_csv(Chemin_acces +'\expérience_1_echantillon_csv.csv', encoding='ISO-8859-1')
data_2= pd.read_csv(Chemin_acces +'\solution_blanc.csv', encoding='ISO-8859-1')

# Obtenir les colonnes D et E
Longueur_donde = data_2['Longueur d\'onde (nm)']
#Tension_blanc = data_1['Tension blanc (Volt)']
#Tension_echantillon= data_2['Tension échantillon (Volt)']
Absorbance=data_1['log'] # np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))

# Lissage de la courbe d'absorbance
smoothed_absorbance = Absorbance.rolling(smoothing_window_size, center=True).mean()

# Recherche des pics d'absorbance
peaks, _ = find_peaks(smoothed_absorbance, distance=window_width)

# Affichage des pics détectés
print('Les pics d\'absorbance se trouvent aux positions suivantes :')
for i in peaks:
    print('{:.2f} nm : {:.2f}'.format(Longueur_donde[i], smoothed_absorbance[i]))

# Sauvegarde des coordonnées des pics dans un fichier CSV
df = pd.DataFrame({'Longueur d\'onde (nm)': Longueur_donde[peaks], 'Absorbance': Absorbance[peaks]})
df.to_csv(Chemin_acces +'\peaks.csv', index=False)

plt.plot(Longueur_donde, smoothed_absorbance)
plt.plot(Longueur_donde[peaks], smoothed_absorbance[peaks], 'ro')
plt.xlabel('Longueur d\'onde (nm)')
plt.ylabel('Absorbance (lissée)')
plt.title('Absorbance du bromophenol (lissée)')

# Affichage du graphique
plt.show()
# Affichage du graphique
plt.show()
