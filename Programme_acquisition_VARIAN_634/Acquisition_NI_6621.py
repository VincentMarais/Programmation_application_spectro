import numpy as np
import nidaqmx
import matplotlib.pyplot as plt

def acquiere_tensions(n):
    # Création d'un objet de tâche pour la carte NI 6221
    with nidaqmx.Task() as task:
        # Configuration de la tâche pour l'acquisition de tension
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")  # Remplacez "Dev1/ai0" par le nom de votre canal d'entrée
        task.timing.cfg_samp_clk_timing(rate=250000, samps_per_chan=32000)
        
        # Acquisition des valeurs de tension
        data = task.read(number_of_samples_per_channel=n)

    return data

# Exemple d'utilisation
n = 100  # Nombre de valeurs de tension à acquérir

tensions = acquiere_tensions(n)
print("Valeurs de tension acquises :", tensions)

x=np.linspace(1,n,n)
plt.plot(x,tensions)
plt.xlabel('Indice')
plt.ylabel('Tension')
plt.show()

