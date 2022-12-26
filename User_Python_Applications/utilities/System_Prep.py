import sys
from MachineMotion import *
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")


def set_ready_condition():
	'''Attempts to reset the safety circuit in preparation to move the machine

	Parameters
	----------
	None

	Returns
	-------
	Boolean
	Status of successfully releasing the E-Stop and resetting the system
	'''

	print("Preparing System...")
	# When starting a program, one must remove the software stop before moving
	print("--> Removing software stop")
	eStop_released = mm.releaseEstop()
	print("--> Resetting system")
	system_reset = mm.resetSystem()
	print("Servos engaged...")
	return (eStop_released and system_reset)


def config_IO():
	'''Detects the IO module, sets the network ID and home sensor IO pin #

	Parameters
	----------
	None

	Returns
	-------
	Tuple
	(Status of successfully finding the IO module, home sensor IO pin #)
	'''

	print("Configuring IO...")
	# Detect all connected digital IO Modules
	IO_found = False
	detectedIOModules = mm.detectIOModules()
	if detectedIOModules is not None:
		IO_found = True
	IO_NetworkID = 1  # To be set depending on IO address
	input_pin_home_sensor = 0  # Read from input pin 0 (choose between 0,1,2,3)
	return IO_found, input_pin_home_sensor


def home_sensor_detected():
	'''Reports the status of the home sensor IO pin

	Paramters
	---------
	None

	Returns
	-------
	Boolean
	Status of the pin reading a value of 1 (True/HIGH)
	'''

	pin_value = mm.digitalRead(IO_NetworkID, home_sensor_IOpin)
	return pin_value == 1


mm = MachineMotionV2()


# IO parameters
IO_NetworkID = 1 # To be set depending on IO address
home_sensor_IOpin = 0 # Input pin# (choose between 0,1,2,3)
