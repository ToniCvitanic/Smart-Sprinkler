#Script to test the tilt motor
import SmartSprinklerModule as SSM
import math
import time

i = -math.pi / 2 + 15 * math.pi / 180
while 1:
    SSM.rotate_motor('tilt', i)
    i = i + 1 * math.pi / 180
    time.sleep(1)
    if i > math.pi / 2:
        i = -math.pi / 2 + 15 * math.pi / 180
