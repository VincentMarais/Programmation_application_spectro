import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, savgol_filter

# Définir la largeur de la fenêtre de recherche des pics
window_width = 10

# Définir la taille de la fenêtre de lissage
smoothing_window_size = 9

Chemin_acces="Manip\Manip_24_03_2023\Fente_0_5mm"

# Lire le fichier ODS
data_1 = pd.read_csv(Chemin_acces +'\solution_blanc.csv', encoding='ISO-8859-1')
data_2= pd.read_csv(Chemin_acces +'\solution_echantillon1.csv', encoding='ISO-8859-1')


# Obtenir les colonnes D et E
Longueur_donde = data_1['Longueur d\'onde (nm)']
Tension_blanc = data_1['Tension blanc (Volt)']
Tension_echantillon= data_2['Tension échantillon (Volt)']
Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))

# Lissage de la courbe d'absorbance
smoothed_absorbance = savgol_filter(Absorbance, window_length=smoothing_window_size, polyorder=3)

Pic_d_absorbance = smoothed_absorbance.max()

# Trouver l'indice du maximum
s = pd.Series(smoothed_absorbance)
max_index = s.idxmax()

# Récupérer la longueur d'onde associée au maximum
Pic_longueur_donde = Longueur_donde[max_index]


# Recherche des pics d'absorbance
peaks, _ = find_peaks(smoothed_absorbance, distance=window_width)

# Affichage des pics détectés
print('Les pics d\'absorbance se trouvent aux positions suivantes :')
for i in peaks:
    print('{:.2f} nm : {:.2f}'.format(Longueur_donde[i], smoothed_absorbance[i]))

# Tracé de la courbe d'absorbance lissée avec les pics détectés
plt.plot(Longueur_donde, smoothed_absorbance)
plt.plot(Longueur_donde[peaks], smoothed_absorbance[peaks], 'ro')
plt.xlabel('Longueur d\'onde (nm)')
plt.ylabel('Absorbance (lissée)')
plt.title('Absorbance du bromophenol (lissée)')


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