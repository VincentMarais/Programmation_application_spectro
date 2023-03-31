import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, savgol_filter # https://www.youtube.com/watch?v=1SvDZPvUo_I&ab_channel=KiyonoLab (Vidéo sur savgol_Filter)

"""
Utilitaire

"""
def analyse_de_la_tension(Tension_blanc, Tension_echantillon):

    for i in range (len(Tension_blanc)):
        if np.abs(Tension_blanc[i]) < np.abs(Tension_echantillon[i]): # Ce qui est possible s'il y a du bruit de mesure 
            Tension_echantillon[i]=Tension_blanc[i]
    return Tension_blanc,Tension_echantillon

# Définir la largeur de la fenêtre de recherche des pics
window_width = 15


# Définir la taille de la fenêtre de lissage
Largeur_fonction_porte = 30 # reglage opti (Fente 0_2mm): 23 / (Fente 0_5mm): 30 / (Fente 1mm): 15 / (Fente 2mm): 30

"""
Lire le fichier

"""
Chemin_acces="Manip\Manip_28_03_2023"



# Lire le fichier ODS
data_1 = pd.read_csv(Chemin_acces +'\solution_blanc1_28_03_2023.csv', encoding='ISO-8859-1')
data_2= pd.read_csv(Chemin_acces +'\solution_echantillon1_28_03_2023.csv', encoding='ISO-8859-1')

# Obtenir les colonnes 
Longueur_donde = data_1['Longueur d\'onde (nm)']
Tension_blanc = data_1['Tension blanc (Volt)']
Tension_echantillon= data_2['Tension échantillon (Volt)']
[Tension_blanc,Tension_echantillon]=analyse_de_la_tension(Tension_blanc,Tension_echantillon)
Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))




"""
La moyenne mobile (ou moyenne glissante) est une technique couramment utilisée pour lisser une série chronologique 
(ou une série de données échantillonnées) 
en supprimant le bruit et en mettant en évidence les tendances à long terme. 
La moyenne mobile est calculée en prenant la moyenne des valeurs d'une fenêtre glissante de données, 
qui se déplace à travers la série chronologique en prenant les données 
à chaque étape et en calculant la moyenne des valeurs dans la fenêtre.

"""

smoothed_absorbance = np.convolve(Absorbance, np.ones(Largeur_fonction_porte)/Largeur_fonction_porte, mode='same') # Je fais le produit de convolution de mon signal avec une  fonction porte de taille Largeur_fonction_porte



"""

Rercherche des pics

"""
# Recherche des pics d'absorbance
peaks, _ = find_peaks(smoothed_absorbance, distance=window_width)

# Affichage des pics détectés
print('Les pics d\'absorbance se trouvent aux positions suivantes :')
for i in peaks:
    print('{:.2f} nm : {:.2f}'.format(Longueur_donde[i], smoothed_absorbance[i]))


Max_absorbance = smoothed_absorbance.max()

# Trouver l'indice du Pic d'absorbance 
s = pd.Series(smoothed_absorbance)
max_index = s.idxmax()

# Récupérer la longueur d'onde associée au maximum
longueur_donde_absorbe = Longueur_donde[max_index]


"""
AFFICHAGE DES DONNNEES

"""


# Sauvegarde des coordonnées des pics dans un fichier CSV
df = pd.DataFrame({'Longueur d\'onde (nm)': Longueur_donde[peaks], 'Absorbance': Absorbance[peaks]})
df.to_csv(Chemin_acces +'\peaks.csv', index=False)


plt.plot(Longueur_donde, smoothed_absorbance)
plt.plot(Longueur_donde[peaks], smoothed_absorbance[peaks], 'ro')
plt.xlabel('Longueur d\'onde (nm)')
plt.ylabel('Absorbance (lissée)')
plt.title('Absorbance du bromophenol (lissée)')


for i in peaks:
    plt.annotate('({:.2f} nm, {:.2f})'.format(Longueur_donde[i], smoothed_absorbance[i]),
                 xy=(Longueur_donde[i], smoothed_absorbance[i]),
                 xytext=(Longueur_donde[i] + 10, smoothed_absorbance[i]),
                 fontsize=10,
                 color='red',
                 arrowprops=dict(facecolor='red', arrowstyle='->'))



plt.annotate('({:.2f} nm, {:.2f})'.format(longueur_donde_absorbe, Max_absorbance),
             xy=(longueur_donde_absorbe , Max_absorbance),
             xytext=(longueur_donde_absorbe + 10 , Max_absorbance),
             fontsize=10,
             color='red',
             arrowprops=dict(facecolor='red', arrowstyle='->'))


# Ligne pointillée reliant le point de pic à l'axe des x
plt.hlines(y=Max_absorbance, xmin=Longueur_donde[0] , xmax=longueur_donde_absorbe, linestyle='dashed', color='red')

# Ligne pointillée reliant le point de pic à l'axe des y
plt.vlines(x=longueur_donde_absorbe, ymin=min(Absorbance), ymax=Max_absorbance, linestyle='dashed', color='red')
# Affichage du graphique
plt.show()
