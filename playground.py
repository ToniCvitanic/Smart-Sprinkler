import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab
import SmartSprinklerModule as ssm

#img = cv2.imread('farflame.png',0)
img = ssm.capture_image()

FLAME_DETECTED,cx,cy = ssm.find_centroid(img)

if FLAME_DETECTED:
    print "Flame Detected"
else:
    print "No Flame Detected"

imgplot = plt.imshow(img,cmap='gray',hold='true')
plt.plot(cx,cy,marker='o',color='r')
pylab.ylim([0,480]),pylab.xlim([0,640])
plt.show()
