import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from Weld_Scan import *


def home_b_z():
	'''Movement sequence to safely home axes b and z

		   Parameters
		   ----------
		   None

		   Returns
		   -------
		   Boolean
		   Status of successful homing sequence execution
		   '''

	retract_cylinder()

	print("Homing axis z...")
	mm.moveToHome(axis_z.drive)
	mm.waitForMotionCompletion(axis=axis_z.drive)

	mm.setSpeed(HOMING_SPEED/2)  # Rotary axes move faster than linear axes
	print("Homing axis b...")
	mm.moveToHome(axis_b.drive)
	mm.waitForMotionCompletion(axis=axis_b.drive)

	print("To home axis C, run the Home_C.py script")
	mm.setSpeed(NORMAL_SPEED)
	return True


# Init
mm = MachineMotionV2()
axes_ready = init()
io_ready, input_pin_home_sensor = config_IO()
system_ready = set_ready_condition()
cylinder_ready = retract_cylinder()
b_z_homed = home_b_z()

while not (axes_ready and io_ready and system_ready and
		   b_z_homed and cylinder_ready):
	sleep(0.1)

mm.setSpeed(NORMAL_SPEED)  # So that any jogging moves have predictable speed

print("\n----------------\n| System Ready |\n----------------\n")
