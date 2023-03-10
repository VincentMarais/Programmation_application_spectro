import serial  
import time 

s = serial.Serial('COM5',115200)

s.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize 
s.flushInput()  # Flush startup text in serial input

def deplacement():
        s.write("G0 X200" + '\n')

# Wait here until grbl is finished to close serial port and file.
