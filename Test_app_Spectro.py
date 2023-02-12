# Bibliothèque
import tkinter
import tkinter.messagebox
import customtkinter
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


Tension_Phidget= []

def Recup_voltage(self, voltage):  # Méthode qui stocke la tension du Phidget dans la liste L	
	
    Tension_Phidget.append(voltage)
    print(Tension_Phidget)



"""
# La fonction Recup_voltage prend deux arguments: self et tension. 

#Il ajoute la valeur de tension à une liste L et imprime le contenu actuel de L.
"""
def main(n): # Méthode principal qui fait fonctionner le phidget
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
	

class App(customtkinter.CTk): # Cf Formation
    def __init__(self):
        super().__init__()



        # configure window
        self.title("Application Varian 643")
        self.geometry(f"{1100}x{580}") #Taille de la page

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Spectro", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Acquisition" , command=self.Acquisition)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Graphique" , command=self.graph)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)




        

        # Tabview 
        self.tabview = customtkinter.CTkTabview(self, width=650)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Balayage")
        self.tabview.add("Suivi Cinétique")
        self.tabview.add("Tab 3")
        self.tabview.tab("Balayage").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Suivi Cinétique").grid_columnconfigure(0, weight=1)

    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
   
    def graph(self):
        x = np.linspace(400, 800, 9) # 100=nombre d'échantillon
        y =  Tension_Phidget
        plt.plot(x, y)
        plt.xlabel("Longueur d'onde (nm) ")
        plt.ylabel('Tension du Phidget')
        plt.title("Tension du phidghet en fonction de la longueur d'onde")
        plt.show()

    def Acquisition(self):
        main(n=9)


if __name__ == "__main__":
    app = App()
    app.mainloop()





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
class Moteur:
    """
    Classe Moteur : permet de controler le moteur (subclass de App)
    
    """
    def __init__(self) -> None:
         pass

	

