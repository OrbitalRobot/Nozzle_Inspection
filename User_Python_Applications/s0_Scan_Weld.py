import sys
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from Default_Axes_Config import *
from Pneumatics import *


mm = MachineMotionV2()

# Get scan paremters
with open('utilities/scan_config.txt', 'r') as cfg:
    lines = cfg.readlines()
    lines = [line.rstrip() for line in lines]
scan_speed = int(lines[0])
scan_accel = int(lines[1])
scan_theta = int(lines[2])
scan_ready = bool(lines[3])
weld = lines[4]

if scan_ready:
	prev_accel = mm.getAxisMaxAcceleration(axis=C_AXIS_DRIVE)
	mm.setSpeed(speed=scan_speed)
	mm.setAxisMaxAcceleration(axis=C_AXIS_DRIVE, acceleration=scan_accel)
	mm.moveRelative(axis=C_AXIS_DRIVE, distance=scan_theta)
	mm.waitForMotionCompletion()
	mm.setAxisMaxAcceleration(axis=C_AXIS_DRIVE, acceleration=prev_accel)
else:
	print("Scan not ready.  Run Weld_(#)_Setup.py to move to the correct weld.")

scan_complete = retract_cylinder()

if scan_complete:
	print(f"Scan of weld {weld} complete.")
else:
	print("Cylinder failed to retract at end of scan.")

# Clear config file so scan_ready variable must be set by running Weld_#_Setup.py
with open('utilities/scan_config.txt', 'w') as cfg:
    cfg.write("")
