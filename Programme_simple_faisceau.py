import serial  
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import re

"""

INITIALISATION DE L'ARDUINO

"""

# Constantes:

COM_PORT = 'COM5'
BAUD_RATE = 115200
PHIDGET_HUB_PORT = 0
PHIDGET_SERIAL_NUMBER = 626587
INITIALIZATION_TIME = 2

connection = serial.Serial(COM_PORT, BAUD_RATE, timeout=1)
    
connection.write("\r\n\r\n".encode())
time.sleep(INITIALIZATION_TIME)
connection.reset_input_buffer()


"""
Caractérisation DU MOTEUR

"""

def etat_mot():
    g_code='?' + '\n'
    connection.write(g_code.encode())
    return str(connection.readline()) # 10: On lit 10 caractère dans le serial

def param_mot():    
    g_code='$G' + '\n'
    connection.write(g_code.encode())
    print(connection.read(75))



def position_moteur_x():
    # Demande la position actuelle du moteur selon l'axe X
    connection.write(b"?x\n")
    reponse = connection.readline().decode().strip()
    position_x = reponse.split(":")[1]
    return int(position_x)

def modif_vitesse_translation(vitesse_translation):
    g_code = '$110=' + str(vitesse_translation) + '\n'
    connection.write(g_code.encode())
    time.sleep(0.5)

def deplacer_moteur(pas): # Fonction qui pilote le moteur      
        gcode_1= 'G0X' + str(pas) + '\n'
        connection.write(gcode_1.encode())
        

def retour_moteur(pas,vitesse_translation): 
        modif_vitesse_translation(vitesse_translation)
        g_code= 'G91'+ '\n' # Le moteur ce déplace en relatif
        connection.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X-' + str(pas) + '\n' # Le moteur ce déplace linéairement de -pas (retour_moteur en arrière)
        connection.write(gcode_1.encode())


def position_XYZ():
    g_code= "?" + '\n' 
    connection.write(g_code.encode())
    time.sleep(0.1)

    # Lire et traiter la réponse
    response = str(connection.readline())
    while 'MPos' not in response:
        response = str(connection.readline())
    
        # Extraire les coordonnées X, Y, et Z
    match = re.search(r"MPos:([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+)", response)
        
    x_pos, y_pos, z_pos = [float(coordinate) for coordinate in match.groups()]
    
    return x_pos

"""
PHIDGET

"""


def detection_Phidget():
    voltage_input = VoltageInput()
    voltage_input.setHubPort(PHIDGET_HUB_PORT)
    voltage_input.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)
    voltage_input.openWaitForAttachment(5000)


def lire_tension_phidget():
    voltage_input = VoltageInput()
    voltage_input.setHubPort(PHIDGET_HUB_PORT)
    voltage_input.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)
    voltage_input.openWaitForAttachment(5000)

    tension = voltage_input.getVoltage()

    voltage_input.close()

    return tension



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
def mode_precision(d, n, vitesse,boolean):  # d: distance parcouru par la vis en mm/  n: nombre de mesure de tension / vitesse: vitesse translation de la vis (mm/min)
    Tension_Phidget_echantillon= []
    Longueur_d_onde=[]
    pas=d/n # 0.5mm Pas de la vis (cf Exel)
    i=0

    t= (pas*60)/vitesse # Temps pour faire un pas 
    g_code= '$110=' + str(vitesse) + '\n'
    connection.write(g_code.encode())
    time.sleep(0.5)
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
	
    if boolean == True:    
        while i < d: # Tant que la vis n'a pas parcouru une distance d
            voltageInput0.openWaitForAttachment(5000)            
            Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
            Longueur_d_onde.append(19.23*i +400) # Je suppose que l'on part à 400nm -> 0mm et que l'on fini à 800 nm --> 20.8mm => 19.23= coefficient directeur de la droite lambda = a*x + 400 nm où x position de la vis
            deplacer_moteur(i+pas) # Le moteur travail en mode absolue par défaut G90 
            time.sleep(t) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
            i+=pas
            print(i)        
            print(Longueur_d_onde)
            print(Tension_Phidget_echantillon)
            print(len(Longueur_d_onde))
            print(len(Tension_Phidget_echantillon))

            voltageInput0.close()
        Tension_Phidget_echantillon.reverse() # On retourne car on commence à 800nm (le rouge) et on termine dans UV 
        return  Longueur_d_onde, Tension_Phidget_echantillon

    elif boolean==False:
        g_code= 'G90'+ '\n' # Le moteur ce déplace en absolu
        connection.write(g_code.encode())
        time.sleep(0.5)
        i=d-pas
        while i > 0: # Tant que la vis n'a pas parcouru une distance d
            voltageInput0.openWaitForAttachment(5000)
            Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
            Longueur_d_onde.append(19.23*i +400) # Je suppose que l'on part à 400nm -> 0mm et que l'on fini à 800 nm --> 20.8mm => 19.23= coefficient directeur de la droite lambda = a*x + 400 nm où x position de la vis
            print(position_XYZ())
            print("Pas= ",pas, "i= ",i)
            
            i=i-pas
            deplacer_moteur(i) # Le moteur travail en mode absolue par défaut G90 
            
            time.sleep(1) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
            print(position_XYZ())

        


            print(Longueur_d_onde)
            print(Tension_Phidget_echantillon)
            print(len(Longueur_d_onde))
            print(len(Tension_Phidget_echantillon))
            voltageInput0.close()
        print(position_XYZ())
        return  Longueur_d_onde, Tension_Phidget_echantillon

"""

Fonction mode_rapide

Entrée:  
- distance: distance parcouru par la vis en mm/  
- nombre_de_mesures: nombre de mesure de tension / 
- vitesse_translation: vitesse translation de la vis (mm/min)

Sortie:


"""

def mode_rapide(distance, vitesse_translation):
    distance_vis = []
    tensions_phidget_echantillon = []

    voltage_input = VoltageInput()
    voltage_input.setHubPort(PHIDGET_HUB_PORT)
    voltage_input.setDeviceSerialNumber(PHIDGET_SERIAL_NUMBER)
    voltage_input.openWaitForAttachment(5000)

    modif_vitesse_translation(vitesse_translation)
    deplacer_moteur(distance)


    while True:
        if "Idle\n" in etat_mot(): # La lettre b devant une chaîne de caractères (string) signifie qu'il s'agit d'une chaîne de caractères de type bytes
            break
        voltage_input.openWaitForAttachment(5000)
        distance_vis.append(position_XYZ())
        tensions_phidget_echantillon.append(voltage_input.getVoltage())
        time.sleep(0.25) # 250ms mise à jour de la tension au borne du Phidget (cf Docs Phidget)
        voltage_input.close()

    tensions_phidget_echantillon.reverse()
    return distance_vis, tensions_phidget_echantillon

def graph_2():
    [x,y]=mode_rapide(4,4)
    plt.plot(x,y)


"""

Fonction mode_continu

Entrée:  
- distance: distance parcouru par la vis en mm/  
- nombre_de_mesures: nombre de mesure de tension / 
- vitesse_translation: vitesse translation de la vis (mm/min)

Sortie:


"""
def mode_continu(longueur_donde, duree_mesure, vitesse_translation):
    tensions_phidget_echantillon = []
    temps=[]
    detection_Phidget()
    
    distance = (longueur_donde - 400) / 19.23 
    modif_vitesse_translation(vitesse_translation)
    deplacer_moteur(distance)
    
    while etat_mot() != b"Idle\n":
        time.sleep(0.25)

    start_time=time.time()
    while time.time() - start_time < duree_mesure:
        temps.append(time.time() - start_time)
        tension = lire_tension_phidget()
        tensions_phidget_echantillon.append(tension)
        time.sleep(0.25)
    
    return temps, tensions_phidget_echantillon
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
def sauvegarder_donnees(nom_fichier, longueurs_d_onde, tensions_Phidget, titre_1, titre_2): # nom_Fichier: str / longueurs_d_onde, tensions: Liste / titre_1, titre_2: str
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2])
        for i in range(len(longueurs_d_onde)):
            writer.writerow([longueurs_d_onde[i], tensions_Phidget[i]])


def solution(d, n, vitesse, nom_du_fichier, boolean):
    [Longueur_donde,Tension] = mode_precision(d,n,vitesse,boolean)
    sauvegarder_donnees(nom_du_fichier, Longueur_donde, Tension, 'Longueur d\'onde (nm)', 'Tension blanc (Volt)')
    




"""
Analyse DES DONNEES

"""



def indice_max(liste):
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
def graph(nom_du_fichier_blanc, nom_du_fichier_echantillon, nom_echantillon): # nom_du_fichier_blanc, nom_du_fichier_echantillon: (str) Chemin d'acces des fichier creer pour l'expérience 
    data_1 = pd.read_csv(nom_du_fichier_blanc,  encoding='ISO-8859-1')
    data_2= pd.read_csv(nom_du_fichier_echantillon,  encoding='ISO-8859-1')

# Obtenir les colonnes 'Longueur d\'onde' et Tension Blanc et Tension echantillon
    Longueur_donde = data_1['Longueur d\'onde (nm)']
    Tension_blanc = data_1['Tension blanc (Volt)']
    Tension_echantillon= data_2['Tension échantillon (Volt)']
    Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))
    Max_absorbance=max(Absorbance)
    Longueur_donde_absorbe=Longueur_donde[indice_max((Absorbance))]

# Création du graphique
    plt.plot(Longueur_donde, Absorbance)
    plt.xlabel('Longueur d\'onde (nm)')
    plt.ylabel('Absorbance')
    plt.title('Absorbance du '+ nom_echantillon)

# Mise en évidence du point de pic en rouge
    plt.scatter(Longueur_donde_absorbe, Max_absorbance, color='red')


# Annotation des coordonnées du point
    plt.annotate('({:.2f} nm, {:.2f})'.format(Longueur_donde_absorbe, Max_absorbance),
             xy=(Longueur_donde_absorbe , Max_absorbance),
             xytext=(Longueur_donde_absorbe + 10 , Max_absorbance),
             fontsize=10,
             color='red',
             arrowprops=dict(facecolor='red', arrowstyle='->'))

# Ligne pointillée reliant le point de pic à l'axe des x
    plt.hlines(y=Max_absorbance, xmin=Longueur_donde[0] , xmax=Longueur_donde_absorbe, linestyle='dashed', color='red')

# Ligne pointillée reliant le point de pic à l'axe des y
    plt.vlines(x=Longueur_donde_absorbe, ymin=min(Absorbance), ymax=Max_absorbance, linestyle='dashed', color='red')
# Affichage du graphique
    plt.show()
# Longueur d'onde d'absorbance
 


"""
UTILITAIRE

"""

        
def acquisition(d, n, vitesse, nom_du_fichier_blanc, nom_du_fichier_echantillon, nom_echantillon): 
    
    solution(d, n, vitesse, nom_du_fichier_blanc,True) 
    s=str(etat_mot())
    while "Idle" not in s:
        s=str(etat_mot())

    mode=input("Choisir le retour : (1: retour avec acqui) et (2: retour simple)")

    if mode=='1':
        solution(d, n, vitesse, nom_du_fichier_echantillon,False)
        time.sleep(0.5) # Laiss
        graph(nom_du_fichier_blanc, nom_du_fichier_echantillon, nom_echantillon)
    
    elif mode=='2':
        retour_moteur(d,10)
    else:
        print("Sélectionner le mode 1 ou 2")

#mode_precision(0.75,4)

acquisition(0.5,2,4,'Manip\Manip_28_03_2023\Fente_1mm\solution_blanc_28_03_2023.csv','Manip\Manip_28_03_2023\Fente_1mm\solution_echantillon_28_03_2023.csv', ' bromophenol') # Distance 13.75 mm / 260 points / vitesse = 4mm/min

# Date: 24/03/2023

#mode_rapide(-0.5,4)
#param_mot()