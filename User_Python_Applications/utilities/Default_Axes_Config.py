import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
import urllib.parse
from MachineMotion import *
from Axis import *

# Constants representing the drive numbers on the MachineMotion4 controller
Z_AXIS_DRIVE = 1
B_AXIS_DRIVE = 2
C_AXIS_DRIVE = 3


def config_axes(*axes):
	'''Sets the initial parameters for the given axes

	   Parameters
	   ----------
	   axes : list
	   all axes to be configured

	   Returns
	   -------
	   Boolean
	   Represents the status of all axes being successfully configured
	   '''

	print("Configuring axes...")

	for axis in axes:
		mm.configServo( drives=axis.drive,
						mechGain=axis.mechGain,
						directions=axis.direction,
						motorCurrent=axis.motorCurrent,
						tuningProfile=axis.tuningProfile,
						parentDrive=axis.parentDrive,
						motorSize=axis.motorSize,
						brake=axis.brake )
		mm.setAxisMaxSpeed(axis=axis.drive, speed=axis.max_speed)
		mm.setAxisMaxAcceleration(axis=axis.drive, acceleration=axis.max_accel)

		if axis.mechGain == MECH_GAIN.indexer_v2_deg_turn:
			mm.setAxisMaxSpeed(axis=axis.drive, speed=25)
			mm.configHomingSpeed(axis.drive, 5, units=UNITS_SPEED.mm_per_sec)

	return True


def init():
	'''Calls the config_axes function with all the axes listed in this file

	Parameters
	----------
	None

	Returns
	-------
	Boolean
	Status returned by config_axes after configuring all machine axes
	'''
	axes_ready = config_axes(*[axis_b, axis_c, axis_z])
	return axes_ready


mm = MachineMotionV2()

# Axis Z is the vertical linear axis
# Axis C is the rotary axis that rotates Axis Z (rotates during a scan)
# Axis B is the rotary axis that rotates around Axis Y
# Axis Y is an imaginary axis that is perpendicular to both X & Z as usual
# Axis X is the pneumatic actuator that presses the probe to the nozzle

axis_z = Axis(drive=Z_AXIS_DRIVE,
			  mechGain=MECH_GAIN.enclosed_ballscrew_16mm_turn,
			  direction=DIRECTION.REVERSE,
			  motorCurrent=10.0,
			  motorSize=MOTOR_SIZE.LARGE,
			  brake=BRAKE.PRESENT,
			  max_speed=100,
			  max_accel=10)

axis_b = Axis(drive=B_AXIS_DRIVE,
			  mechGain=MECH_GAIN.indexer_v2_deg_turn,
			  direction=DIRECTION.CLOCKWISE,
			  motorCurrent=10.0,
			  motorSize=MOTOR_SIZE.LARGE,
			  brake=BRAKE.PRESENT,
			  max_speed=30,
			  max_accel=5)

axis_c = Axis(drive=C_AXIS_DRIVE,
			  mechGain=MECH_GAIN.indexer_v2_deg_turn,
			  direction=DIRECTION.CLOCKWISE,
			  motorCurrent=10.0,
			  motorSize=MOTOR_SIZE.LARGE,
			  brake=BRAKE.NONE,
			  max_speed=30,
			  max_accel=2)  # Set low to avoid wobble while getting up to speed
