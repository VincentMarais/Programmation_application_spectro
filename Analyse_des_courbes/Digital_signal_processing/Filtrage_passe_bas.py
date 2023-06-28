import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, hilbert

# Lire le fichier ODS
Chemin_acces="Manip\Manip_24_03_2023\Fente_0_5mm"

# Lire le fichier ODS
data_solution_blanc = pd.read_csv(Chemin_acces +'\solution_blanc.csv', encoding='ISO-8859-1')
data_solution_echantillon= pd.read_csv(Chemin_acces +'\solution_echantillon.csv', encoding='ISO-8859-1')
#data_bruit_de_noir=pd.read_csv(Chemin_acces +'\Tension_de_noir_31_03_2023.csv', encoding='ISO-8859-1')



# Obtenir les colonnes 
Longueur_donde = data_solution_blanc['Longueur d\'onde (nm)']
Tension_blanc = data_solution_blanc['Tension blanc (Volt)']
Tension_echantillon= data_solution_echantillon['Tension échantillon (Volt)']
#pas_de_vis=data_solution_blanc['pas']
#Tension_de_noir=data_bruit_de_noir['Tension de noir (Volt)']
#pas_de_vis=caracterisation_du_pas_vis(DEPART_VIS, pas_de_vis)
def correction_absorbance_negative(Tension_blanc, Tension_echantillon):
    for i in range (len(Tension_blanc)):
        if np.abs(Tension_blanc[i]) < np.abs(Tension_echantillon[i]): # Ce qui est possible s'il y a du bruit de mesure 
            Tension_echantillon[i]=Tension_blanc[i]
    return Tension_blanc,Tension_echantillon


Tension_blanc=correction_absorbance_negative(Tension_blanc,Tension_echantillon)[0]
Tension_echantillon=correction_absorbance_negative(Tension_blanc,Tension_echantillon)[1]

Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))


def low_pass_filter(fourier_transform, cutoff_frequency, sampling_rate):
    """
    Applique un filtre passe-bas sur la transformée de Fourier du signal.
    
    :param fourier_transform: La transformée de Fourier du signal
    :param cutoff_frequency: La fréquence de coupure du filtre passe-bas
    :param sampling_rate: La fréquence d'échantillonnage du signal
    :return: La transformée de Fourier filtrée
    """
    frequency_axis = np.fft.fftfreq(len(fourier_transform), 1 / sampling_rate)
    mask = np.abs(frequency_axis) <= cutoff_frequency
    filtered_fourier_transform = fourier_transform * mask
    return filtered_fourier_transform


sampling_rate = 10  # Fréquence d'échantillonnage en Hz

# Calculer la transformée de Fourier du signal

fourier_transform = np.fft.fft(Tension_blanc)
fourier_transform_1=np.abs(fourier_transform) 

plt.plot(fourier_transform_1)
plt.show()
# Appliquer le filtre passe-bas
cutoff_frequency = 0.2  # Fréquence de coupure en Hz
filtered_fourier_transform = low_pass_filter(fourier_transform, cutoff_frequency, sampling_rate)
plt.plot(filtered_fourier_transform)
plt.show()
# Calculer le signal filtré
Tension_blanc_filtre = np.fft.ifft(filtered_fourier_transform)
Tension_blanc_filtre=np.real(Tension_blanc_filtre)


plt.figure(figsize=(12, 6))
plt.plot(Longueur_donde, Tension_blanc, label='Signal original')
plt.plot(Longueur_donde, Tension_blanc_filtre, label="Enveloppe lissée", linestyle='--', color='red')
plt.show()