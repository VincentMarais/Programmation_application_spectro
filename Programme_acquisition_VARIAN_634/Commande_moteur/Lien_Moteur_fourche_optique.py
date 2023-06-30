from pyfirmata import Arduino, util
import time
import serial  
import time 
import re


"""
FOURCHE OPTIQUE
"""

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
MOTEUR NEMA 17 
"""


COM_PORT = 'COM3'
BAUD_RATE = 115200
INITIALIZATION_TIME = 2

s = serial.Serial(COM_PORT, BAUD_RATE)
s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(INITIALIZATION_TIME)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.


def modif_vitesse_translation(vitesse_translation_vis):
    g_code = '$110=' + str(vitesse_translation_vis) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)


def deplacer_moteur_vis(course_vis, vitesse_translation_vis): # Fonction qui pilote le moteur      
        g_code= 'G90'+ '\n'
        s.write(g_code.encode())
        time.sleep(0.5)
        modif_vitesse_translation(vitesse_translation_vis)        
        gcode_1= 'G0X' + str(course_vis) + '\n'
        s.write(gcode_1.encode())

def deplacer_moteur_miroir(course_vis): # Fonction qui pilote le moteur      
        g_code= 'G91'+ '\n'
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0Y' + str(course_vis) + '\n'
        s.write(gcode_1.encode())

def retour_moteur(pas_vis, vitesse_translation_vis): 
        modif_vitesse_translation(vitesse_translation_vis)
        g_code= 'G91'+ '\n' # Le moteur ce déplace en relatif
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X-' + str(pas_vis) + '\n' # Le moteur ce déplace linéairement de -pas_vis (retour_moteur en arrière)
        s.write(gcode_1.encode())


def deplacement_double_moteur(course_vis, course_miroir, vitesse_translation_vis):
     deplacer_moteur_vis(course_vis, vitesse_translation_vis)
     deplacer_moteur_miroir(course_miroir)



"""
LIEN FOURCHE OPTIQUE ET MOTEUR
"""

def initialisation_acquisition():
    if 