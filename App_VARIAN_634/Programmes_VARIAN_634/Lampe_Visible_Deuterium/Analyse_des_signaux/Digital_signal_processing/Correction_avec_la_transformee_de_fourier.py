import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, hilbert

# Lire le fichier ODS
Chemin_acces="Manip\Manip_24_03_2023\Fente_1mm"

# Lire le fichier ODS
data_solution_blanc = pd.read_csv(Chemin_acces +'\solution_blanc.csv', encoding='ISO-8859-1')
data_solution_echantillon= pd.read_csv(Chemin_acces +'\solution_echantillon1.csv', encoding='ISO-8859-1')
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


[Tension_blanc,Tension_echantillon]=correction_absorbance_negative(Tension_blanc,Tension_echantillon)

Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))


# Exemple de signal (remplacez-le par le vôtre)
plt.plot(Longueur_donde,Tension_blanc,"red")
plt.plot(Longueur_donde,Tension_echantillon)
plt.show()
# Appliquer la transformée de Fourier
fft_signal = np.fft.fft(Absorbance)
plt.plot(fft_signal)
plt.show()



# Définir le seuil pour supprimer les harmoniques de faible amplitude
seuil = 3  # Vous pouvez ajuster cette valeur en fonction de vos besoins

# Supprimer les harmoniques de faible amplitude
fft_signal_filtre = np.where(np.abs(fft_signal) > seuil, fft_signal, 0)
plt.plot(fft_signal_filtre)
plt.show()



# Appliquer la transformée de Fourier inverse pour récupérer le signal filtré
Absorbance_filtre = np.fft.ifft(fft_signal_filtre)


# Afficher le signal original et le signal filtré

plt.figure()
plt.subplot(2, 1, 1)
plt.plot(Longueur_donde, Absorbance)
plt.title("Signal original")
plt.subplot(2, 1, 2)
plt.plot(Longueur_donde, np.real(Absorbance_filtre))
plt.title("Signal filtré")
plt.tight_layout()
plt.show()




def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='same')

Absorbance_filtre=np.real(Absorbance_filtre)
positive_peaks, _ = find_peaks(Absorbance_filtre)


envelope_signal = np.zeros_like(Absorbance_filtre)
envelope_signal[positive_peaks] = Absorbance_filtre[positive_peaks]


window_size =  10 # Ajustez cette valeur en fonction de la taille de votre signal
smoothed_envelope = moving_average(np.abs(envelope_signal), window_size)

analytic_signal = hilbert(Absorbance_filtre)
amplitude_envelope = np.abs(analytic_signal)

plt.figure(figsize=(12, 6))
plt.plot(Longueur_donde, Absorbance, label='Signal original')
plt.plot(Longueur_donde, smoothed_envelope, label="Enveloppe lissée", linestyle='--', color='red')
plt.plot(Longueur_donde, amplitude_envelope, label="Enveloppe lissée 2", linestyle='--', color='green')

plt.xlabel("Temps")
plt.ylabel("Amplitude")
plt.legend()
plt.show()