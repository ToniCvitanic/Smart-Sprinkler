import RPi.GPIO as GPIO
import math
import time


def rotate_motor(motor, angle):
    # This function rotates the desired motor to the specified angle.
    # motor can either be 1 or 2
    # angle is an angle rotation in radians

    if angle < 0 or angle > math.pi:
        print 'please choose an angle between 0 and pi'
        exit()

    GPIO.setmode(GPIO.BCM)
    if motor == 1:
        GPIO.setup(17, GPIO.OUT)
        channel = 17
    elif motor == 2:
        GPIO.setup(18, GPIO.OUT)
        channel = 18
    else:
        print 'Please select either 1 or 2 for the motor parameter'
        exit()
    
    duty_cycle = angle * 13 / math.pi
    print 'the duty cycle is ' + str(duty_cycle) + '%'

    p = GPIO.PWM(channel, 50)
    p.start(angle * 13 / math.pi)
    time.sleep(1)
    p.stop()

    return angle
