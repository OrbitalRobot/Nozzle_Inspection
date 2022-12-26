import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from Default_Axes_Config import *
from MachineMotion import *
from System_Prep import *
from Pneumatics import *
from math import atan2, sqrt, degrees


WELD_RADII = {  # Values representing the inner radius of a given weld
	1: 568,  # Top weld
	2: 654,
	3: 728,
	4: 788,
	5: 842,
	6: 889,
	7: 932   # Bottom weld
}


'''Values representing the vertical distance from the
   bottom of the nozzle (or bottom of any lifting tooling
   it may be on) to the vertical center of a given weld.'''
WELD_ALTITUDES = {
	1: 1578,  # Top weld
	2: 1349,
	3: 1118,
	4: 897,
	5: 675,
	6: 450,
	7: 215    # Bottom weld
}


# Constants representing the physical dimensions of the machine
B_HORIZONTAL_ANGLE = 12					# (deg)
B_SAFE_ANGLE = B_HORIZONTAL_ANGLE + 75  # (deg) Avoid hitting tooling on nozzle
REST_PAD_HEIGHT = 15					# (mm)
Z_OFFSET = 311 - REST_PAD_HEIGHT		# (mm) Distance from rest pads to 0mm on z axis
X_RETRACTED_LENGTH = 760				# (mm) From center of b axis to end of probe
X_BUFFER = 50							# (mm) Amount x axis will extend when engaged
X_TOTAL_LENGTH = X_RETRACTED_LENGTH + X_BUFFER


# Movement constants used during homing operations
HOMING_SPEED = 10
NORMAL_SPEED = 30


class Weld_Scan:
	'''Description: Manages all aspects of the scan of an individual weld.

	   Unique instances are created in a given Weld_#_Setup.py file for each
	   weld that is scanned.

	   Attributes
	   ----------
	   weld_num: int
			Represents the number of the weld and is assigned in the
			corresponding Weld_#_Setup.py file

	   altitude: float
			Taken from the WELD_ALTITUDES dictionary by referencing
			the weld_num passed into the constructor at instantiation

	   radius: float
			Taken from the WELD_RADII dictionary by referencing
			the weld_num passed into the constructor at instantiation

		b_axis_speed: int
			The speed of the b axis when moving to the scan's starting position

		c_axis_speed: int
			The speed of the c axis when moving to the scan's starting position

		z_axis_speed: int
			The speed of the z axis when moving to the scan's starting position

		scan_speed: int
			The speed with which the c axis will rotate during the scan

		scan_accel: int
			The rate of acceleration with which the c axis will reach scan_speed

		scan_start_c_angle: float
			The angle of the c axis at the start of the scan

		scan_end_c_angle: float
			The angle of the c axis at the end of the scan

		scan_theta: float
			The angular distance covered by the scan

	   C_ANGLE_MIN & C_ANGLE_MAX: int
			Angular limits imposed by physical dimensions of machine components

	   Methods
	   -------
	   validate_scan_params()
			Checks the scan parameters to prevent damage to the machine

		get_b_z()
			Calculates the necessary b and z axis values to reach a given weld

		prepare_scan()
			A sequence of steps to prepare the machine to execute the scan
	   '''

	def __init__(self, weld_num, setup_params, scan_params):
		'''
        Parameters
        ----------
        weld_num : int
            The weld to be scanned, corresponds to keys in WELD_ALTITUDES
        setup_params : dict
            Sets b/c/z speeds from Weld_#_Setup.py when moving to weld
        scan_params : dict
            Sets speed/accel/start/stop angles of scan from Weld_#_Setup.py
        '''
		self.weld_num = weld_num
		self.altitude = WELD_ALTITUDES[self.weld_num]
		self.radius = WELD_RADII[self.weld_num]
		self.b_axis_speed = setup_params['b_axis_speed']
		self.c_axis_speed = setup_params['c_axis_speed']
		self.z_axis_speed = setup_params['z_axis_speed']
		self.scan_speed = scan_params['scan_speed']
		self.scan_accel = scan_params['scan_accel']
		self.scan_start_c_angle = scan_params['scan_start_c_angle']
		self.scan_end_c_angle = scan_params['scan_end_c_angle']
		self.scan_theta = self.scan_end_c_angle - self.scan_start_c_angle
		self.C_ANGLE_MIN = 0	#  Altering these values can damage the machine
		self.C_ANGLE_MAX = 420	#  Altering these values can damage the machine

	def validate_scan_params(self):
		'''Checks scan parameters to avoid machine damage or scanning backwards

		   Parameters
		   ----------
		   None

		   Returns
		   -------
		   Boolean
		   Represents whether the parameters entered are valid
		   '''

		if self.scan_start_c_angle < self.C_ANGLE_MIN:
			print("Starting angle of axis c must be > 0.")
			return False

		elif self.scan_end_c_angle > self.C_ANGLE_MAX:
			print("Ending angle of axis c must be < 420.")
			return False

		elif self.scan_start_c_angle >= self.scan_end_c_angle:
			print("Ending angle of axis c must be greater than starting angle.")
			return False

		else:
			return True


	def get_b_z(self):
		'''Calculates the b angle and z height to place the probe on the weld

		   Parameters
		   ----------
		   None

		   Returns
		   -------
		   Tuple
		   (b angle in degrees, z height in mm)
		   '''

		if self.altitude <= Z_OFFSET:  # Weld is below 0 on the Z axis
			z = 0
			y = self.altitude - Z_OFFSET  # Expecting y < 0
			x = self.radius
			b = B_HORIZONTAL_ANGLE + degrees(atan2(y, x))

		elif self.radius > X_TOTAL_LENGTH:  # X axis fits inside nozzle when horizontal
			z = self.altitude - Z_OFFSET
			b = B_HORIZONTAL_ANGLE

		else:  # Weld is above 0 on the Z axis and the X axis must be angled upward
			hyp = X_TOTAL_LENGTH
			y = sqrt((X_TOTAL_LENGTH ** 2) - (self.radius ** 2))
			x = self.radius
			b = B_HORIZONTAL_ANGLE + degrees(atan2(y, x))
			z = self.altitude - y - Z_OFFSET

		return b, z


	def prepare_scan(self):
		'''Movement sequence to safely place probe at beginning of scan

		   Parameters
		   ----------
		   None

		   Returns
		   -------
		   None
		   Writes details of scan to txt file for consumption by Scan_Weld.py
		   '''

		scan_ready = False

		if not self.validate_scan_params():
			print("Invalid scan parameters entered.  Program exited.")
			exit()

		b, z = self.get_b_z()

		set_ready_condition()
		mm = MachineMotionV2()

		retract_cylinder()
		sleep(0.5)  # Ensure the probe has left the part surface

		# @TODO: Once pneumatic actuator's position sensors are installed,
		#        remove the sleep command and replace it with a check of the
		#        actuator's retracted position sensor.  Once the retracted
		#        position sensor is on, the probe has left the surface of the
		#        part and the b axis can begin rotating.

		mm.setSpeed(self.b_axis_speed)
		mm.moveToPosition(axis=B_AXIS_DRIVE, position=B_SAFE_ANGLE)
		mm.waitForMotionCompletion(B_AXIS_DRIVE)

		mm.setSpeed(self.c_axis_speed)
		mm.moveToPosition(axis=C_AXIS_DRIVE, position=self.scan_start_c_angle)

		mm.setSpeed(self.z_axis_speed)
		mm.moveToPosition(axis=Z_AXIS_DRIVE, position=z)
		mm.waitForMotionCompletion(axis=C_AXIS_DRIVE)
		mm.waitForMotionCompletion(axis=Z_AXIS_DRIVE)

		mm.setSpeed(self.b_axis_speed)
		mm.moveToPosition(axis=B_AXIS_DRIVE, position=b)
		mm.waitForMotionCompletion(B_AXIS_DRIVE)

		scan_ready = extend_cylinder()

		# Send scan parameters
		with open('utilities/scan_config.txt', 'w') as cfg:
		    cfg.write(f"{self.scan_speed}\n{self.scan_accel}\n{self.scan_theta}"
		    		  f"\n{scan_ready}\n{self.weld_num}")

		print(f"In scan start position for WELD: {self.weld_num}.")
		print("Null instrument, then run Scan_Weld.py to scan the weld.")
