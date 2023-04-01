from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np


def main_1(Temps_d_acquisition):  # Fonction choisi pour l'app 
	Tension_Phidget_echantillon= []

	Temps=[]

	voltageInput0 = VoltageInput()
    
	voltageInput0.setHubPort(0) 
	
	voltageInput0.setDeviceSerialNumber(626587)
	
	start_time = time.time() # Temps initial machine depuis 1er Janvier 1970 en second 
	while (time.time() - start_time) < Temps_d_acquisition+1: # Tant la durée de simulation n'a pas duré 10s on applique la boucle
		print(time.time() - start_time)
		Temps.append(time.time() - start_time)
		voltageInput0.openWaitForAttachment(5000)
		Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
		print(Tension_Phidget_echantillon)
		print(len(Tension_Phidget_echantillon))  
		voltageInput0.close() 
	return Temps, Tension_Phidget_echantillon
	


def Data_Interval():
	ch = VoltageInput()

	ch.setHubPort(0) 
		
	ch.setDeviceSerialNumber(626587)
	ch.openWaitForAttachment(1000)

	dataInterval = ch.getDataInterval()
	print("DataInterval: " + str(dataInterval))
	
	ch.close()


Temps_d_acquisition=10
main_1(Temps_d_acquisition)

"""
La fonction main prend un argument Temps_d_acquisition et effectue les étapes suivantes:

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






