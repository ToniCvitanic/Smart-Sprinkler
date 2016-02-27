import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

p = GPIO.PWM(18,50)

p.start(1)
print '1% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(2)
print '2% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(3)
print '3% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(4)
print '4% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(5)
print '5% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(6)
print '6% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(7)
print '7% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(8)
print '8% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(9)
print '9% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(10)
print '10% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(11)
print '11% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(12)
print '12% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(13)
print '13% duty cycle'
time.sleep(3)
p.ChangeDutyCycle(14)
print '14% duty cycle'
time.sleep(3)
p.stop()