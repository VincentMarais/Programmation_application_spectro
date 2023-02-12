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
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Simulation" , command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Graphique" , command=self.graph)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)


        

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
        x = np.linspace(0, 10, 100)
        y = 2*np.sin(x)
        plt.plot(x, y)
        plt.xlabel('Temps')
        plt.ylabel('Tension du Phidget')
        plt.title('Tension du phidghet en fonction du temps')
        plt.show()


if __name__ == "__main__":
    app = App()
    app.mainloop()

###########################################################################################################################################
## Partie Phidget

	

	

