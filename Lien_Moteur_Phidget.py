import tkinter
import serial  
import tkinter.messagebox
import customtkinter
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np
"""
Ce code est écrit en Python et utilise la bibliothèque "Phidget22" pour interfacer avec un dispositif d'entrée de tension Phidget. 
Le code définit deux fonctions: Recup_voltage et main.

Problèmes
"""
# Variables
Tension_Phidget=[]
def creation_Liste():
	L= []
	return L


# Class Phidget
def Recup_voltage(self, voltage):  # Méthode qui stocke la tension du Phidget dans la liste L	
	Tension_Phidget.append(voltage)
	#print(Tension_Phidget)
	
"""
La fonction Recup_voltage prend deux arguments: self et tension. 

Il ajoute la valeur de tension à une liste L et imprime le contenu actuel de L.
"""
s = serial.Serial('COM5', 115200)

s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(2)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.



def deplacement(pas): # Fonction qui pilote le moteur
        gcode_1= 'G0 X' + str(pas) + '\n'
        s.write(gcode_1.encode())
     
    

def main_1(n):  # Fonction choisi pour l'app 
    Tension_Phidget_echantillon= []
    i=0
    pas=0.5 # 0.5mm Pas de la vis (cf Exel)

    Longeur_d_onde=[]
    
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
	
	# Temps initial machine depuis 1er Janvier 1970 en second 
    while i < n: # Tant la durée de simulation n'a pas duré 10s on applique la boucle
        voltageInput0.openWaitForAttachment(1000)
        Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        time.sleep(0.25) # 250ms entre valeur de tension du phidget (cf doc phigdet 20bits)
        Tension_Phidget_echantillon.append(voltageInput0.getVoltage())
        Longeur_d_onde.append(20*i +400) # Je suppose que l'on part à 400nm 
        deplacement(i+pas)
        time.sleep(7.49) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas

        

        print(Longeur_d_onde)
        print(Tension_Phidget_echantillon)
        print(len(Tension_Phidget_echantillon))
        print(Longeur_d_onde)  
        voltageInput0.close() 
    return  Tension_Phidget_echantillon

main_1(n=2)