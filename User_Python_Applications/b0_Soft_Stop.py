import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from Weld_Scan import *


# Constants
C_STOP_ACCEL = 3
B_STOP_ACCEL = 5
Z_STOP_ACCEL = 5


soft_stop_rates = [[C_AXIS_DRIVE, C_STOP_ACCEL],
                  [B_AXIS_DRIVE, B_STOP_ACCEL],
                  [Z_AXIS_DRIVE, Z_STOP_ACCEL]]

mm = MachineMotionV2()

for axis, rate in soft_stop_rates:
    mm.stopMoveContinuous(axis=axis, accel=rate)

for axis in soft_stop_rates:
    mm.waitForMotionCompletion(axis)
