from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # A dev 
"""
Ce code est écrit en Python et utilise la bibliothèque "Phidget22" pour interfacer avec un dispositif d'entrée de tension Phidget. 
Le code définit deux fonctions: Recup_voltage et main.

"""
L=[]
def Recup_voltage(self, voltage):  # Méthode qui stocke la tension du Phidget dans la liste L	
	L.append(voltage)
	print(L)

"""
La fonction Recup_voltage prend deux arguments: self et tension. 

Il ajoute la valeur de tension à une liste L et imprime le contenu actuel de L.
"""
def main(n): # Méthode principal qui fait fonctionner le phidget
	
	voltageInput0 = VoltageInput() # VoltageInput est une classe qui 
	
	voltageInput0.setHubPort(0) 
		
	voltageInput0.setDeviceSerialNumber(626587)

	for k in range (0,n):		

		voltageInput0.setOnVoltageChangeHandler(Recup_voltage)

		voltageInput0.openWaitForAttachment(5000) # Méthode: OpenWaitForAttachment (n): ouvre une 
													#connexion au dispositif d'entrée de tension Phidget et 
													# attend n millisecond qu'il soit attaché

		voltageInput0.close() # On appelle la méthode close qui ferme le programme		
	
	
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
	

main(4)



