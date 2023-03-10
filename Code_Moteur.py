import serial  
import time 

s = serial.Serial('COM5', 115200)

s.write("\r\n\r\n".encode()) # encode pour convertir "\r\n\r\n" 
time.sleep(2)   # Wait for grbl to initialize 
s.flushInput()  # Flush startup text in serial input

def deplacement():
        gcode= 'G0 X50' + '\n'
        s.write(gcode.encode())

# Wait here until grbl is finished to close serial port and file.
