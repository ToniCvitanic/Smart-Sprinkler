import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

# Capture an Image Directly from the Webcam:
def capture_image(ramp_frames=10, average_frames=10, file_name='null'):
    # Function to capture an image via webcam. Requires cv2, numpy, and os.
    # Optional Input Arguments:
    #       - ramp_frames is the number of frames to wait for the camera to calibrate
    #       - average_frames is the number of frames to average (effectively a low pass filter)
    #       - file_name is an argument that saves the image to a local file. If not specified then no image will be saved.
    # Output Arguments:
    #       - camera_capture is the averaged  image variable
    
    # Initialize the camera capture object with cv2.VideoCapture
    camera = cv2.VideoCapture(0)    # Default camera port is 0

    # Function to capture a single image from the camera and return it as a .pil
    def get_image():
        retval, im = camera.read()
        return im

    # Ramp the camera - frames to be discarded; only used for calibration if necessary
    for i in xrange(ramp_frames):
        temp = get_image()
    print("Taking Image ...")
    
    # The image we'll keep is the average of #average_frames:
    camera_capture = get_image()
    for i in xrange(average_frames-1):
        camera_capture = camera_capture.astype(float) + get_image()
    camera_capture = np.divide(camera_capture,average_frames)
    camera_capture = camera_capture.astype('uint8')     # Convert to integer
    
    if file_name != 'null':
        print("Saving Image File ...")
        path = os.curdir + '/'                  # Save in the current directory
        file_name = file_name + '.png'          # Default .png
        cv2.imwrite(path+file_name,camera_capture)

    return camera_capture

# Determine the Centroid of an Image
def find_centroid(img,level=240):
    ret,thresh = cv2.threshold(img,level,255,0)
    if thresh.max() < 255:
        FLAME_DETECTED = 0
        cx = []
        cy = []
    else:
        FLAME_DETECTED = 1
        contours,hierarchy = cv2.findContours(thresh,1,2)
        M = cv2.moments(contours[len(contours)-1])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    return(FLAME_DETECTED,cx,cy)

