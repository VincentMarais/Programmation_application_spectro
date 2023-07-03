import tkinter as tk
from tkinter import filedialog
import csv

def enregistrer_csv():
    # Créer une fenêtre Tkinter
    fenetre = tk.Tk()
    fenetre.withdraw()  # Masquer la fenêtre principale
    
    # Ouvrir la boîte de dialogue pour enregistrer le fichier
    fichier_csv = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("Fichiers CSV", "*.csv")])
    
    # Vérifier si un nom de fichier a été sélectionné
    if fichier_csv:
        # Créer des données CSV de test
        donnees = [
            ['Nom', 'Age', 'Ville'],
            ['Alice', '25', 'Paris'],
            ['Bob', '30', 'Londres'],
            ['Charlie', '35', 'New York']
        ]
        
        # Enregistrer les données dans le fichier CSV
        with open(fichier_csv, 'w', newline='') as fichier:
            writer = csv.writer(fichier)
            writer.writerows(donnees)
        
        print("Fichier CSV enregistré avec succès : ", fichier_csv)
    else:
        print("Aucun fichier sélectionné.")

# Appeler la fonction pour enregistrer le fichier CSV
enregistrer_csv()