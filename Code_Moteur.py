import serial  
import time 

s = serial.Serial('COM5', 115200)

s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(2)   # Attend initialisation un GRBL
s.flushInput()  # 

# Départ 7.25mm / 20 - 7.25 = 12.75mm où 20 course de la vis 

def deplacement(pas): #
        g_code= '$110=10'+ '\n'
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X' + str(pas) + '\n'
        s.write(gcode_1.encode())


def back(pas):
        g_code= '$110=10'+ '\n' # 10 mm/min vitesse opti
        s.write(g_code.encode())
        time.sleep(0.5)
        gcode_1= 'G0X-' + str(pas) + '\n'
        s.write(gcode_1.encode())
        


def aller_retour(pas): # A 
        deplacement(pas)
        back(pas)

deplacement(2)