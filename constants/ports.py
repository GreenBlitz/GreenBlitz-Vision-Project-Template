import os

# all ports constants go in this file

__is_on_rpi = os.uname()[4].startswith('arm')

CAMERA_PORT = 0 if __is_on_rpi else 1
