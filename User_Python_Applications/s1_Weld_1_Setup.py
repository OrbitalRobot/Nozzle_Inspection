import sys
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
from Weld_Scan import *


WELD = 1

setup_parameters = {
	'b_axis_speed': 10,  # deg/sec
	'c_axis_speed': 25,  # deg/sec
	'z_axis_speed': 80   # mm/sec
}

scan_parameters = {
	'scan_speed':		   15,	# deg/sec
	'scan_accel':		   1,	# deg/sec^2
	"scan_start_c_angle":  0,  # deg
	'scan_end_c_angle':    400	# deg
}


ws = Weld_Scan(weld_num=WELD,
			setup_params=setup_parameters,
			scan_params=scan_parameters)

ws.prepare_scan()
