import os

# all exposure constants go in this file

__is_on_rpi = os.uname()[4].startswith('arm')

HIGH_EXPOSURE = 1 if __is_on_rpi else 0
MEDIUM_EXPOSURE = 1 if __is_on_rpi else -5
LOW_EXPOSURE = 0 if __is_on_rpi else -10

AUTO_EXPOSURE_ON = 0.75 if __is_on_rpi else 1
AUTO_EXPOSURE_OFF = 0.25 if __is_on_rpi else 0