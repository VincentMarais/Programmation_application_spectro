import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, savgol_filter,hilbert # https://www.youtube.com/watch?v=1SvDZPvUo_I&ab_channel=KiyonoLab (Vidéo sur savgol_Filter)
import csv
from scipy.interpolate import UnivariateSpline

#CONSTANTE
DEPART_VIS=19.25 # Analyse UV départ de la vis à 19.25mm


"""
VARIABLES

"""

Fenetre_recherche_pic = 30 # Définir la largeur de la fenêtre de recherche des pics
Largeur_fonction_porte = 30 # reglage opti (Fente 0_2mm): 23 / (Fente 0_5mm): 30 / (Fente 1mm): 15 / (Fente 2mm): 30 (# Définir la taille de la fenêtre de lissage)
Chemin_acces="Manip\Manip_22_03_2023"
Manip='Manip_24_03_2023_Fente_1mm'

# Lire le fichier ODS
data_solution_blanc = pd.read_csv(Chemin_acces +'\solution_blanc.csv', encoding='ISO-8859-1')
data_solution_echantillon= pd.read_csv(Chemin_acces +'\expérience_1_echantillon.csv', encoding='ISO-8859-1')
#data_bruit_de_noir=pd.read_csv(Chemin_acces +'\Tension_de_noir_31_03_2023.csv', encoding='ISO-8859-1')


"""
Caractérisation du pas de vis
"""
# Course de la vis en absolu
def caracterisation_du_pas_vis(depart, pas_de_vis): # Course de depart de la vis en (mm)
    for i in range (len(pas_de_vis)):
        pas_de_vis[i]=pas_de_vis[i]+depart # Où 19.25 Pour l'UV-VIS
    return pas_de_vis


"""

Correction préliminaire du signal

"""


# Supprimmer le bruit de noir
def correction_bruit_de_noir(Tension_solution,Tension_de_noir):
    valeur_moyenne_tension_de_noir=np.mean(Tension_de_noir)
    for i in range(Tension_solution):
        Tension_solution[i]= Tension_solution[i] - valeur_moyenne_tension_de_noir
    return Tension_solution



# Supprimer les absorbances négatives 
def correction_absorbance_negative(Tension_blanc, Tension_echantillon):
    """
    Fonction qui corrige le bruit de mesure qui si I_0 < I n'est pas valable dans notre cas la solution est cencé absorbé de l'énergie lumineuse
    """
    for i in range (len(Tension_blanc)):
        if np.abs(Tension_blanc[i]) < np.abs(Tension_echantillon[i]): # Ce qui est possible s'il y a du bruit de mesure 
            Tension_echantillon[i]=Tension_blanc[i]
    return Tension_blanc,Tension_echantillon


def zero_absorbance(Absorbance_lisse, Absorbance_spline):
    """
    Fonction qui mettre l'absorbance de mon signal lissé à zéro si elle est cencé l'être avec correction absorbance negatif
    """
    for i in range(len(Absorbance_lisse)):
        if Absorbance_lisse[i]==0:
            Absorbance_spline[i]=0
    return Absorbance_spline


"""

Acquisition des données

"""
# Obtenir les colonnes 
Longueur_donde = data_solution_blanc['Longueur d\'onde (nm)']
Tension_blanc = data_solution_echantillon['Tension blanc (Volt)']
Tension_echantillon= data_solution_echantillon['Tension échantillon (Volt)']
#pas_de_vis=data_solution_blanc['pas']
#Tension_de_noir=data_bruit_de_noir['Tension de noir (Volt)']
Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))

"""
Correction des données
"""


# Correction bruit de noir
#Tension_blanc=correction_bruit_de_noir(Tension_blanc, Tension_de_noir)
#Tension_echantillon=correction_bruit_de_noir(Tension_echantillon, Tension_de_noir)

#Correction absorbance négatives
[Tension_blanc,Tension_echantillon]=correction_absorbance_negative(Tension_blanc,Tension_echantillon)


# Calcul de l'absorbance
Absorbance_negatif_corrig=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))

# Analyse UV départ de la vis à 19.25mm
#pas_de_vis=caracterisation_du_pas_vis(DEPART_VIS)


"""
La moyenne mobile (ou moyenne glissante) est une technique couramment utilisée pour lisser une série chronologique 
(ou une série de données échantillonnées) 
en supprimant le bruit et en mettant en évidence les tendances à long terme. 
La moyenne mobile est calculée en prenant la moyenne des valeurs d'une fenêtre glissante de données, 
qui se déplace à travers la série chronologique en prenant les données 
à chaque étape et en calculant la moyenne des valeurs dans la fenêtre.

"""
# Lissage de la courbe d'Absorbance avec un produit de convolution discret et une fonction porte
smoothed_absorbance = np.convolve(Absorbance_negatif_corrig, np.ones(Largeur_fonction_porte)/Largeur_fonction_porte, mode='same') # Je fais le produit de convolution de mon signal avec une  fonction porte de taille Largeur_fonction_porte
    
spline = UnivariateSpline(Longueur_donde, smoothed_absorbance, s=0.05)
"""
Lorsque vous ajustez s, vous modifiez la pénalité appliquée aux différences entre les 
données et la courbe de spline. Plus la valeur de s est grande, plus le lissage 
est important, ce qui donne une courbe de spline plus douce et moins sensible au bruit des données. 
Inversement, si la valeur de s est faible, la courbe de spline sera plus proche des données bruitées, avec moins de lissage

"""

# Prédictions à partir du spline
smoothed_absorbance = spline(Longueur_donde)


smoothed_absorbance = zero_absorbance(smoothed_absorbance,smoothed_absorbance)


"""
Rercherche des pics
"""
# Recherche des pics d'absorbance
peaks, _ = find_peaks(smoothed_absorbance, distance=Fenetre_recherche_pic) # La fonction find_peaks de scipy.signal permet de trouver les maxima locaux dans un signal en comparant les valeurs voisines

"""
Sauvegarde des données
"""
def sauvegarder_donnees(nom_fichier, Liste,Liste_2, titre_1, titre_2 ): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    Liste=np.real(Liste)
    Liste=Liste.tolist()
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2])
        for i in range(len(Liste)):
            writer.writerow([Liste[i], Liste_2[i]])


"""
AFFICHAGE DES DONNNEES
"""



def graph_Longueur_donde_Absorbance(nom_espece_chimique):   

    # Affichage des pics détectés
    print('Les pics d\'absorbance se trouvent aux positions suivantes :')
    for i in peaks:
        print('{:.2f} nm : {:.2f}'.format(Longueur_donde[i], smoothed_absorbance[i]))


    # Calculer le maximum d'absorbance
    Max_absorbance = smoothed_absorbance.max()

    # Trouver la longueur lié au maximum d'absorbance 
    s = pd.Series(smoothed_absorbance)
    max_index = s.idxmax()

    df = pd.DataFrame({'Longueur_d_onde_(nm)': Longueur_donde[peaks], 'Absorbance': smoothed_absorbance[peaks]})
    df.to_csv(Chemin_acces +'\peaks_longueur_donde_'+Manip+'.csv', index=False)

    longueur_donde_absorbe = Longueur_donde[max_index]

    plt.plot(Longueur_donde, smoothed_absorbance, '--', label='Données lissé')
    plt.plot(Longueur_donde[peaks], smoothed_absorbance[peaks], 'ro')
    plt.xlabel('Longueur d\'onde (nm)')
    plt.ylabel('Absorbance (lissée)')
    plt.title('Absorbance du ' + nom_espece_chimique + ' (lissée)')

    # Affichage des coordonnées de tout les pics
    for i in peaks:
        plt.annotate('({:.2f} nm, {:.2f})'.format(Longueur_donde[i], smoothed_absorbance[i]),
                    xy=(Longueur_donde[i], smoothed_absorbance[i]),
                    xytext=(Longueur_donde[i] + 10, smoothed_absorbance[i]),
                    fontsize=10,
                    color='red',
                    arrowprops=dict(facecolor='red', arrowstyle='->'))



    # Affichage du maximum d'absorbance 
    plt.annotate('({:.2f} nm, {:.2f})'.format(longueur_donde_absorbe, Max_absorbance),
                xy=(longueur_donde_absorbe , Max_absorbance),
                xytext=(longueur_donde_absorbe + 10 , Max_absorbance),
                fontsize=10,
                color='red',
                arrowprops=dict(facecolor='red', arrowstyle='->'))


    # Ligne pointillée reliant le point de pic à l'axe des x
    plt.hlines(y=Max_absorbance, xmin=Longueur_donde[0] , xmax=longueur_donde_absorbe, linestyle='dashed', color='red')

    # Ligne pointillée reliant le point de pic à l'axe des y
    plt.vlines(x=longueur_donde_absorbe, ymin=min(smoothed_absorbance), ymax=Max_absorbance, linestyle='dashed', color='red')

    # Affichage du graphique
    plt.show()




def Graph_Course_vis_absorbance(nom_espece_chimique,pas_de_vis):

     # Affichage des pics détectés
    print('Les pics d\'absorbance se trouvent aux positions suivantes :')
    for i in peaks:
        print('{:.2f} mm : {:.2f}'.format(pas_de_vis[i], smoothed_absorbance[i]))


    # Calculer le maximum d'absorbance
    Max_absorbance = smoothed_absorbance.max()

    # Trouver la longueur lié au maximum d'absorbance 
    s = pd.Series(smoothed_absorbance)
    max_index = s.idxmax()
    pas_vis_absorbe = pas_de_vis[max_index]

    df = pd.DataFrame({'Pas (mm)': pas_de_vis[peaks], 'Absorbance': smoothed_absorbance[peaks]})
    df.to_csv(Chemin_acces +'\peaks_pas_vis.csv', index=False)

    plt.figure()
    plt.plot(pas_de_vis, Absorbance, '-', label='Données bruitées')
    plt.plot(pas_de_vis, smoothed_absorbance, '--', label='Données lissé')
    plt.legend()
    plt.xlabel('Course de la vis (mm)')
    plt.ylabel('Absorbance (lissée)')
    plt.title('Absorbance du ' + nom_espece_chimique + ' (lissée)')

    # Affichage des coordonnées de tout les pics
    for i in peaks:
        plt.annotate('({:.2f} mm, {:.2f})'.format(pas_de_vis[i], smoothed_absorbance[i]),
                    xy=(pas_de_vis[i], smoothed_absorbance[i]),
                    xytext=(pas_de_vis[i] + 0.5 , smoothed_absorbance[i]),
                    fontsize=10,
                    color='red',
                    arrowprops=dict(facecolor='red', arrowstyle='->'))


    
    # Affichage du maximum d'absorbance 
    plt.annotate('({:.2f} mm, {:.2f})'.format(pas_vis_absorbe, Max_absorbance),
                xy=(pas_vis_absorbe , Max_absorbance),
                xytext=(pas_vis_absorbe + 0.5 , Max_absorbance),
                fontsize=10,
                color='red',
                arrowprops=dict(facecolor='red', arrowstyle='->'))


    # Ligne pointillée reliant le point de pic à l'axe des x
    plt.hlines(y=Max_absorbance, xmin=pas_de_vis[0] , xmax=pas_vis_absorbe, linestyle='dashed', color='red')

    # Ligne pointillée reliant le point de pic à l'axe des y
    plt.vlines(x=pas_vis_absorbe, ymin=min(Absorbance), ymax=Max_absorbance, linestyle='dashed', color='red')

    # Affichage du graphique
    plt.show()

nom_espece_chimique='bromophenol dilué'
graph_Longueur_donde_Absorbance(nom_espece_chimique)
#Graph_Course_vis_absorbance(nom_espece_chimique)







