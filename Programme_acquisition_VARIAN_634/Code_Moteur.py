import serial  
import time 
import re

# Constantes:

COM_PORT = 'COM5'
BAUD_RATE = 115200
PHIDGET_HUB_PORT = 0
PHIDGET_SERIAL_NUMBER = 626587
INITIALIZATION_TIME = 2

s = serial.Serial(COM_PORT, BAUD_RATE)
s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(INITIALIZATION_TIME)   # Attend initialisation un GRBL
s.flushInput()  # Vider le tampon d'entrée, en supprimant tout son contenu.

def position_moteur_x():
    # Demande la position actuelle du moteur selon l'axe X
    s.write(b"?x\n")
    reponse = s.readline().decode().strip()
    position_x = reponse.split(":")[1]
    return int(position_x)



def position_XYZ():
    g_code= "?" + '\n' 
    s.write(g_code.encode())
    time.sleep(0.1)

    # Lire et traiter la réponse
    response = str(s.readline())
    print("Réponse brute :", response)
    while 'MPos' not in response:
        response = str(s.readline())
    
        # Extraire les coordonnées X, Y, et Z
    match = re.search(r"MPos:([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+)", response)
        
    x_pos, y_pos, z_pos = [float(coordinate) for coordinate in match.groups()]
    
    return x_pos


"""
Les méthodes reset_input_buffer() et flushInput() sont toutes deux utilisées pour vider le tampon d'entrée (input buffer) d'un port série. 
Cependant, il y a une différence entre ces deux méthodes.
reset_input_buffer() est une méthode de la bibliothèque PySerial qui permet de vider complètement le tampon d'entrée du port série. 
Cela signifie que toutes les données en attente dans le tampon d'entrée seront supprimées. 
Cette méthode est utile lorsque vous voulez vous assurer que le tampon d'entrée est vide avant de recevoir de nouvelles données.

flushInput() est également une méthode de PySerial qui permet de vider le tampon d'entrée. Cependant, contrairement 
à reset_input_buffer(), flushInput() ne supprime pas toutes les données en attente dans le tampon d'entrée. 
Au lieu de cela, elle supprime uniquement les données qui n'ont pas encore été lues par l'application. 
Cela peut être utile si vous voulez vider le tampon d'entrée sans perdre les données qui ont déjà été lues.

En résumé, la principale différence entre reset_input_buffer() et flushInput() est que la première supprime toutes les 
données en attente dans le tampon d'entrée, tandis que la seconde supprime uniquement les données qui n'ont pas encore 
été lues par l'application. Il est important de choisir la méthode appropriée en fonction de vos besoins en matière de 
gestion des données série.

"""

"""
Caractérisation DU MOTEUR

"""

def etat_mot():
    g_code='?' + '\n'
    s.write(g_code.encode())
    return s.read(40) # 10: On lit 10 caractère dans le serial

def param_mot():    
    g_code='$G' + '\n'
    s.write(g_code.encode())
    print(s.read(75))



def position_moteur_x():
    # Demande la position actuelle du moteur selon l'axe X
    g_code= "?" + '\n' 
    s.write(g_code.encode())
    time.sleep(0.1)
    reponse = str(s.readline())
    while 'MPos' not in reponse:
        reponse = str(s.readline())
        print(reponse)
    
    #reponse = reponse.split(":")
    #position_x=reponse.split(",")[0]
    #return float(position_x)

def modif_vitesse_translation(vitesse_translation_vis):
    g_code = '$110=' + str(vitesse_translation_vis) + '\n'
    s.write(g_code.encode())
    time.sleep(0.5)


def deplacement_domaine_visible():
        g_code= 'G90'+ '\n'
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X7.25' + '\n'
        s.write(gcode_1.encode())

        
def deplacer_moteur_vis(course_vis, vitesse_translation_vis): # Fonction qui pilote le moteur      
        g_code= 'G91'+ '\n'
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
deplacer_moteur(-0.754,4)
s=str(etat_mot())
while 'Idle' not in s:
    s=str(etat_mot())
"""


course_vis=-1
course_miroir=2
vitesse_translation_vis=4

#deplacement_double_moteur(course_vis, course_miroir, vitesse_translation_vis)
deplacer_moteur_miroir(course_miroir)
deplacer_moteur_vis(course_vis,vitesse_translation_vis)





