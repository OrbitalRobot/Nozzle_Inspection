import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from Weld_Scan import *


# Constants
z_park_speed = 30
b_park_speed = 15
c_park_speed = 15

mm = MachineMotionV2()

retract_cylinder()
sleep(0.5)

mm.setSpeed(z_park_speed)
mm.moveToPosition(axis=Z_AXIS_DRIVE, position=0)
mm.waitForMotionCompletion(axis=Z_AXIS_DRIVE)

mm.setSpeed(b_park_speed)
mm.moveToPosition(axis=B_AXIS_DRIVE, position=0)

mm.setSpeed(c_park_speed)
mm.moveToPosition(axis=C_AXIS_DRIVE, position=0)
mm.waitForMotionCompletion(C_AXIS_DRIVE)
