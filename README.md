# **Nozzle_Inspection**
This was a professional project to develop an automated inspection system for performing eddy current array testing on rocket nozzles in production.  A more complete and sophisticated system was being developed by a vendor, but it was behind schedule.  So NDT's engineering leadership requested a rapidly protoyped system to be developed to facilitate inspection R&D for them until the final system arrived.

In this project are the Python programs that run the nozzle inspection machine designed in-house using Vention's cloud-based CAD and programmed using their MachineMotion API.  The end-of-arm-tooling was also designed in-house and machined by Protolabs.  It allows the probe to rotate about its center to ensure the probe is always parallel to the surface it is scanning.


## **System Description**
A nozzle will be placed (aft-end-down) over the top of the vertical axis and sit on the 4 white rest pads at the ends of the four legs.  Then this machine will place the eddy current array probe (the black and orange padded object held by the end-of-arm-tooling) against the inside of the nozzle, and rotate the probe around the circumference of the nozzle to inspect it.  The inspection will be performed at various heights on the nozzle.  The nozzle is not shown for IP/ITAR reasons.

![image](https://user-images.githubusercontent.com/121198760/209497766-6d0bfe8c-3236-4e58-9490-4b7d51a4118d.png)

![image](https://user-images.githubusercontent.com/121198760/209497883-f1877358-11c3-4d75-a0fc-0efd4a56191a.png)

![image](https://user-images.githubusercontent.com/121198760/209498160-bec2c17f-4dc9-4783-bd69-d24dcea80d99.png)


The eddy current probe is mounted to the a pneumatic actuator to press it against the inside of the nozzle while scanning.  This direction in which the pneumatic actuator extends is considered the x-axis of the machine.

The pneumatic actuator is mounted to a turntable that is rotated by the motor to the right of it.  This rotation is considered to be around the y-axis, and is therefore referred to as b, adhering to the Translate X-Y-Z / Rotate A-B-C convention commonly used for industrial robots.

This turntable is mounted to the carriage of the large vertical ballscrew actuator that is the z-axis.  At the top of the z-axis, a vertically oriented motor is mounted to facilitate raising and lowering the carriage of the z-axis.

The base of the z-axis is mounted to a second turntable which rotates about the vertical, making it the c-axis.  This turntable is rotated by a motor mounted to the underside of the machine.
