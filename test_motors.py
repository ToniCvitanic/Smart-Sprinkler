#Script to test motors
import SmartSprinklerModule as SSM
import math
import time

while 1:
    i = -math.pi / 2
    j = -math.pi / 2
    print 'testing pan'
    while i < math.pi / 2:
        SSM.rotate_motor('pan', i)
        i = i + 5 * math.pi / 180
        time.sleep(1)
    print 'testing tilt'
    while j < math.pi / 2:
        SSM.rotate_motor('tilt', j)
        j = j + 5 * math.pi / 180
        time.sleep(1)
