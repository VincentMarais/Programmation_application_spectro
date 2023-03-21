import tkinter
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


def main_1(n):  # Fonction choisi pour l'app 
	Tension_Phidget_echantillon= []

	Temps=[]

	voltageInput0 = VoltageInput()
    
	voltageInput0.setHubPort(0) 
	
	voltageInput0.setDeviceSerialNumber(626587)
	
	start_time = time.time() # Temps initial machine depuis 1er Janvier 1970 en second 
	while (time.time() - start_time) < n+1: # Tant la durée de simulation n'a pas duré 10s on applique la boucle
		print(time.time() - start_time)
		Temps.append(time.time() - start_time)
		voltageInput0.openWaitForAttachment(5000)
		Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
		print(Tension_Phidget_echantillon)
		print(len(Tension_Phidget_echantillon))  
		voltageInput0.close() 
	return Temps, Tension_Phidget_echantillon
	

def main_2(n): # 
	k= 0 
	voltageInput0 = VoltageInput() # VoltageInput est une classe qui la tension d'entrée du Phidget 
	
	voltageInput0.setHubPort(0) 
		
	voltageInput0.setDeviceSerialNumber(626587)

	voltageInput0.setOnVoltageChangeHandler(Recup_voltage)

	voltageInput0.openWaitForAttachment(5000) # Méthode: OpenWaitForAttachment (n): ouvre une 
													#connexion au dispositif d'entrée de tension Phidget et 
													# attend n millisecond qu'il soit attaché
	while k < n: 	
		print(len(Tension_Phidget))
		time.sleep(0.25) # Intervalle de temps entre 2 valeurs du Phidget  (cf docs Phidget: https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python)
		k+=1
	voltageInput0.close() # On appelle la méthode close qui ferme le programme	


def main_3(n): # Méthode principal qui fait fonctionner le phidget
	k= 0 
	voltageInput0 = VoltageInput() # VoltageInput est une classe qui 
	
	voltageInput0.setHubPort(0) 
		
	voltageInput0.setDeviceSerialNumber(626587)

	while k < n: 	

		voltageInput0.setOnVoltageChangeHandler(Recup_voltage)
		time.sleep(1)
		k+=1
		voltageInput0.openWaitForAttachment(5000) # Méthode: OpenWaitForAttachment (n): ouvre une 
													#connexion au dispositif d'entrée de tension Phidget et 
													# attend n millisecond qu'il soit attaché

		voltageInput0.close() # On appelle la méthode close qui ferme le programme		

def main_4():
	ch = VoltageInput()

	ch.setHubPort(0) 
		
	ch.setDeviceSerialNumber(626587)
	ch.openWaitForAttachment(1000)

	dataInterval = ch.getDataInterval()
	print("DataInterval: " + str(dataInterval))
	
	ch.close()
main_1(10)



"""
La fonction main prend un argument n et effectue les étapes suivantes:

1) Crée une instance de la classe VoltageInput et l'assigne à la variable voltageInput0.

2) Appelle la méthode setHubPort sur voltageInput0 et définit le port de l'hub à 0.

3) Appelle la méthode setDeviceSerialNumber sur voltageInput0 et définit le numéro de série à 626587.

4) Exécute une boucle for n fois.
	1. Dans chaque itération de la boucle, il appelle la méthode setOnVoltageChangeHandler sur voltageInput0 et définit la fonction 
		de gestionnaire à Recup_voltage.

	2. Appelle la méthode openWaitForAttachment sur voltageInput0 avec un argument de 5000 millisecondes (5 secondes), 
	   ce qui ouvre une connexion au dispositif d'entrée de tension Phidget et attend qu'il soit attaché.

	3. Appelle la méthode close sur voltageInput0, qui ferme la connexion au dispositif d'entrée de tension Phidget.

"""
def graph(n):
	x = np.linspace(0, n, n) # 100=nombre d'échantillon
	y =  np.sin(x)
	plt.plot(x, y)
	plt.xlabel("Longueur d'onde (nm) ")
	plt.ylabel('Tension du Phidget')
	plt.title("Tension du phidghet en fonction de la longueur d'onde")
	plt.show()





