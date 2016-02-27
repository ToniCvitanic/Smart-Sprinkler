import pigpio
import time

pi = pigpio.pi()
pi.hardware_PWM(18, 50, 10000)
print '1% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 20000)
print '2% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 30000)
print '3% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 40000)
print '4% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 50000)
print '5% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 60000)
print '6% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 70000)
print '7% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 80000)
print '8% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 90000)
print '9% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 100000)
print '10% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 110000)
print '11% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 120000)
print '12% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 130000)
print '13% duty cycle'
time.sleep(3)
pi.hardware_PWM(18, 50, 140000)
print '14% duty cycle'
time.sleep(3)