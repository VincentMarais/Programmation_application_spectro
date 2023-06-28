import serial  
import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import re
import os


 
"""
INITIALISATION DE L'ARDUINO + PHIDGET
"""
# Constantes Arduino
COM_PORT = 'COM5'
BAUD_RATE = 115200
# Constantes Carte NI-6221
# Configurations lorsque le signal de commande de la lampe au xénon est réglé à 20Hz : SAMPLES_PER_CHANNEL=30000 / SAMPLE_RATE=250000

INITIALIZATION_TIME = 2
TEMPS_ATTENTE_PHIDGET=5000
SAMPLES_PER_CHANNEL = 30000
SAMPLE_RATE = 250000
CHANNELS = ['Dev1/ai0']  # Remplacez ceci par le nom de votre canal
NUM_ACQUISITIONS = 10  # Remplacez ceci par le nombre d'acquisitions que vous souhaitez effectuer
INPUT_RANGE = 0.2  # Gamme de tension en Volts


# Initialisation arduino
s = serial.Serial(COM_PORT, BAUD_RATE)
s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(INITIALIZATION_TIME)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.



""" 
Programme MOTEUR

"""
def etat_mot():
    g_code='?' + '\n'
    s.write(g_code.encode())

    return s.read(10)

def param_mot():    
    g_code='$G' + '\n'
    s.write(g_code.encode())
    print(s.read(75))


def position_XYZ_vis():
    g_code= "?" + '\n' 
    s.write(g_code.encode())
    time.sleep(0.1)

    # Lire et traiter la réponse
    response = str(s.readline())
    while 'MPos' not in response:
        response = str(s.readline())
    
    # Extraire les coordonnées X, Y, et Z
    match = re.search(r"MPos:([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+)", response)
        
    x_pos, y_pos, z_pos = [float(coordinate) for coordinate in match.groups()]
    
    return x_pos



def deplacer_vis(pas): # Fonction qui pilote le moteur      
        gcode_1= 'G0X' + str(pas) + '\n'
        s.write(gcode_1.encode())
        


def retour_vis(pas): 
        g_code= '$110=10'+ '\n' # On modifie la vitesse_translation_vis de translation de la vis (mm/min)
        s.write(g_code.encode())
        time.sleep(0.5)
        g_code= 'G91'+ '\n' # Le moteur ce déplace en relatif
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X-' + str(pas) + '\n' # Le moteur ce déplace linéairement de -pas (retour_vis en arrière)
        s.write(gcode_1.encode())


def modif_vitesse_translation_vis(vitesse_translation):
    g_code = '$110=' + str(vitesse_translation) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)

"""
PROGRAMME CARTE NI 6221
"""

def acquiere_tensions():
    with nidaqmx.Task() as task:
        # Configurer la tâche
        for channel in CHANNELS:
            task.ai_channels.add_ai_voltage_chan(channel, terminal_config=TerminalConfiguration.DIFF)
        
        task.timing.cfg_samp_clk_timing(SAMPLE_RATE, samps_per_chan=SAMPLES_PER_CHANNEL,
                                        sample_mode=AcquisitionType.FINITE, min_val=-INPUT_RANGE, max_val=INPUT_RANGE)
        for _ in range(NUM_ACQUISITIONS):
            # Acquisition des données
            data = task.read(number_of_samples_per_channel=SAMPLES_PER_CHANNEL)
            
            # Conversion des données en un tableau numpy pour faciliter les calculs
            np_data = np.array(data)
            
            # Trouver et stocker le minimum
            min_voltage = np.min(np_data)

    return min_voltage


"""
LIEN MOTEUR ET CARTE NI 6221

"""


def mode_precision(course_vis, nombre_de_mesures, vitesse_translation_vis):  # d: distance parcouru par la vis en mm/  n: nombre de mesure de tension / vitesse_translation_vis: vitesse_translation_vis translation de la vis (mm/min)
    Tension_CARTE_NI= []
    Longueur_d_onde=[]
    pas_de_vis=[]
    i=0
    pas=course_vis/nombre_de_mesures # 0.5mm Pas de la vis (cf Exel)
    temps_par_pas= (pas*60)/vitesse_translation_vis # Temps pour faire un pas 
    Temps_acquisition_carte=1
    #Initialisation du moteur (vitesse de rotation)
    g_code= '$110=' + str(vitesse_translation_vis) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)
    
    while i < course_vis: # Tant que la vis n'a pas parcouru une distance course_vis
        Tension_CARTE_NI.append(acquiere_tensions()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        pas_de_vis.append(i)
        
        Longueur_d_onde.append(31.10419907*i +200) # Je suppose que l'on part à 400nm -> 0mm et que l'on fini à 800 nm --> 20.8mm => 19.23= coefficient directeur de la droite lambda = a*x + 400 nm où x position de la vis
        deplacer_vis(i+pas) # Le moteur travail en mode absolue par défaut G90 
        time.sleep(Temps_acquisition_carte) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas

        print(i)     
        print(Longueur_d_onde)
        print(Tension_CARTE_NI)
        print(len(Longueur_d_onde))
        print(len(Tension_CARTE_NI))

    Tension_CARTE_NI.reverse() # On retourne car on commence à 800nm (le rouge) et on termine dans UV 
    return  Longueur_d_onde, Tension_CARTE_NI, pas_de_vis




"""
PARTIE ACQUISITION DES DONNEES
""" 

# Fonction pour écrire les données dans un fichier CSV
def sauvegarder_donnees(nom_fichier, Liste_longueurs_d_onde, Liste_tensions, Liste_pas_vis, titre_1, titre_2, titre_3): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2,titre_3])
        for i in range(len(Liste_longueurs_d_onde)):
            writer.writerow([Liste_longueurs_d_onde[i], Liste_tensions[i], Liste_pas_vis[i]])



def solution(course_vis, nombre_de_mesure, vitesse_translation, fichier_echantillon, nom_colonne_tension): # Départ 7.25mm / 21 - 7.25 = 13.75mm où 21 course de la vis total de la vis => course_vis=13.75mm
    [Longueur_d_onde, Tension_echantillon, pas_de_vis] = mode_precision(course_vis, nombre_de_mesure, vitesse_translation)
    sauvegarder_donnees(fichier_echantillon, Longueur_d_onde, Tension_echantillon, pas_de_vis, 'Longueur d\'onde (nm)', nom_colonne_tension,'Liste_pas_vis')
    s=str(etat_mot())
    while 'Idle' not in s: # 'Idle': Instruction GRBL pour dire ce que moteur est à l'arrêt / 'Run' le moteur tourne
        s=str(etat_mot())

    print(s)

    param_mot()
    retour_vis(course_vis)
    param_mot()


def maximum(liste):
    maxi = liste[0]
    p=0
    for i in range(len(liste)):
        if liste[i] > maxi:
            p = i
            maxi=liste[i]

    return p



"""
AFFICHAGE DES DONNEES
"""

def graph(fichier_blanc, fichier_echantillon, Nom_echantillon): # fichier_blanc, fichier_echantillon: (str) Chemin d'acces des fichier creer pour l'expérience 
    data_1 = pd.read_csv(fichier_blanc,  encoding='ISO-8859-1')
    data_2= pd.read_csv(fichier_echantillon,  encoding='ISO-8859-1')

# Obtenir les colonnes 'Longueur d\'onde' et Tension Blanc et Tension echantillon
    Longueur_donde = data_1['Longueur d\'onde (nm)']
    Tension_blanc = data_1['Tension blanc (Volt)']
    Tension_echantillon= data_2['Tension échantillon (Volt)']
    Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))
    Pic_d_absorbance=max(Absorbance)
    Pic_longueur_donde=Longueur_donde[maximum((Absorbance))]

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
    plt.show()


"""
ACQUISITION
"""

def acquisition(course_vis, nombre_de_mesures, vitesse_translation_vis, fichier_blanc, fichier_echantillon, Nom_echantillon): 
    mode=input("Choisir le mode d'acquisition (noir) / (blanc) / (echantillon) :")
    if mode=='blanc':
        solution(course_vis, nombre_de_mesures, vitesse_translation_vis, fichier_blanc, 'Tension blanc (Volt)') 
    
    elif mode=='echantillon':
        solution(course_vis, nombre_de_mesures, vitesse_translation_vis, fichier_echantillon, 'Tension échantillon (Volt)')
        time.sleep(0.5) # Voir si c'est nécessaire 
        graph(fichier_blanc, fichier_echantillon, Nom_echantillon)
    
    else:
        print("Sélectionner le mode (blanc), (echantillon), (noir)")




course_vis=10 # 7mm
nombre_de_mesures=200 # A modifier si on veut être plus précis
vitesse_translation_vis=4 # 4mm/min

Date='10_05_2023' # A modifier à chaque jour de projet
Chemin_acces='Manip\Manip_' + Date
Taille_de_fente='\Fente_0_2mm' # A modifier si on change de fente

fichier_bruit_de_noir= Chemin_acces + Taille_de_fente + '\Tension_de_noir_' + Date + '.csv'
fichier_blanc=  Chemin_acces + Taille_de_fente + '\Tension_de_blanc_' + Date + '.csv'
fichier_echantillon=  Chemin_acces + Taille_de_fente + '\Tension_de_echantillon_' + Date + '.csv'


utilisateur = "admin"
projet = "Projet_GP"
programmation = "Programmation_Spectro/Programmation_application_spectro"
date = "Manip_11_05_2023"
fente = "Fente_0_2mm"

# Concaténer les variables pour former le chemin d'accès complet
chemin = os.path.join("C:/Users", utilisateur, "Documents", projet, programmation, date, fente)

# Créer le répertoire en utilisant le chemin d'accès
os.makedirs(chemin)

Nom_echantillon='bleu de bromophenol' # A modifier si on change de composé chimique

acquisition(course_vis, nombre_de_mesures, vitesse_translation_vis, fichier_blanc, fichier_echantillon, Nom_echantillon) # course_vis 13.75 mm / 260 points / vitesse_translation_vis = 4mm/min


