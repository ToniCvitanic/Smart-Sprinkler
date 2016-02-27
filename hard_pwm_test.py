import pigpio
import time

pi = pigpio.pi()
pi.hardware_PWM(18, 50, 100000)
print '10% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 200000)
print '20% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 300000)
print '30% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 400000)
print '40% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 500000)
print '50% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 600000)
print '60% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 700000)
print '70% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 800000)
print '80% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 900000)
print '90% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 1000000)
print '100% duty cycle'
time.sleep(3)
