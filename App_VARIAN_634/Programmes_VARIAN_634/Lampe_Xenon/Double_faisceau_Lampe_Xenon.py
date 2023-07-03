import serial  
import numpy as np
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import csv
import pandas as pd
import os
from pyfirmata import Arduino, util
from Commande_moteur.Code_Moteur import deplacer_moteur_miroir , deplacer_vis, etat_mot, param_mot , retour_vis
from Commande_moteur.Fourche_optique import fourche_optique_etat
from Carte_NI_PCI.Acquisition_Tension_NI_6621 import acquisition_tension
from Utilitaires.Creation_fichier_mois_annee import Repertoire_annee_mois_jour, Repertoire_Date_Fente 

 
"""
INITIALISATION DE L'ARDUINO + CARTE NI-PCI 6221
"""
# Constantes
COM_PORT = 'COM3'
BAUD_RATE = 115200
INITIALIZATION_TIME = 2
Frequence_creneau = np.array([20.0]) # 20Hz l'amplitude de la tension est maximal au borne de la photodiode, si on augmente la fréquence au borne de la photodiode => diminution de la tension
Rapport_cyclique = np.array([0.5]) # Déterminer un rapport cyclique optimal pour la mesure
SAMPLES_PER_CHANNEL = 30000 # Nombre d'échantillon récupéré
SAMPLE_RATE = 250000 # Fréquence d'échantillonage maximal de la carte (on récupérer une partie du signal cf critère de Shannon)
CHANNELS = ['Dev1/ai0', 'Dev1/ai1']  

"""
INITIALISATION DE LA MANIP

"""

Repertoire_annee_mois_jour()
[Date, Taille_de_fente] = Repertoire_Date_Fente()


# Initialisation arduino
s = serial.Serial(COM_PORT, BAUD_RATE)
s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(INITIALIZATION_TIME)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.


"""
FOURCHE OPTIQUE
"""

board = Arduino('COM8')
it = util.Iterator(board)
it.start()
pin = board.get_pin('d:3:i')  # d pour digital, 3 pour le pin 3, i pour input






def mode_precision(course_vis, nombre_de_mesures, vitesse_translation_vis, Frequence_creneau, Rapport_cyclique):  # d: distance parcouru par la vis en mm/  n: nombre de mesure de tension / vitesse_translation_vis: vitesse_translation_vis translation de la vis (mm/min)
    """
    Entrée :

    Sortie : 
    
    """

    Tensions_capteur_1= []
    Tensions_capteur_2= []

    Longueur_d_onde=[]
    pas_de_vis=[]
    Absorbance=[]
    i=0
    pas=course_vis/nombre_de_mesures # 0.5mm Pas de la vis (cf Exel)
    temps_par_pas= (pas*60)/vitesse_translation_vis # Temps pour faire un pas 
    
    """
    Initialisation graphe animé
    """

    style.use('ggplot')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    def animate(i):
        ax.clear()
        ax.set_title("Absorbance du bromophenol")
        ax.set_xlabel("Longueur d\'onde (nm)")
        ax.set_ylabel("Absorbance")
        ax.plot(Longueur_d_onde[:i], Absorbance[:i])  
    """
    Initialisation moteur    
    """
    a=fourche_optique_etat()
    print(a)
    if a!='Bonne photodiode':
        while a!='Bonne photodiode':
            a=fourche_optique_etat()
            if a=='Mauvaise photodiode':
                print("TOURNE 0.4 car :", a)                  
                deplacer_moteur_miroir(0.4) # Le moteur doit faire une angle de 60°                 
                time.sleep(1)
                a=fourche_optique_etat()
                print("TOURNE -0.4 car :", a)
                deplacer_moteur_miroir(-0.4) # Le moteur doit faire une angle de 60° 

            else:
                print(a)

        else: 
            print(a)
    g_code= 'G90'+ '\n' # Le moteur ce déplace en relatif
    s.write(g_code.encode())
    time.sleep(0.5)

    g_code= '$110=' + str(vitesse_translation_vis) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)

    """
    Début de l'acquisition de l'absorbance
    """
    while i < course_vis: # Tant que la vis n'a pas parcouru une distance course_vis

        Tension_capteur_1=acquisition_tension(Frequence_creneau, Rapport_cyclique, 'ai0' )
        Tensions_capteur_1.append(Tension_capteur_1) # 
        print("Tension photodiode 1 (Volt) :", Tensions_capteur_1)
        print("Taille de la liste Tension photodiode 1 :", len(Tensions_capteur_1))

        deplacer_moteur_miroir(0.33334) # Le moteur doit faire une angle de 60° 
        time.sleep(0.5)
        Tension_capteur_2=acquisition_tension(Frequence_creneau, Rapport_cyclique, 'ai1' )
        Tensions_capteur_2.append(Tension_capteur_2) # 
        print("Tension photodiode 2 (Volt) :",Tensions_capteur_2)
        print("Taille de la liste photodiode 2 :", len(Tensions_capteur_2))

        deplacer_moteur_miroir(-0.33334) # Le moteur doit faire une angle de 60° 
        time.sleep(0.5)

        pas_de_vis.append(i)
        Longueur_d_onde.append(-31.10419907*i +800) # Je suppose que l'on part à 400nm -> 5.4mm et que l'on fini à 800 nm --> 18.73nm
        
        deplacer_vis(i+pas) # Le moteur travail en mode absolue par défaut G90 
        
        print("Pas de vis (mm) :", i)     
        print("Longueur d\'onde (nm) :", Longueur_d_onde)
        print("Taille de la liste Longueur d\'onde (nm) :", len(Longueur_d_onde))
        
        time.sleep(temps_par_pas) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas
        Tensions_capteur_1.reverse() # On retourne car on commence à 800nm (le rouge) et on termine dans UV 
        Tensions_capteur_2.reverse() # On retourne car on commence à 800nm (le rouge) et on termine dans UV 
        Longueur_d_onde.reverse()

        Absorbance=Absorbance=np.log10(np.abs(Tensions_capteur_1)/np.abs(Tensions_capteur_2))

    """
    Affichage l'absorbance
    """
    Graph_anime = animation.FuncAnimation(fig, animate, interval=50)
    plt.show()

   
    return  Longueur_d_onde, Tensions_capteur_1, Tensions_capteur_2, pas_de_vis




"""
PARTIE ACQUISITION DES DONNEES
""" 

# Fonction pour écrire les données dans un fichier CSV
def sauvegarder_donnees(nom_fichier, Liste_longueurs_d_onde, Liste_tensions, Liste_pas_vis, titre_1, titre_2, titre_3): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    with open(nom_fichier, 'w', newline='', encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2,titre_3])
        for i in range(len(Liste_longueurs_d_onde)):
            writer.writerow([Liste_longueurs_d_onde[i], Liste_tensions[i], Liste_pas_vis[i]])








"""
AFFICHAGE DES DONNEES
"""

def graph(fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin): # fichier_blanc, fichier_echantillon: (str) Chemin d'acces des fichier creer pour l'expérience 
    data_1 = pd.read_csv(fichier_blanc,  encoding='utf-8')
    data_2= pd.read_csv(fichier_echantillon,  encoding='utf-8')

# Obtenir les colonnes 'Longueur d\'onde' et Tension Blanc et Tension echantillon
    Longueur_donde = data_1['Longueur d\'onde (nm)']
    Tension_blanc = data_1['Tension blanc (Volt)']
    Tension_echantillon= data_2['Tension échantillon (Volt)']
    Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))
    Pic_d_absorbance=max(Absorbance)
    Pic_longueur_donde=Longueur_donde[np.argmax((Absorbance))]


# Création du graphique
    plt.plot(Longueur_donde, Absorbance)
    plt.xlabel('Longueur d\'onde (nm)')
    plt.ylabel('Absorbance')
    plt.title('Absorbance du '+ Nom_echantillon)

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
    plt.savefig(chemin +'\\'+ Titre+".pdf")

    plt.show()


"""
ACQUISITION
"""

def solutions(course_vis, nombre_de_mesure, vitesse_translation_vis, Frequence_creneau, Rapport_cyclique, fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin): # Départ 7.25mm / 21 - 7.25 = 13.75mm où 21 course de la vis total de la vis => course_vis=13.75mm
    nom_colonne_tension_blanc='Tension blanc (Volt)'
    nom_colonne_tension_echantillon='Tension échantillon (Volt)'


    [Longueur_d_onde, Tension_blanc, Tension_echantillon, pas_de_vis] = mode_precision(course_vis, nombre_de_mesure, vitesse_translation_vis, Frequence_creneau, Rapport_cyclique)
    
    sauvegarder_donnees(fichier_echantillon, Longueur_d_onde, Tension_echantillon, pas_de_vis, 'Longueur d\'onde (nm)', nom_colonne_tension_echantillon,'Liste_pas_vis')
    sauvegarder_donnees(fichier_blanc, Longueur_d_onde, Tension_blanc, pas_de_vis, 'Longueur d\'onde (nm)', nom_colonne_tension_blanc,'Liste_pas_vis')

    s=str(etat_mot())
    while 'Idle' not in s: # 'Idle': Instruction GRBL pour dire ce que moteur est à l'arrêt / 'Run' le moteur tourne
        s=str(etat_mot())

    print(s)
    
    param_mot()
    retour_vis(course_vis)
    param_mot()

    graph(fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin)







# Concaténer les variables pour former le chemin d'accès complet

chemin = os.path.join("C:\\Users\\vimarais\\Desktop\\Programmation_application_spectro-master\\Manip", Date, Taille_de_fente)

# Vérifier si le répertoire existe déjà
if not os.path.exists(chemin):
    # Créer le répertoire en utilisant le chemin d'accès
    os.makedirs(chemin)
    print("Répertoire créé avec succès :", chemin)
else:
    print("Le répertoire existe déjà :", chemin)


course_vis=13.33 # 7mm
nombre_de_mesures=200 # A modifier si on veut être plus précis
vitesse_translation_vis=10 # 4mm/min



fichier_blanc=  chemin + '\Tension_de_blanc_' + Date + "_" + Taille_de_fente + '.csv'
fichier_echantillon=  chemin + '\Tension_de_echantillon_' + Date + "_" + Taille_de_fente + '.csv'


Nom_echantillon='bleu de bromophenol' # A modifier si on change de composé chimique
Titre="Absorbance_"+ "_" + Nom_echantillon+ Date+"_"+ Taille_de_fente  

solutions(course_vis, nombre_de_mesures, vitesse_translation_vis, np.array([Frequence_creneau]), np.array([Rapport_cyclique]), fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin) # course_vis 13.75 mm / 260 points / vitesse_translation_vis = 4mm/min
#graph(fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin)

#mode_precision(course_vis, nombre_de_mesures, vitesse_translation_vis, Frequence_creneau=np.array([Frequence_creneau]), Rapport_cyclique=np.array([Rapport_cyclique]))

