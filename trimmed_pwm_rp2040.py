import time
import machine
from machine import Pin, PWM
import rp2

machine.freq(120000000) # set the CPU frequency to 240 MHz

m1pin1 = Pin(5)
m1pin2 = Pin(21)

m1pwm1 = PWM(m1pin1, freq=1000, duty_u16=0)
m1pwm2 = PWM(m1pin2, freq=1000, duty_u16=0)

LED = Pin(6, Pin.OUT)

max_duty = 65535 # constant

def m1Forward(dutyCycle):
    m1pwm1.duty_u16(dutyCycle)
    m1pwm2.duty_u16(0)

def m1Backward(dutyCycle):
    m1pwm1.duty_u16(0)
    m1pwm2.duty_u16(dutyCycle)

def allStop():
  # set all duty cycles to 0
  m1pwm1.duty_u16(0)
  m1pwm2.duty_u16(0)

def setup():
    m1pwm1.freq(1000)
    m1pwm2.freq(1000)

# setup()

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
