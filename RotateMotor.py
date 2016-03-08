import RPi.GPIO as GPIO
import math
import time


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
