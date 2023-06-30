import serial  
import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType, Edge, TaskMode , TerminalConfiguration
from nidaqmx.stream_writers import CounterWriter
import time # bibliothèque temps 
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
import re
import os
from pyfirmata import Arduino, util

 
"""
INITIALISATION DE L'ARDUINO + CARTE NI-PCI 6221
"""
# Constantes
COM_PORT = 'COM3'
BAUD_RATE = 115200
INITIALIZATION_TIME = 2
Frequence_creneau = np.array([20.0]) # 20Hz l'amplitude de la tension est maximal au borne de la photodiode, si on augmente la fréquence au borne de la photodiode => diminution de la tension
Rapport_cyclique = np.array([0.5]) # Déterminer un rapport cyclique optimal pour la mesure
SAMPLES_PER_CHANNEL = 30000 # Nombre d'échantillon récupéré
SAMPLE_RATE = 250000 # Fréquence d'échantillonage maximal de la carte (on récupérer une partie du signal cf critère de Shannon)
CHANNELS = ['Dev1/ai0', 'Dev1/ai1']  
NUM_ACQUISITIONS = 20  # Remplacez ceci par le nombre d'acquisitions que vous souhaitez effectuer


Date='30_06_2023' # A modifier à chaque jour de projet
Taille_de_fente='Fente_2nm' # A modifier si on change de fente


# Initialisation arduino
s = serial.Serial(COM_PORT, BAUD_RATE)
s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(INITIALIZATION_TIME)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.



""" 
Programme MOTEUR

"""
def etat_mot():
    """
    Entree : Aucune

    Sortie : renvoie les 10 premiers caractère de l'état du moteur 

    But: Savoir si le moteur est en mouvement "Run" ou non "Idle"
    """
    g_code='?' + '\n' # '?' en g_code : Affiche l’état actif de Grbl (Idle, Run, Hold, Door, Home, Alarm, Check) et la position en temps réel avec les coordonnées de la machine ou les coordonnées de travail.
    s.write(g_code.encode())

    return s.read(10)

def param_mot():    
    """
    Entree : Aucune

    Sortie : Aucune

    But: Afficher de type de déplacement du moteur : G90 déplacement absolue
    """
    g_code='$G' + '\n' # $G - Voir l'état de l'analyseur de GCODE
    s.write(g_code.encode())
    print(s.read(75))


def position_XYZ_vis():
    g_code= "?" + '\n' 
    s.write(g_code.encode())
    time.sleep(0.1)

    # Lire et traiter la réponse
    response = str(s.readline())
    while 'MPos' not in response:
        response = str(s.readline())
    
    # Extraire les coordonnées X, Y, et Z
    match = re.search(r"MPos:([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+)", response)
        
    x_pos, y_pos, z_pos = [float(coordinate) for coordinate in match.groups()]
    
    return x_pos



def deplacer_vis(pas): # Fonction qui pilote le moteur      
        g_code= 'G90'+ '\n' # Le moteur ce déplace en relatif
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X' + str(pas) + '\n'
        s.write(gcode_1.encode())
        


def retour_vis(pas): 
        g_code= '$110=10'+ '\n' # On modifie la vitesse_translation_vis de translation de la vis (mm/min)
        s.write(g_code.encode())
        time.sleep(0.5)
        g_code= 'G91'+ '\n' # Le moteur ce déplace en relatif
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X-' + str(pas) + '\n' # Le moteur ce déplace linéairement de -pas (retour_vis en arrière)
        s.write(gcode_1.encode())


def modif_vitesse_translation_vis(vitesse_translation):
    g_code = '$110=' + str(vitesse_translation) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)



def deplacer_moteur_miroir(course_miroir): # Fonction qui pilote le moteur            
        g_code= 'G91'+ '\n' # Le moteur ce déplace en relatif
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0Y' + str(course_miroir) + '\n'
        s.write(gcode_1.encode())



"""
FOURCHE OPTIQUE

"""

# remplacer '' par le port série correct de votre Arduino pour la fourche optique
board = Arduino('COM8')

        # utiliser l'itérateur seulement pour les entrées analogiques (non nécessaire ici)
it = util.Iterator(board)
it.start()
pin = board.get_pin('d:3:i')  # d pour digital, 3 pour le pin 3, i pour input

def fourche_optique_etat():
        # définir le pin 3 comme entrée


    # une boucle pour lire l'état du pin
    state = pin.read()  # lire l'état du pin
            
    if state is not None:
            if state:
                        return 'Bonne photodiode'
            else:
                        return 'Mauvaise photodiode'
    else:
        return 'Le pin n\'est pas reconnu.'
    
"""
PROGRAMME CARTE NI 6221
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


"""
LIEN MOTEUR ET CARTE NI PCI 6221

"""


def mode_precision(course_vis, nombre_de_mesures, vitesse_translation_vis, Frequence_creneau, Rapport_cyclique):  # d: distance parcouru par la vis en mm/  n: nombre de mesure de tension / vitesse_translation_vis: vitesse_translation_vis translation de la vis (mm/min)
    """
    Entrée :

    Sortie : 
    
    """
    
    Tensions_capteur_1= []
    Tensions_capteur_2= []

    Longueur_d_onde=[]
    pas_de_vis=[]
    i=0
    pas=course_vis/nombre_de_mesures # 0.5mm Pas de la vis (cf Exel)
    temps_par_pas= (pas*60)/vitesse_translation_vis # Temps pour faire un pas 

    
    """
    Initialisation moteur    
    """
    a=fourche_optique_etat()
    print(a)
    if a!='Bonne photodiode':
        while a!='Bonne photodiode':
            a=fourche_optique_etat()
            if a=='Mauvaise photodiode':
                print("TOURNE 0.4 car :", a)                  
                deplacer_moteur_miroir(0.4) # Le moteur doit faire une angle de 60°                 
                time.sleep(1)
                a=fourche_optique_etat()
                print("TOURNE -0.4 car :", a)
                deplacer_moteur_miroir(-0.4) # Le moteur doit faire une angle de 60° 

            else:
                print(a)

        else: 
            print(a)
    g_code= 'G90'+ '\n' # Le moteur ce déplace en relatif
    s.write(g_code.encode())
    time.sleep(0.5)

    g_code= '$110=' + str(vitesse_translation_vis) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)
    while i < course_vis: # Tant que la vis n'a pas parcouru une distance course_vis

        Tension_capteur_1=acquisition_tension(Frequence_creneau, Rapport_cyclique, 'ai0' )
        Tensions_capteur_1.append(Tension_capteur_1) # 
        print("Tension photodiode 1 (Volt) :", Tensions_capteur_1)
        print("Taille de la liste Tension photodiode 1 :", len(Tensions_capteur_1))

        deplacer_moteur_miroir(0.33334) # Le moteur doit faire une angle de 60° 
        time.sleep(0.5)
        Tension_capteur_2=acquisition_tension(Frequence_creneau, Rapport_cyclique, 'ai1' )
        Tensions_capteur_2.append(Tension_capteur_2) # 
        print("Tension photodiode 2 (Volt) :",Tensions_capteur_2)
        print("Taille de la liste photodiode 2 :", len(Tensions_capteur_2))

        deplacer_moteur_miroir(-0.33334) # Le moteur doit faire une angle de 60° 
        time.sleep(0.5)

        pas_de_vis.append(i)
        Longueur_d_onde.append(-31.10419907*i +800) # Je suppose que l'on part à 400nm -> 5.4mm et que l'on fini à 800 nm --> 18.73nm
        
        deplacer_vis(i+pas) # Le moteur travail en mode absolue par défaut G90 
        
        print("Pas de vis (mm) :", i)     
        print("Longueur d\'onde (nm) :", Longueur_d_onde)
        print("Taille de la liste Longueur d\'onde (nm) :", len(Longueur_d_onde))
        
        time.sleep(temps_par_pas) # Comme $110 =4mm/min et le pas de vis est de 0.5mm => Le moteur réalise un pas de vis en 7.49s
        i+=pas

        

    Tensions_capteur_1.reverse() # On retourne car on commence à 800nm (le rouge) et on termine dans UV 
    Tensions_capteur_2.reverse() # On retourne car on commence à 800nm (le rouge) et on termine dans UV 

    Longueur_d_onde.reverse()
    return  Longueur_d_onde, Tensions_capteur_1, Tensions_capteur_2, pas_de_vis




"""
PARTIE ACQUISITION DES DONNEES
""" 

# Fonction pour écrire les données dans un fichier CSV
def sauvegarder_donnees(nom_fichier, Liste_longueurs_d_onde, Liste_tensions, Liste_pas_vis, titre_1, titre_2, titre_3): # nom_Fichier: str / Liste_longueurs_d_onde, Liste_tensions: Liste / titre_1, titre_2: str
    with open(nom_fichier, 'w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow([titre_1, titre_2,titre_3])
        for i in range(len(Liste_longueurs_d_onde)):
            writer.writerow([Liste_longueurs_d_onde[i], Liste_tensions[i], Liste_pas_vis[i]])




def maximum(liste):
    maxi = liste[0]
    p=0
    for i in range(len(liste)):
        if liste[i] > maxi:
            p = i
            maxi=liste[i]

    return p



"""
AFFICHAGE DES DONNEES
"""

def graph(fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin): # fichier_blanc, fichier_echantillon: (str) Chemin d'acces des fichier creer pour l'expérience 
    data_1 = pd.read_csv(fichier_blanc,  encoding='ISO-8859-1')
    data_2= pd.read_csv(fichier_echantillon,  encoding='ISO-8859-1')

# Obtenir les colonnes 'Longueur d\'onde' et Tension Blanc et Tension echantillon
    Longueur_donde = data_1['Longueur d\'onde (nm)']
    Tension_blanc = data_1['Tension blanc (Volt)']
    Tension_echantillon= data_2['Tension échantillon (Volt)']
    Absorbance=np.log10(np.abs(Tension_blanc)/np.abs(Tension_echantillon))
    Pic_d_absorbance=max(Absorbance)
    Pic_longueur_donde=Longueur_donde[maximum((Absorbance))]

# Création du graphique
    plt.plot(Longueur_donde, Absorbance)
    plt.xlabel('Longueur d\'onde (nm)')
    plt.ylabel('Absorbance')
    plt.title('Absorbance du '+ Nom_echantillon)

# Mise en évidence du point de pic en rouge
    plt.scatter(Pic_longueur_donde, Pic_d_absorbance, color='red')


# Annotation des coordonnées du point
    plt.annotate('({:.2f} nm, {:.2f})'.format(Pic_longueur_donde, Pic_d_absorbance),
             xy=(Pic_longueur_donde , Pic_d_absorbance),
             xytext=(Pic_longueur_donde + 10 , Pic_d_absorbance),
             fontsize=10,
             color='red',
             arrowprops=dict(facecolor='red', arrowstyle='->'))

# Ligne pointillée reliant le point de pic à l'axe des x
    plt.hlines(y=Pic_d_absorbance, xmin=Longueur_donde[0] , xmax=Pic_longueur_donde, linestyle='dashed', color='red')

# Ligne pointillée reliant le point de pic à l'axe des y
    plt.vlines(x=Pic_longueur_donde, ymin=min(Absorbance), ymax=Pic_d_absorbance, linestyle='dashed', color='red')
# Affichage du graphique
    plt.savefig(chemin +'\\'+ Titre+".pdf")

    plt.show()


"""
ACQUISITION
"""

def solutions(course_vis, nombre_de_mesure, vitesse_translation_vis, Frequence_creneau, Rapport_cyclique, fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin): # Départ 7.25mm / 21 - 7.25 = 13.75mm où 21 course de la vis total de la vis => course_vis=13.75mm
    nom_colonne_tension_blanc='Tension blanc (Volt)'

    nom_colonne_tension_echantillon='Tension échantillon (Volt)'


    [Longueur_d_onde, Tension_blanc, Tension_echantillon, pas_de_vis] = mode_precision(course_vis, nombre_de_mesure, vitesse_translation_vis, Frequence_creneau, Rapport_cyclique)
    
    sauvegarder_donnees(fichier_echantillon, Longueur_d_onde, Tension_echantillon, pas_de_vis, 'Longueur d\'onde (nm)', nom_colonne_tension_echantillon,'Liste_pas_vis')
    sauvegarder_donnees(fichier_blanc, Longueur_d_onde, Tension_blanc, pas_de_vis, 'Longueur d\'onde (nm)', nom_colonne_tension_blanc,'Liste_pas_vis')

    s=str(etat_mot())
    while 'Idle' not in s: # 'Idle': Instruction GRBL pour dire ce que moteur est à l'arrêt / 'Run' le moteur tourne
        s=str(etat_mot())

    print(s)
    
    param_mot()
    retour_vis(course_vis)
    param_mot()

    graph(fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin)







# Concaténer les variables pour former le chemin d'accès complet
projet = "Projet_GP_Spectro"

chemin = os.path.join("C:\\Users\\vimarais\\Desktop\\Programmation_application_spectro-master\\Manip", Date, Taille_de_fente)

# Vérifier si le répertoire existe déjà
if not os.path.exists(chemin):
    # Créer le répertoire en utilisant le chemin d'accès
    os.makedirs(chemin)
    print("Répertoire créé avec succès :", chemin)
else:
    print("Le répertoire existe déjà :", chemin)


course_vis=13.33 # 7mm
nombre_de_mesures=200 # A modifier si on veut être plus précis
vitesse_translation_vis=10 # 4mm/min



fichier_blanc=  chemin + '\Tension_de_blanc_' + Date + "_" + Taille_de_fente + '.csv'
fichier_echantillon=  chemin + '\Tension_de_echantillon_' + Date + "_" + Taille_de_fente + '.csv'

projet = "Projet_GP_Spectro"
programmation = "Programmation_Spectro/Programmation_application_spectro"

Nom_echantillon='bleu de bromophenol' # A modifier si on change de composé chimique
Titre="Absorbance_"+ "_" + Nom_echantillon+ Date+"_"+ Taille_de_fente  

solutions(course_vis, nombre_de_mesures, vitesse_translation_vis, np.array([Frequence_creneau]), np.array([Rapport_cyclique]), fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin) # course_vis 13.75 mm / 260 points / vitesse_translation_vis = 4mm/min
#graph(fichier_blanc, fichier_echantillon, Nom_echantillon, Titre, chemin)

#mode_precision(course_vis, nombre_de_mesures, vitesse_translation_vis, Frequence_creneau=np.array([Frequence_creneau]), Rapport_cyclique=np.array([Rapport_cyclique]))

