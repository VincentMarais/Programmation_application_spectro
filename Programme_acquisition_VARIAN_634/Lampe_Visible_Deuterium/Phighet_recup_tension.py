from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *

import matplotlib.pyplot as plt
import numpy as np
import sys
import time


"""
Explication: Recup_tension_temps

Entrée: Temps_d_acquisition (réel): temps d'acquisition de la tension par le Phidget

Sortie: 
	- Temps(liste): Liste qui contient les instant d'acquisition  
	- Tension_Phidget_echantillon: Liste qui contient les tensions à chaque instant
"""

def Recup_tension_temps(Temps_d_acquisition):  # Fonction choisi pour l'app 
    
	Tension_Phidget_echantillon= []
	Temps=[]
    
	voltageInput0 = VoltageInput() 
	voltageInput0.setHubPort(1) 
	voltageInput0.setDeviceSerialNumber(626587)
	voltageInput0.openWaitForAttachment(5000)

	start_time = time.time() # Temps initial machine depuis 1er Janvier 1970 en second 
	while (time.time() - start_time) < Temps_d_acquisition+1: # Tant la durée de simulation n'a pas duré 10s on applique la boucle
		print(time.time() - start_time)
		Temps.append(time.time() - start_time)
		voltageInput0.openWaitForAttachment(5000)
		Tension_Phidget_echantillon.append(voltageInput0.MinVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
		print(Tension_Phidget_echantillon)
		print(len(Tension_Phidget_echantillon))  
		voltageInput0.close() 
	return Temps, Tension_Phidget_echantillon




Recup_tension_temps(10)	# 10 second d'acquisition
plt.plot(Recup_tension_temps[0],Recup_tension_temps[1])
plt.xlabel('Temps (second)')
plt.ylabel('Tension (Volt)')
plt.show()



#Temps_d_acquisition=10
#main_1(Temps_d_acquisition)








