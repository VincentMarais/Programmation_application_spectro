import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import matplotlib.pyplot as plt

# Configurations lorsque le signal de commande de la lampe au xénon est réglé à 20Hz
SAMPLES_PER_CHANNEL = 32000
SAMPLE_RATE = 250000
CHANNELS = ['Dev1/ai0']  # Remplacez ceci par le nom de votre canal
NUM_ACQUISITIONS = 10  # Remplacez ceci par le nombre d'acquisitions que vous souhaitez effectuer
input_range = 0.2  # Gamme de tension en Volts

# Stockage du minimum de tension pour chaque acquisition
min_tensions = []

with nidaqmx.Task() as task:
    # Configurer la tâche
    for channel in CHANNELS:
        task.ai_channels.add_ai_voltage_chan(channel, terminal_config=TerminalConfiguration.RSE)
    
    task.timing.cfg_samp_clk_timing(SAMPLE_RATE, samps_per_chan=SAMPLES_PER_CHANNEL,
                                    sample_mode=AcquisitionType.FINITE, min_val=-input_range, max_val=input_range)
    for _ in range(NUM_ACQUISITIONS):
        # Acquisition des données
        data = task.read(number_of_samples_per_channel=SAMPLES_PER_CHANNEL)
        
        # Conversion des données en un tableau numpy pour faciliter les calculs
        np_data = np.array(data)
        
        # Trouver et stocker le minimum
        min_voltage = np.min(np_data)
        min_tensions.append(min_voltage)


x=np.linspace(1,NUM_ACQUISITIONS,NUM_ACQUISITIONS)
plt.plot(x,min_tensions)
plt.xlabel('Indice')
plt.ylabel('Tension')
plt.show()

