#Script to test the pan motor
import SmartSprinklerModule as SSM
import math
import time

i = -math.pi / 2
while 1:
    SSM.rotate_motor('pan', i)
    i = i + 5 * math.pi / 180
    time.sleep(1)
    if i > math.pi / 2:
        i = -math.pi / 2
