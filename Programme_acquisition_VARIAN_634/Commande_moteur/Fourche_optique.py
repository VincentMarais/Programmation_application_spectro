import serial
import time 
COM_PORT = 'COM3'
BAUD_RATE = 115200
INITIALIZATION_TIME = 2

s = serial.Serial(COM_PORT, BAUD_RATE)

def get_pin_state(pin):
    s.write('M119\r\n'.encode())  # Envoie la commande M119 pour obtenir l'état des broches
    while True:
        response = s.readline().decode().strip()
        if response.startswith('Endstop'):
            if 'X+:' in response:
                state = response.split('X+:')[-1].strip()
                if state == 'HIGH':
                    return True
                elif state == 'LOW':
                    return False
            else:
                return None  # Broche X+ non trouvée dans la réponse


pin_state = get_pin_state('X+')
if pin_state is not None:
    if pin_state:
        print("La fourche optique est en état HIGH.")
    else:
        print("La fourche optique est en état LOW.")
else:
    print("La broche X+ n'a pas été trouvée dans la réponse.")
