import RPi.GPIO as GPIO
import pigpio
import time
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

# Note: camera coordinates: x starts at left side, y starts from top and goes down


# Capture an Image Directly from the Webcam:


def capture_image(ramp_frames=10, average_frames=10, file_name='null'):
    # Function to capture an image via webcam. Requires cv2, numpy, and os.
    # Optional Input Arguments:
    #       - ramp_frames is the number of frames to wait for the camera to calibrate
    #       - average_frames is the number of frames to average (effectively a low pass filter)
    #       - file_name is an argument that saves the image to a local file. If not specified then no image will be
    #         saved.
    # Output Arguments:
    #       - camera_capture is the averaged  image variable
    
    # Initialize the camera capture object with cv2.VideoCapture
    camera = cv2.VideoCapture(0)   # Default camera port is 0

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
    camera_capture = np.divide(camera_capture, average_frames)
    camera_capture = camera_capture.astype('uint8')     # Convert to integer
    
    if file_name != 'null':
        print("Saving Image File ...")
        path = os.curdir + '/'                  # Save in the current directory
        file_name = file_name + '.png'          # Default .png
        cv2.imwrite(path+file_name, camera_capture)

    return camera_capture

# Determine the Centroid of an Image


def find_centroid(img, level=240):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, level, 255, 0)
    if thresh.max() < 255:
        FLAME_DETECTED = 0
        cx = []
        cy = []
        EDGE_CROSSING = 0
    else:
        FLAME_DETECTED = 1
        contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[len(contours)-1]
        
        M = cv2.moments(cnt)
        if M['m00'] == 0:
            M['m00'] = thresh.sum()/255
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        cntx = cnt[:,0,0]
        cnty = cnt[:,0,1]

        EDGE_CROSSING = []
        if len(cntx[cntx <= 10]) > 5:
            EDGE_CROSSING.append(1)
            print 'Flame crosses Left Side of Image'
        if len(cntx[cntx >=630]) > 5:
            EDGE_CROSSING.append(2)
            print 'Flame crosses Right Side of Image'
        if len(cnty[cnty <= 10]) > 5:
            EDGE_CROSSING.append(3)
            print 'Flame crosses Top Side of Image'
        if len(cnty[cnty >= 470]) > 5:
            EDGE_CROSSING.append(4)
            print 'Flame crosses Bottom Side of Image'
            
    return FLAME_DETECTED, cx, cy, EDGE_CROSSING


def rotate_motor(direction, angle):
    # This function rotates the desired motor to the specified angle.
    # direction can either be pan or tilt
    # angle is an angle rotation in radians

    pi = pigpio.pi()

    if direction is not 'pan' and direction is not 'tilt':
        print 'Please choose either pan or tilt for the direction'
        exit()

    if angle < -math.pi / 2:
        print 'Reached lowest angle for ' + direction
        angle = -math.pi / 2
    elif angle > math.pi / 2:
        print 'Reached maximum angle for ' + direction
        angle = math.pi / 2

    if direction is 'pan':
        if angle <= 0:
            duty_cycle = (math.pi / 2 - abs(angle)) * 4.55 / (math.pi / 2) + 3.4
        else:
            duty_cycle = angle * (4.55 / (math.pi / 2)) + 7.95
        print 'the pan duty cycle is ' + str(duty_cycle) + '%'
    else:
        if angle <= 0:
            duty_cycle = (math.pi / 2 - abs(angle)) * 4.55 / (math.pi / 2) + 3.4
        else:
            duty_cycle = angle * (4.55 / (math.pi / 2)) + 7.95
        print 'the tilt duty cycle is ' + str(duty_cycle) + '%'

    if direction == 'pan':
        pi.hardware_PWM(13, 50, duty_cycle * 10000)
    else:
        pi.hardware_PWM(18, 50, duty_cycle * 10000)

    return angle


def center_target(pan_angle, tilt_angle, cx, cy, initial_rotation=3*math.pi/180, initial_gain=.0003):
    # This function commands the motors to adjust the camera until the centroid of the fire is brought to the center of
    # the image
    # pan_angle and tilt_angle indicate the current pan and tilt angles of the camera
    # initial_rotation indicates the angle by which the camera will rotate to calibrate its gains

    # The function returns 1 if successful, and 0 if unsuccessful

    # Define the image size
    x_max = 640
    y_max = 480

    mid_gain = .0005
    far_gain = .0007

    # Capture an initial image
    #img = capture_image()
    #flame, cx, cy = find_centroid(img)

    # Calculate how far the x and y coordinates of the centroid are from the center of the image
    x_offset = cx - float(x_max) / 2.0
    y_offset = cy - float(y_max) / 2.0

    print 'the x offset is ' + str(x_offset)
    print 'the y offset is ' + str(y_offset)

    # Define a tolerance of how close you want cx and cy to be to the center of the image (in pixels)
    tolerance = 3

    # Start targeting with initial angle change
    if abs(x_offset) > tolerance:
        if x_offset < 0:
            pan_angle = rotate_motor('pan', pan_angle - abs(x_offset) * initial_rotation)
        else:
            pan_angle = rotate_motor('pan', pan_angle + x_offset * initial_rotation)
    if abs(y_offset) > tolerance:
        if y_offset < 0:
            tilt_angle = rotate_motor('tilt', tilt_angle - abs(y_offset) * initial_rotation)
        else:
            tilt_angle = rotate_motor('tilt', tilt_angle + y_offset * initial_rotation)
    i = 1
    img = capture_image(3,3,'centerimage' + str(i))
    flame, cx, cy, edge_crossing = find_centroid(img)
    print 'cx is ' + str(cx)
    print 'cy is ' + str(cy)
    if not flame:
        print 'Lost flame after first rotation'
        exit()

    new_x_offset = cx - float(x_max) / 2.0
    new_y_offset = cy - float(y_max) / 2.0

    x_change = [new_x_offset - x_offset]
    y_change = [new_y_offset - y_offset]

    x_offset = new_x_offset
    y_offset = new_y_offset

    # Repeat this process, updating the gains every iteration, until convergence
    while abs(x_offset) > tolerance or abs(y_offset) > tolerance:
        while i <= 3:
            print 'the x offset is ' + str(x_offset)
            print 'the y offset is ' + str(y_offset)
            if abs(x_offset) > tolerance:
                if x_offset < 0:
                    rotate_motor('pan', pan_angle - abs(x_offset) * initial_gain)
                else:
                    rotate_motor('pan', pan_angle + x_offset * initial_gain)
            if abs(y_offset) > tolerance:
                if y_offset < 0:
                    rotate_motor('tilt', tilt_angle + abs(y_offset) * initial_gain)
                else:
                    rotate_motor('tilt', tilt_angle - y_offset * initial_gain)
            i = i + 1
            img = capture_image(3,3,'centerimage' + str(i))
            flame, cx, cy, edge_crossing = find_centroid(img)
            print 'cx is ' + str(cx)
            print 'cy is ' + str(cy)
            if not flame:
                print 'Flame lost'
                return 0

            new_x_offset = cx - float(x_max) / 2.0
            new_y_offset = cy - float(y_max) / 2.0

            x_change.append(new_x_offset - x_offset)
            y_change.append(new_y_offset - y_offset)

            x_offset = new_x_offset
            y_offset = new_y_offset

        ave_x_change = (abs(x_change[1]) + abs(x_change[2]) + abs(x_change[3]))/3
        ave_y_change = (abs(y_change[1]) + abs(y_change[2]) + abs(y_change[3]))/3

        if x_offset > 100 and y_offset > 100 and i == 4:
            if ave_x_change < 10 or ave_y_change < 10:
                print 'using far gain'
                gain = far_gain
            elif ave_ave_x_change < 30 or ave_y_change < 30:
                print 'using mid gain'
                gain = mid_gain
            else:
                gain = initial_gain
        else:
            gain = initial_gain
                
        print 'the x offset is ' + str(x_offset)
        print 'the y offset is ' + str(y_offset)
        if abs(x_offset) > tolerance:
            if x_offset < 0:
                rotate_motor('pan', pan_angle + abs(x_offset) * gain)
            else:
                rotate_motor('pan', pan_angle - x_offset * gain)
        if abs(y_offset) > tolerance:
            if y_offset < 0:
                rotate_motor('tilt', tilt_angle - abs(y_offset) * gain)
            else:
                rotate_motor('tilt', tilt_angle + y_offset * gain)
        i = i + 1
        img = capture_image(3,3,'centerimage' + str(i))
        flame, cx, cy, edge_crossing = find_centroid(img)
        print 'cx is ' + str(cx)
        print 'cy is ' + str(cy)
        if not flame:
            print 'Flame lost'
            return 0

        new_x_offset = cx - float(x_max) / 2.0
        new_y_offset = cy - float(y_max) / 2.0

        x_offset = new_x_offset
        y_offset = new_y_offset

    return 1


def spray_water(duration=5):
    # This function sprays the water fun at full power for a specified amount of time in seconds

    if duration < 0:
        print 'Cannot spray water for a negative amount time'
        exit()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, 1)
    time.sleep(duration)
    GPIO.output(27, 0)

    return
