import numpy as np
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
import matplotlib.pyplot as plt

# Configurations lorsque le signal de commande de la lampe au xénon est réglé à 20Hz
SAMPLES_PER_CHANNEL = 30000
SAMPLE_RATE = 250000
CHANNELS = ['Dev1/ai0', 'Dev1/ai1']  

"""
Fonction acquisition_tension
"""
def acquisition_tension(Frequence_creneau, Rapport_cyclique, Channel):
    min_tensions = []

    if Channel=='ai0': # Acquisition sur le 1er capteur
        
        with nidaqmx.Task() as task_impulsion , nidaqmx.Task() as task_voltage :
            task_impulsion.co_channels.add_co_pulse_chan_freq('/Dev1/ctr0', freq=Frequence_creneau[0], duty_cycle=Rapport_cyclique[0], initial_delay=0.0) # freq 1D numy et duty_cycle 1D numpy cf docs
            task_impulsion.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS)

            print(f"Génération du train d'impulsions avec une fréquence de {Frequence_creneau[0]} Hz et un rapport cyclique de {Rapport_cyclique[0]}")
            task_impulsion.start()

                # Ici, vous pouvez insérer une pause ou attendre un certain événement avant de passer à la génération suivante
            task_voltage.ai_channels.add_ai_voltage_chan(CHANNELS[0], terminal_config=TerminalConfiguration.DIFF)
            
            task_voltage.timing.cfg_samp_clk_timing(SAMPLE_RATE, samps_per_chan=SAMPLES_PER_CHANNEL, sample_mode=AcquisitionType.FINITE)
            frequence = int(Frequence_creneau)
            for _ in range(frequence):
                # Acquisition des données
                    data = task_voltage.read(number_of_samples_per_channel=SAMPLES_PER_CHANNEL)
                # Conversion des données en un tableau numpy pour faciliter les calculs
                    np_data = np.array(data)
                
                # Trouver et stocker le minimum
                    min_voltage = np.min(np_data)
                    min_tensions.append(min_voltage)
            task_impulsion.stop()
            task_voltage.stop()
            moyenne=np.mean(min_tensions)
        return moyenne


    elif  Channel=='ai1': # Acquisition sur le 2eme capteur
        with nidaqmx.Task() as task_impulsion , nidaqmx.Task() as task_voltage :
            task_impulsion.co_channels.add_co_pulse_chan_freq('/Dev1/ctr0', freq=Frequence_creneau[0], duty_cycle=Rapport_cyclique[0], initial_delay=0.0) # freq 1D numy et duty_cycle 1D numpy cf docs
            task_impulsion.timing.cfg_implicit_timing(sample_mode=AcquisitionType.CONTINUOUS)

            print(f"Génération du train d'impulsions avec une fréquence de {Frequence_creneau[0]} Hz et un rapport cyclique de {Rapport_cyclique[0]}")
            task_impulsion.start()

                # Ici, vous pouvez insérer une pause ou attendre un certain événement avant de passer à la génération suivante
            task_voltage.ai_channels.add_ai_voltage_chan(CHANNELS[1], terminal_config=TerminalConfiguration.DIFF)
            
            task_voltage.timing.cfg_samp_clk_timing(SAMPLE_RATE, samps_per_chan=SAMPLES_PER_CHANNEL, sample_mode=AcquisitionType.FINITE)
            frequence = int(Frequence_creneau)
            for _ in range(frequence):
                # Acquisition des données
                    data = task_voltage.read(number_of_samples_per_channel=SAMPLES_PER_CHANNEL)
                # Conversion des données en un tableau numpy pour faciliter les calculs
                    np_data = np.array(data)
                
                # Trouver et stocker le minimum
                    min_voltage = np.min(np_data)
                    min_tensions.append(min_voltage)
            task_impulsion.stop()
            task_voltage.stop()
            moyenne=np.mean(min_tensions)
        return moyenne



