import nidaqmx
from nidaqmx.constants import AcquisitionType, Edge
from nidaqmx.stream_readers import AnalogMultiChannelReader
from nidaqmx.stream_writers import DigitalSingleChannelWriter
import numpy as np

def min_voltage_measure(n):
    # Configuration des paramètres
    sample_rate = 250000  # Fréquence d'échantillonnage
    samples_per_channel = 32000  # Nombre de points à acquérir
    voltage_range = 0.2  # Input range
    acquisition_time = samples_per_channel / sample_rate  # Temps d'acquisition
    
    # Création des tableaux pour stocker les résultats
    min_voltages = np.zeros((n,))

    # Création de la tâche d'acquisition
    with nidaqmx.Task() as acquisition_task, nidaqmx.Task() as generation_task:
        # Configuration de la tâche d'acquisition
        acquisition_task.ai_channels.add_ai_voltage_chan("Dev1/ai0", 
                                                         min_val=-voltage_range, 
                                                         max_val=voltage_range)
        acquisition_task.timing.cfg_samp_clk_timing(sample_rate, 
                                                    samps_per_chan=samples_per_channel,
                                                    sample_mode=AcquisitionType.FINITE)
        
        # Configuration de la tâche de génération
        generation_task.do_channels.add_do_chan("Dev1/port0/line0")
        generation_task.timing.cfg_samp_clk_timing(20, sample_mode=AcquisitionType.CONTINUOUS)  # Génération à 20Hz
        
        # Création du signal créneau
        square_wave = np.array([0, 5]*int(acquisition_time*20/2), dtype=np.uint8)
        
        # Synchronisation des tâches
        acquisition_task.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev1/do/StartTrigger",
                                                                       edge=Edge.RISING)
        acquisition_task.triggers.start_trigger.dig_edge_src = "/Dev1/do/SampleClock"

        writer = DigitalSingleChannelWriter(generation_task.out_stream)
        writer.write_many_sample_port_uint32(square_wave)
        
        # Boucle d'acquisition
        for i in range(n):
            reader = AnalogMultiChannelReader(acquisition_task.in_stream)
            data = np.zeros((1, samples_per_channel))
            reader.read_many_sample(data, samples_per_channel)

            # Enregistrement du minimum de tension
            min_voltages[i] = np.min(data)

    return min_voltages
