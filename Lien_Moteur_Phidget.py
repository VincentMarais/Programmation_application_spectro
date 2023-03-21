import tkinter
import serial  
import tkinter.messagebox
import customtkinter
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np

# Variables
s = serial.Serial('COM5', 115200)
Tension_Phidget_blanc= []


s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(2)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.



def deplacement(pas): # Fonction qui pilote le moteur
        gcode_1= 'G0 X' + str(pas) + '\n'
        s.write(gcode_1.encode())
     
    
def etalonnage(d): # d: Distance que la vis doit parcourir en (mm)
    Longueur_d_onde=[]
    i=0
    pas=0.5 # 0.5mm Pas de la vis (cf Exel)
    
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
	
    while i < d: # Tant la durée de simulation n'a pas duré 10s on applique la boucle
        voltageInput0.openWaitForAttachment(5000)
        Tension_Phidget_blanc.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        Longueur_d_onde.append(19.23*i +400) # Je suppose que l'on part à 400nm -> 0mm et que l'on fini à 800 nm --> 20.8mm => 19.23= coefficient directeur de la droite lambda = a*x + 400 nm où x position de la vis
        print(Longueur_d_onde)
        print(Tension_Phidget_blanc)
        deplacement(i+pas)
        time.sleep(7.49) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas

        print(i)

        

        print(Longueur_d_onde)
        print(Tension_Phidget_blanc)
        print(len(Tension_Phidget_blanc))
        voltageInput0.close()
    deplacement(-d)
    return Longueur_d_onde



def mode_precision(n):  # n: distance parcouru par la vis en mm/ Ici on mesure la tension au borne du phidget à chaque pas
    Tension_Phidget_echantillon= []
    Longueur_d_onde=[]
    i=0
    pas=0.5 # 0.5mm Pas de la vis (cf Exel)
    
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
	
    while i < n: # Tant la durée de simulation n'a pas duré 10s on applique la boucle
        voltageInput0.openWaitForAttachment(5000)
        Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        Longueur_d_onde.append(19.23*i +400) # Je suppose que l'on part à 400nm -> 0mm et que l'on fini à 800 nm --> 20.8mm => 19.23= coefficient directeur de la droite lambda = a*x + 400 nm où x position de la vis
        print(Longueur_d_onde)
        print(Tension_Phidget_echantillon)
        deplacement(i+pas)
        time.sleep(7.49) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas

        print(i)

        

        print(Longueur_d_onde)
        print(Tension_Phidget_echantillon)
        print(len(Tension_Phidget_echantillon))
        voltageInput0.close()
    deplacement(-i)
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
    return  Longueur_d_onde, Tension_Phidget_echantillon



def graph_absorbance():
    [x,y]=mode_rapide(20,4)
    y=np.log10(y/Tension_Phidget_blanc) # Définition de l'absorbance
    plt.plot(x,y)
    plt.xlabel("Longueur d'onde (nm) ")
    plt.ylabel('Absorbance')
    plt.title("Absorbance de la solution")
    plt.show()

def graph_blanc():
    [x,Tension_Phidget_blanc]= mode_rapide(20,4)
     # Définition de l'absorbance
    plt.plot(x,Tension_Phidget_blanc)
    plt.xlabel("Longueur d'onde (nm) ")
    plt.ylabel('Tension Blanc (Volt)')
    plt.title("Absorbance de la solution")
    plt.show()

graph_blanc()

