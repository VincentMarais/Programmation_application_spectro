# Bibliothèque
import tkinter
import tkinter.messagebox
import customtkinter
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os
import serial  



# Variables


# Tension_Phidget_echantillon= []



# Classe Phidget
s = serial.Serial('COM5', 115200)

s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(2)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.



def deplacement(pas): # Fonction qui pilote le moteur
        gcode_1= 'G0 X' + str(pas) + '\n'
        s.write(gcode_1.encode())
"""
# La fonction Recup_voltage prend deux arguments: self et tension. 

#Il ajoute la valeur de tension à une liste L et imprime le contenu actuel de L.
"""
def main(n):  
    Tension_Phidget_echantillon= []
    i=0
    pas=0.5 # 0.5mm Pas de la vis (cf Exel)

    Longueur_d_onde=[]
    
    voltageInput0 = VoltageInput()
    
    voltageInput0.setHubPort(0) 
	
    voltageInput0.setDeviceSerialNumber(626587)
	
	# Temps initial machine depuis 1er Janvier 1970 en second 
    while i < n: # Tant la durée de simulation n'a pas duré 10s on applique la boucle
        voltageInput0.openWaitForAttachment(1000)
        Tension_Phidget_echantillon.append(voltageInput0.getVoltage()) # getVoltage() : (Tension la plus récente du channel Phidget) https://www.phidgets.com/?view=api&product_id=VCP1000_0&lang=Python
        time.sleep(0.25) # 250ms entre valeur de tension du phidget (cf doc phigdet 20bits)
        Tension_Phidget_echantillon.append(voltageInput0.getVoltage())
        Longueur_d_onde.append(20*i +400) # Je suppose que l'on part à 400nm 
        deplacement(i+pas)
        time.sleep(7.49) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas

        print(i)

        

        print(Longueur_d_onde)
        print(Tension_Phidget_echantillon)
        print(len(Tension_Phidget_echantillon))
        voltageInput0.close() 
    return  Longueur_d_onde, Tension_Phidget_echantillon
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


## Classe Application

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Application VARIAN 634")
        self.geometry("700x450")
        self.iconbitmap("test_images\Polytech_clermond_logo.ico")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "Polytech_clermond_logo.ico")), size=(30, 30))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "optique_spectro.png")), size=(441, 200))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  VARIAN 634", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Accueil",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Balayage",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Continu",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="INFORMATIONS", image=self.image_icon_image)
        self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
     
        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

            # Bouton Page Balayage
        self.second_frame_button_1= customtkinter.CTkButton(self.second_frame, text="Acquisition balayage" , command=self.Acquisition)
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.second_frame_button_2= customtkinter.CTkButton(self.second_frame, text="Graphique balayage" , command=self.Acquisition_graph_balayage)
        self.second_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
     

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # Bouton Page Continu
        self.third_frame_button_1= customtkinter.CTkButton(self.third_frame, text="Acquisition continu" , command=self.Acquisition)
        self.third_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.third_frame_button_2= customtkinter.CTkButton(self.third_frame, text="Graphique continu" , command=self.Acquisition_graph_continu)
        self.third_frame_button_2.grid(row=2, column=0, padx=20, pady=10)



        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def sidebar_button_event(self):
        print("sidebar_button click")
   

   # Méthode pour l'analyse des données 

    def Acquisition_graph_balayage(self): # Tracer un graphique pour le balayage x=longueur d'onde / y= Tension
        [x,y]= Recup_tension_Phidget(n=5) 
        plt.plot(x, y)
        plt.xlabel("Longueur d'onde (nm)")
        plt.ylabel('Tension du Phidget (Volt)')
        plt.title("Mode Balayage")
        plt.show()
    
    def Acquisition_graph_continu(self): # Tracer un graphique pour le continu
        [x,y]= Recup_tension_Phidget(n=10)         
        plt.plot(x, y)
        plt.xlabel("Temps (s)")
        plt.ylabel('Tension du Phidget (Volt)')
        plt.title("Mode Continu")
        plt.show()

    def Acquisition(self):        
        L=[]
        Recup_tension_Phidget(n=10)




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

	

