import pigpio
pi = pigpio.pi()
pi.hardware_PWM(13, 50, 0)
pi.hardware_PWM(18, 50, 0)

