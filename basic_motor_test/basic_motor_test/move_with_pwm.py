import time
'''import machine
from machine import Pin, PWM
import rp2

machine.freq(100000000) # set the CPU frequency to 240 MHz

print('starting')

m1pin1 = Pin(21)
m1pin2 = Pin(5)
m2pin1 = Pin(18)
m2pin2 = Pin(17)

m1pwm1 = PWM(m1pin1, freq=1000, duty_u16=0)
m1pwm2 = PWM(m1pin2, freq=1000, duty_u16=0)
m2pwm1 = PWM(m2pin1, freq=1000, duty_u16=0)
m2pwm2 = PWM(m2pin2, freq=1000, duty_u16=0)

LED = Pin(6, Pin.OUT)'''

while True:
    # print(f'm1pwm1: {m1pwm1.duty_u16()}, m1pwm2: {m1pwm2.duty_u16()}, m2pwm1: {m2pwm1.duty_u16()}, m2pwm2: {m2pwm2.duty_u16()}')
    time.sleep(2)
