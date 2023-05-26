import nidaqmx
from nidaqmx.constants import TerminalConfiguration

"""
Programme pour aquérir la tension de la carte NI 6221

"""
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0", terminal_config=TerminalConfiguration.RSE)
    
    # Configure le task pour un échantillonnage continu.
    task.timing.cfg_samp_clk_timing(1000, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
    
    try:
        # Commence l'échantillonnage.
        task.start()

        while True:
            # Lire la valeur de tension.
            voltage = task.read()
            print(f"La tension lue est : {voltage} V")

    except KeyboardInterrupt:
        # Si l'utilisateur appuie sur CTRL+C, arrêtez l'échantillonnage.
        print("Échantillonnage arrêté par l'utilisateur.")
    finally:
        # Assurez-vous que la tâche est bien arrêtée à la fin.
        task.stop()
