import sys
from time import sleep
sys.path.append("/var/lib/cloud9/vention-control/python-api")
sys.path.append("/var/lib/cloud9/User_Python_Applications/utilities")
import urllib.parse
from MachineMotion import *


mm = MachineMotionV2()

print("------------------------------\nChecking pin states...\n")
pins = (0, 1, 2, 3)

for pin in pins:
	current_state = mm.digitalRead(deviceNetworkId=1, pin=pin)
	print(f"Pin #{pin} state: {current_state}")

sleep(1)

print("------------------------------\nSetting pin states...\n")
mm.digitalWrite(deviceNetworkId=1, pin=0, value=0)
mm.digitalWrite(deviceNetworkId=1, pin=2, value=1)
print(f"Pin 0 should be 0")
print(f"Pin 2 should be 1")

sleep(5)

print("------------------------------\nChecking pin states...\n")
pins = (0, 1, 2, 3)

for pin in pins:
	current_state = mm.digitalRead(deviceNetworkId=1, pin=pin)
	print(f"Pin #{pin} state: {current_state}")

sleep(1)

print("------------------------------\nSetting pin states...\n")
mm.digitalWrite(deviceNetworkId=1, pin=0, value=1)
mm.digitalWrite(deviceNetworkId=1, pin=2, value=0)
print(f"Pin 0 should be 1")
print(f"Pin 2 should be 0")

sleep(5)

print("------------------------------\nChecking pin states...\n")
pins = (0, 1, 2, 3)

for pin in pins:
	current_state = mm.digitalRead(deviceNetworkId=1, pin=pin)
	print(f"Pin #{pin} state: {current_state}")
