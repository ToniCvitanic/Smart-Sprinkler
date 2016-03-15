import pigpio
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

    if angle <= 0:
        duty_cycle = (math.pi / 2 - abs(angle)) * 5.5 / (math.pi / 2) + 2
    else:
        duty_cycle = angle * (5.5 / (math.pi / 2)) + 7.5
    print 'the duty cycle is ' + str(duty_cycle) + '%'

    if direction == 'pan':
        pigpio.hardware_PWM(17, 50, duty_cycle * 10000)
        channel = 17
    else:
        pigpio.hardware_PWM(178, 50, duty_cycle * 10000)
        channel = 18

    return angle
