import pigpio
import RPi.GPIO as GPIO
pi = pigpio.pi()
pi.hardware_PWM(13, 50, 0)
pi.hardware_PWM(18, 50, 0)
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, 0)

