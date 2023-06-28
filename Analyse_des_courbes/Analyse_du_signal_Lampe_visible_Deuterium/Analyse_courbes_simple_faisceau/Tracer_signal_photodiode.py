import pandas as pd

import matplotlib.pyplot as plt
import numpy as np


"""
Chemin d'accès

"""
DEPART_VIS=19.25
nom_espece_chimique='bromophenol dilué'

"""
Utilitaire
"""
def Indice_maximum(liste):
    maxi = liste[0]
    p=0
    for i in range(len(liste)):
        if liste[i] > maxi:
            p = i
            maxi=liste[i]

    return p

# Course de la vis en absolu
def caracterisation_du_pas_vis(depart,pas_de_vis): # Course de depart de la vis en (mm)
    for i in range (len(pas_de_vis)):
        pas_de_vis[i]=pas_de_vis[i]+depart # Où 19.25 Pour l'UV-VIS
    return pas_de_vis


# Lire le fichier ODS
Chemin_acces="Manip\Manip_24_03_2023\Fente_0_5mm"

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

# Maximum d'
Max_d_absorbance=max(Absorbance)
longueur_donde_absorbe=Longueur_donde[Indice_maximum((Absorbance))]
#Pas_vis_absorbe=pas_de_vis[Indice_maximum((Absorbance))]

def graph_Longueur_donde_Absorbance(nom_espece_chimique):
    # Création du graphique
    plt.plot(Longueur_donde, Absorbance)
    plt.xlabel('Longueur d\'onde (nm)')
    plt.ylabel('Absorbance')
    plt.title('Absorbance du '+ nom_espece_chimique)

    # Mise en évidence du point de pic en rouge
    plt.scatter(longueur_donde_absorbe, Max_d_absorbance, color='red')


    # Annotation des coordonnées du point
    plt.annotate('({:.2f} nm, {:.2f})'.format(longueur_donde_absorbe, Max_d_absorbance),
                xy=(longueur_donde_absorbe , Max_d_absorbance),
                xytext=(longueur_donde_absorbe + 10 , Max_d_absorbance),
                fontsize=10,
                color='red',
                arrowprops=dict(facecolor='red', arrowstyle='->'))

    # Ligne pointillée reliant le point de pic à l'axe des x
    plt.hlines(y=Max_d_absorbance, xmin=Longueur_donde[0] , xmax=longueur_donde_absorbe, linestyle='dashed', color='red')

    # Ligne pointillée reliant le point de pic à l'axe des y
    plt.vlines(x=longueur_donde_absorbe, ymin=min(Absorbance), ymax=Max_d_absorbance, linestyle='dashed', color='red')
    # Affichage du graphique
    plt.show()



def graph_pas_de_vis_Absorbance(nom_espece_chimique, pas_de_vis, Pas_vis_absorbe):
    # Création du graphique
    plt.plot(pas_de_vis, Absorbance)
    plt.xlabel('Course de la vis (mm)')
    plt.ylabel('Absorbance')
    plt.title('Absorbance du '+ nom_espece_chimique)

    # Mise en évidence du point de pic en rouge
    plt.scatter(Pas_vis_absorbe, Max_d_absorbance, color='red')


    # Annotation des coordonnées du point
    plt.annotate('({:.2f} mm, {:.2f})'.format(Pas_vis_absorbe, Max_d_absorbance),
                xy=(Pas_vis_absorbe , Max_d_absorbance),
                xytext=(Pas_vis_absorbe +0.5  , Max_d_absorbance),
                fontsize=10,
                color='red',
                arrowprops=dict(facecolor='red', arrowstyle='->'))

    # Ligne pointillée reliant le point de pic à l'axe des x
    plt.hlines(y=Max_d_absorbance, xmin=pas_de_vis[0] , xmax=Pas_vis_absorbe, linestyle='dashed', color='red')

    # Ligne pointillée reliant le point de pic à l'axe des y
    plt.vlines(x=Pas_vis_absorbe, ymin=min(Absorbance), ymax=Max_d_absorbance, linestyle='dashed', color='red')
    # Affichage du graphique
    plt.show()





graph_Longueur_donde_Absorbance(nom_espece_chimique)


