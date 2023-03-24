import serial  
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

"""
INITIALISATION DE L'ARDUINO

"""
# Variables
s = serial.Serial('COM5', 115200)


s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(2)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.

"""
DEPLACEMENT DU MOTEUR

"""

def maximum(liste):
    maxi = liste[0]
    p=0
    for i in range(len(liste)):
        if liste[i] > maxi:
            p = i
            maxi=liste[i]

    return p

def etat_mot():
    g_code='?' + '\n'
    s.write(g_code.encode())

    return s.read(10)

def param_mot():
    
    g_code='$G' + '\n'
    s.write(g_code.encode())
    print(s.read(75))
    

def deplacement(pas): # Fonction qui pilote le moteur      
        gcode_1= 'G0X' + str(pas) + '\n'
        s.write(gcode_1.encode())
        


def retour(pas):
        g_code= '$110=10'+ '\n'
        s.write(g_code.encode())
        time.sleep(0.5)
        g_code= 'G91'+ '\n'
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X-' + str(pas) + '\n'
        s.write(gcode_1.encode())



"""
LIEN ENTRE LE MOTEUR ET LE PHIDGET
"""
    



def mode_precision(d, n, vitesse):  # d: distance parcouru par la vis en mm/ n: nombre mesure de tension / vitesse: vitesse translation de la vis (mm/min)
    Tension_Phidget_echantillon= []
    Longueur_d_onde=[]
    i=0
    pas=d/n # 0.5mm Pas de la vis (cf Exel)
    
    t= (pas*60)/vitesse # Temps pour faire un pas 
    g_code= '$110=' + str(vitesse) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
	
    while i < d: # 
        voltageInput0.openWaitForAttachment(5000)
        Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        Longueur_d_onde.append(19.23*i +400) # Je suppose que l'on part à 400nm -> 0mm et que l'on fini à 800 nm --> 20.8mm => 19.23= coefficient directeur de la droite lambda = a*x + 400 nm où x position de la vis
        print(Longueur_d_onde)
        print(Tension_Phidget_echantillon)
        deplacement(i+pas) # A comprendre car non logique
        time.sleep(t) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas

        print(i)        

        print(Longueur_d_onde)
        print(Tension_Phidget_echantillon)
        print(len(Longueur_d_onde))
        print(len(Tension_Phidget_echantillon))

        voltageInput0.close()
    Tension_Phidget_echantillon.reverse()
    return  Longueur_d_onde, Tension_Phidget_echantillon



def mode_rapide(d,vitesse):  # d: distance parcouru par la vis / vitesse: vitesse du moteur en (mm/min) / Ici on mesure la tension en continue
    Tension_Phidget_echantillon= []
    Longueur_d_onde=[] 
    
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
	
    deplacement(d)
    start_time = time.time() # Le temps début lorque le moteur démarre /	# Temps initial machine depuis 1er Janvier 1970 en second 


    while (time.time() - start_time) < (d*60)/vitesse: # d*60/vitesse = temps en second afin que la vis soit à la distance d
        voltageInput0.openWaitForAttachment(5000)
        Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        Longueur_d_onde.append(19.23*((time.time() - start_time)*vitesse)/60 +400) # cf mode précis pour comprendre
        print(Tension_Phidget_echantillon)
        print(len(Tension_Phidget_echantillon))  
        print(Longueur_d_onde)
        voltageInput0.close() 
    #Tension_Phidget_echantillon=reversed(Tension_Phidget_echantillon)
    return  Longueur_d_onde, Tension_Phidget_echantillon


def acquisition_n_valeurs(d,vitesse): # d: distance à parcourir par la vis / vitesse de déplacement de la vis
    t= (d*60)/vitesse
    n=t/0.25 # n nombre de valeurs a prendre
    print(n)
    Tension_Phidget=[]
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
    deplacement(d)
    for i in range(1,int(n)):
        voltageInput0.openWaitForAttachment(5000)
        Tension_Phidget.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        time.sleep(0.25)
        print(Tension_Phidget)
        voltageInput0.close() 
    
    time.sleep(0.5)
    retour(d)
    return Tension_Phidget.reverse()



"""
PARTIE ACQUISITION DES DONNEES

""" 







# Fonction pour écrire les données dans un fichier CSV
def sauvegarder_donnees(nom_fichier, longueurs_d_onde, tensions, titre_1, titre_2):
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2])
        for i in range(len(longueurs_d_onde)):
            writer.writerow([longueurs_d_onde[i], tensions[i]])


def solution_blanc(d, n, vitesse, nom_du_fichier_blanc):
    [Longueur_donde,Tension_blanc] = mode_precision(d,n,vitesse)
    sauvegarder_donnees(nom_du_fichier_blanc, Longueur_donde, Tension_blanc, 'Longueur d\'onde (nm)', 'Tension blanc (Volt)')
    s=str(etat_mot())
    while 'Idle' not in s:
        s=str(etat_mot())
    
    param_mot()
    retour(d)
    param_mot()

def solution_echantillon(d, n, vitesse,nom_du_fichier_echantillon): # Départ 7.25mm / 21 - 7.25 = 13.75mm où 21 course de la vis total de la vis => d=13.75mm
    [Longueur_d_onde, Tension_echantillon] = mode_precision(d,n, vitesse)
    sauvegarder_donnees(nom_du_fichier_echantillon, Longueur_d_onde, Tension_echantillon, 'Longueur d\'onde (nm)', 'Tension échantillon (Volt)')
    s=str(etat_mot())
    while 'Idle' not in s:
        s=str(etat_mot())

    print(s)

    param_mot()
    retour(d)
    param_mot()

"""
AFFICHAGE DES DONNEES
"""


def graph(nom_du_fichier_blanc, nom_du_fichier_echantillon, nom_echantillon):
    data_1 = pd.read_csv(nom_du_fichier_blanc,  encoding='ISO-8859-1')
    data_2= pd.read_csv(nom_du_fichier_echantillon,  encoding='ISO-8859-1')

# Obtenir les colonnes 'Longueur d\'onde' et Tension Blanc et Tension echantillon
    Longueur_donde = data_1['Longueur d\'onde (nm)']
    Tension_blanc = data_1['Tension blanc (Volt)']
    Tension_echantillon= data_2['Tension échantillon (Volt)']
    Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))
# Longueur d'onde d'absorbance
    print( "Longueur d'onde d'absorbance : ", Longueur_donde[maximum(Absorbance)])
# Tracer le graphe
    plt.plot(Longueur_donde, Absorbance)
    plt.xlabel('Longueur d\'onde (nm)')
    plt.ylabel('Absorbance ')
    plt.title('Absorbance du' + nom_echantillon)
    plt.show()  


"""
UTILITAIRE

"""

def acquisition(d, n, vitesse, nom_du_fichier_blanc, nom_du_fichier_echantillon, nom_echantillon): 
    mode=int(input("Choisir l'acquisition:"))
    if mode==0:
        solution_blanc(d, n, vitesse, nom_du_fichier_blanc) 
    elif mode==1:
        solution_echantillon(d, n, vitesse, nom_du_fichier_echantillon)
        time.sleep(0.5)
        graph(nom_du_fichier_blanc, nom_du_fichier_echantillon, nom_echantillon)
        print("Longueur d'onde d'absorbance : " )
    else:
        print("Sélectionner le mode 0 ou 1")

#mode_precision(0.75,4)

acquisition(14,200,4,'solution_blanc.csv','solution_echantillon1.csv', ' bromophenol') # Distance 13.75 mm / 260 points / vitesse = 4mm/min


#param_mot()