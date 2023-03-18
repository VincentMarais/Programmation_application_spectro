import serial  
import time 

s = serial.Serial('COM5', 115200)

s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(2)   # Attend initialisation un GRBL
s.flushInput()  # 



def deplacement(pas): # Fonction qui pilote le moteur
        gcode_1= 'G0 X' + str(pas) + '\n'
        s.write(gcode_1.encode())

        



deplacement(pas=0.5)  
