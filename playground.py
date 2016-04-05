import cv2
import numpy as np
import matplotlib.pyplot as plt
import SmartSprinklerModule as ssm

#im = cv2.imread('farflame.png')
#im = cv2.imread('closeflame.png')
#im = cv2.imread('edgypic.png')
#im = cv2.imread('centerimage1.png')
#im = cv2.imread('centerimage6.png')

im = cv2.imread('middletest.png')
#im = cv2.imread('edgetest.png')
#im = cv2.imread('goodtest.png')

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,240,255,0)
contours,hierarchy = cv2.findContours(thresh,1,2)
cnt = contours[len(contours)-1]

AL = cv2.arcLength(cnt,True)
FLAME,cx,cy,EDGE = ssm.find_centroid(im,200)

print EDGE

if EDGE[0] == 4:
    idx = cnt[cnt[:,0,0]>=470,0,1]
    L = max(idx)-min(idx)
else:
    print 'test another edge!!!!!'

# Inequalities based on geometric perimeter comparisons
### NOT WORKING STILL!
if L*3.14159/2 < 1*(AL-L):
    print 'Our approximation of the centroid is good enough'
else:
    if EDGE[0]==4:
        cy = 480
    print 'Our approximation of the centroid isn"t good enough'

imgplot = plt.imshow(im,cmap='gray')
cv2.drawContours(im,contours,-1,(0,255,0),3)
plt.plot(cx,cy,marker='o',color='r')
plt.show()

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
