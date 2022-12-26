from MachineMotion import *
class Axis:
  '''Handles the parameters of an axis.

  Parameters
  ----------
  See the configServo function from the MachineMotion class for details.

  Returns
  -------
  None
  '''

  def __init__(self, drive, mechGain, direction, motorCurrent=10.0,
              tuningProfile=TUNING_PROFILES.DEFAULT, parentDrive=None,
              motorSize=MOTOR_SIZE.LARGE, brake=BRAKE.NONE, max_speed=10,
              max_accel=5):
    self.drive = drive
    self.mechGain = mechGain
    self.direction = direction
    self.motorCurrent = motorCurrent
    self.tuningProfile = tuningProfile
    self.parentDrive = parentDrive
    self.motorSize = motorSize
    self.brake = brake
    self.max_speed = max_speed
    self.max_accel = max_accel
