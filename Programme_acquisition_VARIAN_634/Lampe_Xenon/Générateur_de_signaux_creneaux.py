import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType, Edge, TaskMode , TerminalConfiguration
from nidaqmx.stream_writers import CounterWriter
import time
import matplotlib.pyplot as plt
import csv

Frequence_creneau = 20.0
Rapport_cyclique = 0.5
SAMPLES_PER_CHANNEL = 30000
SAMPLE_RATE = 250000
CHANNELS = ['Dev1/ai0']  # Remplacez ceci par le nom de votre canal
NUM_ACQUISITIONS = 10  # Remplacez ceci par le nombre d'acquisitions que vous souhaitez effectuer







def acquisition_tension(Frequence_creneau, Rapport_cyclique):
    min_tensions = []
    frequence = int(Frequence_creneau)

    with nidaqmx.Task() as task_impulsion , nidaqmx.Task() as task_voltage :
        task_impulsion.co_channels.add_co_pulse_chan_freq('/Dev1/ctr0', freq=Frequence_creneau[0], duty_cycle=Rapport_cyclique[0], initial_delay=0.0) # freq 1D numy et duty_cycle 1D numpy cf docs
        task_impulsion.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS)

        print(f"Génération du train d'impulsions avec une fréquence de {Frequence_creneau[0]} Hz et un rapport cyclique de {Rapport_cyclique[0]}")
        task_impulsion.start()

            # Ici, vous pouvez insérer une pause ou attendre un certain événement avant de passer à la génération suivante
        task_voltage.ai_channels.add_ai_voltage_chan(CHANNELS[0], terminal_config=TerminalConfiguration.DIFF, min_val=-1.0, max_val=1.0)
        
        task_voltage.timing.cfg_samp_clk_timing(SAMPLE_RATE, samps_per_chan=SAMPLES_PER_CHANNEL, sample_mode=AcquisitionType.FINITE)
        for _ in range(frequence):
            # Acquisition des données
            data = task_voltage.read(number_of_samples_per_channel=SAMPLES_PER_CHANNEL)
            # Conversion des données en un tableau numpy pour faciliter les calculs
            np_data = np.array(data)
            
            # Trouver et stocker le minimum
            min_voltage = np.min(np_data)
            min_tensions.append(min_voltage)
            print(np.shape(min_tensions))
        
        task_impulsion.stop()
        task_voltage.stop()

        moyenne=np.mean(min_tensions)
        print(min_tensions)
    return min_tensions, moyenne

i = 0
while i < 2:
    a = acquisition_tension(Frequence_creneau=np.array([Frequence_creneau]), Rapport_cyclique=np.array([Rapport_cyclique]))
    print(a)
    print(i)
    time.sleep(1)
    i += 1


def sauvegarder_donnees(nom_fichier, Liste_longueurs_d_onde, Liste_tensions, titre_1, titre_2): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2])
        for i in range(len(Liste_longueurs_d_onde)):
            writer.writerow([Liste_longueurs_d_onde[i], Liste_tensions[i]])

nom_fichier="C:\\Users\\vimarais\\Documents\\Projet_GP_Spectro\\27_06_2023\\Fente_2mm\\Fichier_OK.csv"
x = np.linspace(0, len(a[0]), len(a[0]))

sauvegarder_donnees(nom_fichier,x, a[0], 'Indice', 'Tension (Volt)')
Titre="Tension_photodiode_Lampe_XENON"
plt.plot(x, a[0])
plt.axhline(y=a[1], color='red', linestyle="--")
plt.xlabel('Indice')
plt.ylabel('Tension (Volt)')
plt.savefig("C:\\Users\\vimarais\\Documents\\Projet_GP_Spectro\\27_06_2023\\Fente_2mm\\"+Titre+".pdf")
plt.show()

