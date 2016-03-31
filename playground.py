import cv2
import numpy as np
import matplotlib.pyplot as plt

#im = cv2.imread('farflame.png')
#im = cv2.imread('closeflame.png')
#im = cv2.imread('testing.png')
im = cv2.imread('edgypic.png')

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray,240,255,0)
contours,hierarchy = cv2.findContours(thresh,1,2)

cnt = contours[len(contours)-1]
cntx = cnt[:,0,0]
cnty = cnt[:,0,1]

print cntx[cntx<=15]
print cntx[cntx>=625]
print cnty[cnty<=15]
print cnty[cnty>=465]



imgplot = plt.imshow(im,cmap='gray')
cv2.drawContours(im,contours,-1,(0,255,0),3)
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
