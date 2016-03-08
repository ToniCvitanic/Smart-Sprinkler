import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import pylab
import SmartSprinklerModule as ssm
import math

def Pix2PT(x,y,Po,To):
    # Calculate approximate pan and tilt to center on pixel (x,y), where (0,0)
    # is the upper right corner of the image.

    # Hardcoded camera specs:
    fov = 25*math.pi/180
    w = 640
    h = 480

    d = 0.5*math.sqrt(w*w+h*h)/math.tan(fov/2)
    t = w/2-x

    P = Po + math.atan(t/d)*180/math.pi
    T = To + math.atan((h/2-y)/math.sqrt(d*d+t*t))*180/math.pi

    return P,T

print Pix2PT(0,240,0,0)
print Pix2PT(640,240,0,0)
print Pix2PT(320,0,0,0)
print Pix2PT(320,480,0,0)

#img = cv2.imread('farflame.png',0)
#img = ssm.capture_image()

#FLAME_DETECTED,cx,cy = ssm.find_centroid(img)

#if FLAME_DETECTED:
#    print "Flame Detected"
#else:
#    print "No Flame Detected"
#
#imgplot = plt.imshow(img,cmap='gray',hold='true')
#plt.plot(cx,cy,marker='o',color='r')
#pylab.ylim([0,480]),pylab.xlim([0,640])
#plt.show()
