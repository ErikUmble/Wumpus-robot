import time
import rp2
import machine
from machine import Pin, PWM

machine.freq(100000000) # set the CPU frequency to 240 MHz

m1pin1 = Pin(21)
m1pin2 = Pin(4)
m2pin1 = Pin(18)
m2pin2 = Pin(17)

m1pwm1 = PWM(m1pin1)
m1pwm2 = PWM(m1pin2)
m2pwm1 = PWM(m2pin1)
m2pwm2 = PWM(m2pin2)

LED = Pin(6, Pin.OUT)
max_duty = 65535 # constant

def calc_duty(duty_100):
    return int(duty_100 * max_duty / 100)

def m1Forward(dutyCycle):
    m1pwm1.duty_u16(calc_duty(dutyCycle))
    m1pwm2.duty_u16(0)

def m1Backward(dutyCycle):
    m1pwm1.duty_u16(0)
    m1pwm2.duty_u16(calc_duty(dutyCycle))

def m2Forward(dutyCycle):
    m2pwm1.duty_u16(calc_duty(dutyCycle))
    m2pwm2.duty_u16(0)

def m2Backward(dutyCycle):
    m2pwm1.duty_u16(0)
    m2pwm2.duty_u16(calc_duty(dutyCycle))


def allStop():
  # set all duty cycles to 0
  m1pwm1.duty_u16(0)
  m1pwm2.duty_u16(0)
  m2pwm1.duty_u16(0)
  m2pwm2.duty_u16(0)

def setup():
    # initialize frequencies
    m1pwm1.freq(1000)
    m1pwm2.freq(1000)
    m2pwm1.freq(1000)
    m2pwm2.freq(1000)

setup()

while True:
    allStop()
    LED.off()
    time.sleep(2)
    LED.on()
    time.sleep(2)
    LED.off()
    print('turning m1 forward')
    m1Forward(100)
    time.sleep_ms(2000)

    m1Forward(50)
    time.sleep_ms(2000)

    m1Backward(100)
    time.sleep_ms(2000)

    m1Backward(50)
    time.sleep_ms(2000)

    allStop()

    print('turning m2 forward')

    m2Forward(100)
    time.sleep_ms(2000)

    m2Forward(50)
    time.sleep_ms(2000)

    m2Backward(100)
    time.sleep_ms(2000)

    m2Backward(50)
    time.sleep_ms(2000)

    allStop()





