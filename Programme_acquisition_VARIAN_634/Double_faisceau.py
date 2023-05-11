import serial  
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np
import csv # Déjà dans python
import pandas as pd
import re

 
"""
INITIALISATION DE L'ARDUINO + PHIDGET
"""
# Constantes
COM_PORT = 'COM5'
BAUD_RATE = 115200
PHIDGET_0_HUB_PORT = 0
PHIDGET_1_HUB_PORT = 1
PHIDGET_SERIAL_NUMBER = 626587
INITIALIZATION_TIME = 2
TEMPS_ATTENTE_PHIDGET=5000


# Initialisation arduino
s = serial.Serial(COM_PORT, BAUD_RATE)
s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(INITIALIZATION_TIME)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.



# Initialisation Phidget
def detection_Phidget():
    voltage_input = VoltageInput()
    voltage_input.setHubPort(PHIDGET_0_HUB_PORT)
    voltage_input.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)
    voltage_input.openWaitForAttachment(5000)


def lire_tension_phidget():
    voltage_input = VoltageInput()
    voltage_input.setHubPort(PHIDGET_0_HUB_PORT)
    voltage_input.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)
    voltage_input.openWaitForAttachment(5000)

    tension = voltage_input.getVoltage()

    voltage_input.close()

    return tension



"""
Caractérisation DU MOTEUR
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



def deplacer_moteur_vis(course_vis): # Fonction qui pilote le moteur      
        gcode_1= 'G0X' + str(course_vis) + '\n'
        s.write(gcode_1.encode())

def deplacer_moteur_miroir(course_miroir): # Fonction qui pilote le moteur      
        gcode_1= 'G0Y' + str(course_miroir) + '\n'
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
LIEN ENTRE LE MOTEUR ET LE PHIDGET
"""
    
"""

Fonction mode_precision

Entrée:  
- distance: distance parcouru par la vis en mm/  
- nombre_de_mesures: nombre de mesure de tension / 
- vitesse_translation: vitesse translation de la vis (mm/min)

Sortie:


"""
def mode_precision(course_vis, nombre_de_mesures):  # d: distance parcouru par la vis en mm/  n: nombre de mesure de tension / vitesse_translation_vis: vitesse_translation_vis translation de la vis (mm/min)
    Tension_Phidget_blanc= []
    Tension_Phidget_echantillon= []
    Longueur_d_onde=[]
    pas_de_vis=[]
    i=0
    
    pas=course_vis/nombre_de_mesures # 0.5mm Pas de la vis (cf Exel)
    t= (pas*60)/4 # Temps pour faire un pas 
    
    g_code= '$110=' + str(4) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)
    
    ch0 = VoltageInput()
    ch0.setHubPort(PHIDGET_0_HUB_PORT) 
    ch0.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)

    ch1 = VoltageInput()
    ch1.setHubPort(PHIDGET_1_HUB_PORT) 
    ch1.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)
	
    while i < course_vis: # Tant que la vis n'a pas parcouru une distance course_vis
        
        ch0.openWaitForAttachment(TEMPS_ATTENTE_PHIDGET)
        Tension_Phidget_echantillon.append(ch0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        print(Tension_Phidget_echantillon)
        deplacer_moteur_miroir(0.33334) # Le moteur doit faire une angle de 60° 
        ch0.close() # Voir si je mets le close à la fin du while

        ch1.openWaitForAttachment(TEMPS_ATTENTE_PHIDGET)
        Tension_Phidget_blanc.append(ch1.getVoltage())
        print(Tension_Phidget_blanc)
        deplacer_moteur_miroir(-0.33334)
        ch1.close()

        pas_de_vis.append(i)
        Longueur_d_onde.append(31.10419907*i +400) # Je suppose que l'on part à 400nm -> 0mm et que l'on fini à 800 nm --> 20.8mm => 19.23= coefficient directeur de la droite lambda = a*x + 400 nm où x position de la vis
        
        deplacer_moteur_vis(i+pas) # Le moteur travail en mode absolue par défaut G90 
        time.sleep(t) # A voir si je le laisse
        i+=pas

        print(i)     
        print(Longueur_d_onde)

    Tension_Phidget_echantillon.reverse() # On retourne car on commence à 800nm (le rouge) et on termine dans UV 
    return  Longueur_d_onde, pas_de_vis, Tension_Phidget_blanc, Tension_Phidget_echantillon




"""
La lettre b devant une chaîne de caractères (string) signifie qu'il s'agit d'une chaîne de caractères de type bytes, 
c'est-à-dire une séquence d'octets en Python. Dans ce cas, la fonction etat_mot() 
renvoie une chaîne de caractères encodée en bytes, donc pour comparer cette chaîne avec la chaîne de caractères "Idle\n", 
il faut la convertir également en une chaîne de caractères encodée en bytes.
"""




"""
PARTIE ACQUISITION DES DONNEES
""" 

# Fonction pour écrire les données dans un fichier CSV
def sauvegarder_donnees(nom_fichier, Liste_longueurs_d_onde, Liste_pas_vis, Liste_tensions_blanc, Liste_tensions_echantillon, titre_1, titre_2, titre_3, titre_4): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2, titre_3, titre_4])
        for i in range(len(Liste_longueurs_d_onde)):
            writer.writerow([Liste_longueurs_d_onde[i], Liste_pas_vis[i], Liste_tensions_blanc[i], Liste_tensions_echantillon[i]])



def solution(course_vis, nombre_de_mesure, vitesse_translation, fichier_echantillon, nom_colonne_tension_blanc, nom_colonne_tension_echantillon ): # Départ 7.25mm / 21 - 7.25 = 13.75mm où 21 course de la vis total de la vis => course_vis=13.75mm
    [Longueur_d_onde, pas_de_vis, Tension_blanc, Tension_echantillon] = mode_precision(course_vis, nombre_de_mesure, vitesse_translation)
    sauvegarder_donnees(fichier_echantillon, Longueur_d_onde, pas_de_vis, Tension_blanc, Tension_echantillon, 'Longueur d\'onde (nm)', 'pas de vis (mm)', nom_colonne_tension_blanc, nom_colonne_tension_echantillon)
    s=str(etat_mot())
    while 'Idle' not in s: # 'Idle': Instruction GRBL pour dire ce que moteur est à l'arrêt / 'Run' le moteur tourne
        s=str(etat_mot())

    print(s)

    param_mot()
    retour_vis(course_vis)
    param_mot()


# Fonction pour acquérir le bruit de noir et retourne la 
def acquisition_bruit_noir(PHIDGET_HUB_PORT,nom_fichier_bruit_noir, nombre_de_mesure):
    Tension_de_noir=[]
    
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(PHIDGET_HUB_PORT) 
	
    voltageInput0.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)

    while len(Tension_de_noir)< nombre_de_mesure:
        voltageInput0.openWaitForAttachment(TEMPS_ATTENTE_PHIDGET)
        Tension_de_noir.append(voltageInput0.getVoltage())
        print(Tension_de_noir)
    
    with open(nom_fichier_bruit_noir, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(['Tension de noir (Volt)'])
        for i in range(len(Tension_de_noir)):
            writer.writerow([Tension_de_noir[i]])



"""
ANALYSE DES DONNEES

"""
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
    data = pd.read_csv(fichier_blanc,  encoding='ISO-8859-1')

# Obtenir les colonnes 'Longueur d\'onde' et Tension Blanc et Tension echantillon
    Longueur_donde = data['Longueur d\'onde (nm)']
    Tension_blanc = data['Tension blanc (Volt)']
    Tension_echantillon= data['Tension échantillon (Volt)']
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

def acquisition(course_vis, nombre_de_mesures, vitesse_translation_vis, PHIDGET_HUB_PORT, fichier_bruit_de_noir, fichier_blanc, fichier_echantillon, Nom_echantillon): 
    mode=input("Choisir le mode d'acquisition (noir) / (acquisition) :")
    if mode=='noir':
        acquisition_bruit_noir(PHIDGET_HUB_PORT,fichier_bruit_de_noir,nombre_de_mesures)
    
    elif mode=='acquisition':
        solution(course_vis, nombre_de_mesures, vitesse_translation_vis, fichier_echantillon, 'Tension blanc (Volt)', 'Tension échantillon (Volt)')
        time.sleep(0.5) # Voir si c'est nécessaire 
        graph(fichier_blanc, fichier_echantillon, Nom_echantillon)
    
    else:
        print("Sélectionner le mode (noir) / (acquisition)")


course_vis=2 # 7mm
nombre_de_mesures=5 # A modifier si on veut être plus précis
vitesse_translation_vis=4 # 4mm/min

Date='31_03_2023' # A modifier à chaque jour de projet
Chemin_acces='Manip\Manip_' + Date
Taille_de_fente='\Fente_1mm' # A modifier si on change de fente

fichier_bruit_de_noir= Chemin_acces + Taille_de_fente + '\Tension_de_noir_' + Date + '.csv'
fichier_blanc=  Chemin_acces + Taille_de_fente + '\Tension_de_blanc_' + Date + '.csv'
fichier_echantillon=  Chemin_acces + Taille_de_fente + '\Tension_de_echantillon_' + Date + '.csv'

Nom_echantillon='bleu de bromophenol' # A modifier si on change de composé chimique

#acquisition(course_vis, nombre_de_mesures, vitesse_translation_vis, PHIDGET_0_HUB_PORT, fichier_bruit_de_noir, fichier_blanc, fichier_echantillon, Nom_echantillon) # course_vis 13.75 mm / 260 points / vitesse_translation_vis = 4mm/min
mode_precision(course_vis, nombre_de_mesures)

