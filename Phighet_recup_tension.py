from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
import time # Test Git

L=[]
def onVoltageChange(self, voltage):  # Le channel de 	
	L.append(voltage)
	print(L)

def main(n):
	
	voltageInput0 = VoltageInput()
	for k in range (0,n):		

		voltageInput0.setHubPort(0)
		voltageInput0.setDeviceSerialNumber(626587)

		voltageInput0.setOnVoltageChangeHandler(onVoltageChange)

		voltageInput0.openWaitForAttachment(5000)

		voltageInput0.close()		
	
	

	

main(4)



