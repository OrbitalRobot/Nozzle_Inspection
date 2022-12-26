import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from Weld_Scan import *
from time import sleep


def search_for_home(axis, speed, accel, search_vector):
	'''Causes c axis to search for the home sensor and set its home position

		   Parameters
		   ----------
		   axis : int
				The drive number of the axis to be homed

		   speed : int
				The speed at which to home the axis

		   accel : int
				The rate at which to reach the homing speed

		   search_vector : float
				The direction and angular distance to search for the home sensor

		   Returns
		   -------
		   Boolean
		   Status of successfully finding the home sensor in the search vector
		   '''

	starting_pos = mm.getActualPositions(axis=axis)
	mm.setSpeed(speed)
	mm.moveRelative(axis=axis, distance=search_vector)

	while True:
		distance_traveled = abs(mm.getActualPositions(axis=axis) - starting_pos)
		if home_sensor_detected():
			mm.stopContinuousMove(axis=axis, accel=accel)
			return True
		elif distance_traveled >= abs(search_vector):
			mm.stopContinuousMove(axis=axis, accel=accel)
			return False


# ********** CONSTANTS **********
# Homing parameters
AXIS = C_AXIS_DRIVE
HOME_POSITION = 0  # (deg)
SMALL_ROTATION_DISTANCE = 30 # (deg)
MAX_ROTATION_DISTANCE = 420 # (deg) max scan rotation is 440, -20 deg buffer
SPEED = HOMING_SPEED # (deg/s) recommended max = 10 deg/s for position accuracy
ACCEL = 5 # (deg/s^2) set low to prevent unnecessary wear
RE_APPROACH_DISTANCE = 10  # (deg)
# *******************************


mm = MachineMotionV2()


# Prepare system
set_ready_condition()


# Find all connected digital IO modules
detectedIOModules = mm.detectIOModules()


# Wait until IO module is detected
while (detectedIOModules is None):
	print("I can't find the IO module")
	sleep(0.1)

prev_b_angle = mm.getActualPositions(axis=B_AXIS_DRIVE)

# Verify not at home already
if home_sensor_detected() is not True:

	retract_cylinder()

	mm.setSpeed(SPEED)
	mm.moveToPosition(axis=B_AXIS_DRIVE, position=B_SAFE_ANGLE)
	mm.waitForMotionCompletion(B_AXIS_DRIVE)

	# Check for sensor in the positive direction
	search_for_home(axis=AXIS,
					speed=SPEED,
					accel=ACCEL,
					search_vector=SMALL_ROTATION_DISTANCE)
	sleep(0.5)

	if home_sensor_detected() is not True:
		# Check for sensor in the negative direction
		search_for_home(axis=AXIS,
					speed=SPEED,
					accel=ACCEL,
					search_vector=-MAX_ROTATION_DISTANCE)


# Leave home and re-approach slowly to be at precise home position
mm.waitForMotionCompletion(axis=AXIS)
sleep(0.2)
mm.setSpeed(SPEED)
mm.moveRelative(axis=AXIS, distance=RE_APPROACH_DISTANCE)
mm.waitForMotionCompletion(axis=AXIS)
sleep(0.2)
print("Searching in negative direction")
success = search_for_home(axis=AXIS,
				speed=SPEED/2,
				accel=ACCEL,
				search_vector=-(2 * RE_APPROACH_DISTANCE))


if success:
	print("Returned to home")
else:
	print("Failed to home correctly")


if home_sensor_detected() is True:  # At home position
	mm.setPosition(axis=AXIS, position=HOME_POSITION)


# Return b-axis to its previous position
mm.setSpeed(SPEED)
mm.moveToPosition(axis=B_AXIS_DRIVE, position=prev_b_angle)
mm.waitForMotionCompletion(B_AXIS_DRIVE)

mm.setSpeed(SPEED*2)
