import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from MachineMotion import *
from time import sleep


# ********** TODO after position sensors installed **********
# def cylinder_extended():
# 	extended_pin_state = mm.digitalRead(IO_NetworkID, cylinder_ext_sensor_IOpin)
# 	retracted_pin_state = mm.digitalRead(IO_NetworkID, cylinder_ret_sensor_IOpin)
# 	return (extended_pin_state == ON and retracted_pin_state == OFF)


# ********** TODO after position sensors installed **********
# def cylinder_retracted():
# 	extended_pin_state = mm.digitalRead(IO_NetworkID, cylinder_ext_sensor_IOpin)
# 	retracted_pin_state = mm.digitalRead(IO_NetworkID, cylinder_ret_sensor_IOpin)
# 	return (extended_pin_state == OFF and retracted_pin_state == ON)


def set_and_check_pin(deviceNetworkId=1,
					  pin=0, state=0, max_attempts=10, wait=0.2):
	success = False
	attempts = 0
	while (success == False) and (attempts < max_attempts):
		print(f"I've tried {attempts} times to change pin #{pin}'s state to {state}")
		mm.digitalWrite(deviceNetworkId, pin, state)
		sleep(wait)
		current_state = mm.digitalRead(deviceNetworkId, pin)
		print(f"State: {state}")
		print(f"Current state of pin {pin}: {current_state}.")
		if current_state == state:
			print("...and I finally got it!")
			success = True
			return success
		else:
			print("...but it's being a stubborn little bitch :(")
			attempts += 1

		if attempts == max_attempts:
			print(f"Attempt to set pin {pin} to state {state} failed.")
			return success




def extend_cylinder():
	'''Commands the pneumatic cylinder to extend

	Parameters
	----------
	None

	Returns
	-------
	Now: Boolean
	Now: True

	After Position Sensor Installed: Function Call
	After Position Sensor Installed: Call to cylinder_extended()
	'''

	ret_pin_state_change = set_and_check_pin(deviceNetworkId=IO_NetworkID,
									   pin=OUT_ret_cylinder_pin, state=0)
	# ********** TODO after position sensors installed **********
	#while cylinder_retracted():
		#sleep(0.1)

	ext_pin_state_change = set_and_check_pin(deviceNetworkId=IO_NetworkID,
									   pin=OUT_ext_cylinder_pin, state=1)
	# ********** TODO after position sensors installed **********
	#while not cylinder_extended():
		#sleep(0.1)
	#return cylinder_extended()
	status = ext_pin_state_change and ret_pin_state_change
	return status




def retract_cylinder():
	'''Commands the pneumatic cylinder to retract

	Parameters
	----------
	None

	Returns
	-------
	Now: Boolean
	Now: True

	After Position Sensor Installed: Function Call
	After Position Sensor Installed: Call to cylinder_retracted()
	'''

	ext_pin_state_change = set_and_check_pin(deviceNetworkId=IO_NetworkID,
									   pin=OUT_ext_cylinder_pin, state=0)
	# ********** TODO after position sensors installed **********
	#while cylinder_extended:
		#sleep(0.1)

	ret_pin_state_change = set_and_check_pin(deviceNetworkId=IO_NetworkID,
									   pin=OUT_ret_cylinder_pin, state=1)
	# ********** TODO after position sensors installed **********
	#while not cylinder_retracted:
		#sleep(0.1)
	#return cylinder_retracted()
	status = ext_pin_state_change and ret_pin_state_change
	print(f"cylinder retract status: {status}")
	return status


mm = MachineMotionV2()

# IO parameters
IO_NetworkID = 1 # To be set depending on IO address
# TODO after pneumatic cylinder position sensors are installed
#IN_cylinder_ext_sensor_IOpin = 2 # Input pin (choose between 0,1,2,3)
#IN_cylinder_ret_sensor_IOpin = 3 # Input pin (choose between 0,1,2,3)
OUT_ext_cylinder_pin = 0 # Output pin (choose between 0,1,2,3)
OUT_ret_cylinder_pin = 2 # Output pin (choose between 0,1,2,3)
