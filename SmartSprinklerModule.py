import RPi.GPIO as GPIO
import time
import math
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
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, level, 255, 0)
    if thresh.max() < 255:
        FLAME_DETECTED = 0
        cx = []
        cy = []
    else:
        FLAME_DETECTED = 1
        contours, hierarchy = cv2.findContours(thresh, 1, 2)
        M = cv2.moments(contours[len(contours)-1])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    return FLAME_DETECTED, cx, cy


def rotate_motor(direction, angle):
    # This function rotates the desired motor to the specified angle.
    # direction can either be pan or tilt
    # angle is an angle rotation in radians

    if direction is not 'pan' and direction is not 'tilt':
        print 'Please choose either pan or tilt for the direction'
        exit()

    if angle < -math.pi / 2:
        print 'Reached lowest angle for ' + direction
        angle = -math.pi / 2
    elif angle > math.pi / 2:
        print 'Reached maximum angle for ' + direction
        angle = math.pi / 2

    GPIO.setmode(GPIO.BCM)
    if direction == 'pan':
        GPIO.setup(17, GPIO.OUT)
        channel = 17
    else:
        GPIO.setup(18, GPIO.OUT)
        channel = 18

    if angle <= 0:
        duty_cycle = (math.pi / 2 - abs(angle)) * 5.5 / (math.pi / 2) + 2
    else:
        duty_cycle = angle * (5.5 / (math.pi / 2)) + 7.5
    print 'the duty cycle is ' + str(duty_cycle) + '%'

    p = GPIO.PWM(channel, 50)
    p.start(duty_cycle)
    time.sleep(1)
    p.stop()

    return angle


def center_target(pan_angle, tilt_angle, initial_rotation=.09):
    # This function commands the motors to adjust the camera until the centroid of the fire is brought to the center of
    # the image
    # pan_angle and tilt_angle indicate the current pan and tilt angles of the camera
    # initial_rotation indicates the angle by which the camera will rotate to calibrate its gains

    # The function returns 1 if successful, and 0 if unsuccessful

    # Define the image size
    x_max = 480
    y_max = 640

    # Capture an initial image
    img = capture_image()
    flame, cx, cy = find_centroid(img)

    # Calculate how far the x and y coordinates of the centroid are from the center of the image
    x_offset = float(x_max) / 2.0 - cx
    y_offset = float(y_max) / 2.0 - cy

    # Define a tolerance of how close you want cx and cy to be to the center of the image (in pixels)
    tolerance = 3

    # Do an initial rotation to calibrate gains
    if abs(x_offset) > tolerance:
        if x_offset < 0:
            pan_angle = rotate_motor('pan', pan_angle + initial_rotation)
        else:
            pan_angle = rotate_motor('pan', pan_angle - initial_rotation)
    if abs(y_offset) > tolerance:
        if y_offset < 0:
            tilt_angle = rotate_motor('tilt', tilt_angle + initial_rotation)
        else:
            tilt_angle = rotate_motor('tilt', tilt_angle - initial_rotation)

    img = capture_image()
    flame, cx, cy = find_centroid(img)
    if not flame:
        print 'Fire no longer detected after small angle change. Either the camera is too close to the fire, or the' \
              ' fire has gone out'
        exit()

    new_x_offset = float(x_max) / 2.0 - cx
    new_y_offset = float(y_max) / 2.0 - cy

    # Calculate gains. Gains refer to how far the camera moved versus how many pixels the centroid coordinates changed
    # by.
    x_change = new_x_offset - x_offset
    y_change = new_y_offset - y_offset
    if x_change == 0 or y_change == 0:
        print('The initial turret rotation is too small. Please choose a larger initial rotation.')
        exit()

    x_gain = initial_rotation / abs(x_change)
    y_gain = initial_rotation / abs(y_change)

    # Repeat this process, updating the gains every iteration, until convergence
    while abs(x_offset) > tolerance or abs(y_offset) > tolerance:
        if abs(x_offset) > tolerance:
            if x_offset < 0:
                rotate_motor('pan', pan_angle + abs(x_offset) * x_gain)
            else:
                rotate_motor('pan', pan_angle - x_offset * x_gain)
        if abs(y_offset) > tolerance:
            if y_offset < 0:
                rotate_motor('tilt', tilt_angle + abs(y_offset) * y_gain)
            else:
                rotate_motor('tilt', tilt_angle - y_offset * y_gain)

        img = capture_image()
        flame, cx, cy = find_centroid(img)
        if not flame:
            print 'Flame lost'
            return 0

        new_x_offset = float(x_max) / 2.0 - cx
        new_y_offset = float(y_max) / 2.0 - cy

        x_change = new_x_offset - x_offset
        y_change = new_y_offset - y_offset

        if x_change == 0 or y_change == 0:
            print 'The gain is too small. Consider adding higher proportional or integral gains'
            exit()

        x_gain = abs(x_offset * x_gain) / abs(x_change)
        y_gain = abs(y_offset * y_gain) / abs(y_change)

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
