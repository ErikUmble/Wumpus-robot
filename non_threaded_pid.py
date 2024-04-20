import time
import rp2
import machine
from machine import Pin, PWM
import _thread
from rotary_irq_rp2 import RotaryIRQ

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

saturated_duty = 16000 # choice for max speed

turn90ticks = 115
turn_error = 10

enc_max_value = 20000

kp = 0.8
ki = 0.08
kd = 0.04

encpins = (15, 25, 7, 27)

enc1p1 = Pin(encpins[0], Pin.IN)
enc1p2 = Pin(encpins[1], Pin.IN)
enc2p1 = Pin(encpins[2], Pin.IN)
enc2p2 = Pin(encpins[3], Pin.IN)

enc1 = 0
enc2 = 0
enc1dir = 1
enc2dir = 1

def enc_pin_high(pin):
    global enc1dir
    global enc2dir
    global enc1
    global enc2
    if pin == encpins[0] or pin == encpins[1]:
        if enc1p1.value() == 1 and enc1p2.value() == 1:
            enc1 += 1 * enc1dir
        elif enc1p1.value() == 1:
            enc1dir = 1
        else:
            enc1dir = -1
    if pin == encpins[2] or pin == encpins[3]:
        if enc2p1.value() == 1 and enc2p2.value() == 1:
            enc2 += 1 * enc2dir
        elif enc2p1.value() == 1:
            enc2dir = -1
        else:
            enc2dir = 1


enc1p1.irq(lambda pin: enc_pin_high(15), Pin.IRQ_RISING)
enc1p2.irq(lambda pin: enc_pin_high(25), Pin.IRQ_RISING)
enc2p1.irq(lambda pin: enc_pin_high(7), Pin.IRQ_RISING)
enc2p2.irq(lambda pin: enc_pin_high(27), Pin.IRQ_RISING)

def calc_duty(duty_100):
    return int(duty_100 * max_duty / 100)

def m1Forward(dutyCycle):
    m1pwm1.duty_u16(min(calc_duty(dutyCycle), saturated_duty))
    m1pwm2.duty_u16(0)

def m1Backward(dutyCycle):
    m1pwm1.duty_u16(0)
    m1pwm2.duty_u16(min(calc_duty(dutyCycle), saturated_duty))

def m1Signed(dutyCycle):
    if dutyCycle >= 0:
        m1Forward(dutyCycle)
    else:
        m1Backward(-dutyCycle)

def m2Forward(dutyCycle):
    m2pwm1.duty_u16(min(calc_duty(dutyCycle), saturated_duty))
    m2pwm2.duty_u16(0)

def m2Backward(dutyCycle):
    m2pwm1.duty_u16(0)
    m2pwm2.duty_u16(min(calc_duty(dutyCycle), saturated_duty))

def m2Signed(dutyCycle):
    if dutyCycle >= 0:
        m2Forward(dutyCycle)
    else:
        m2Backward(-dutyCycle)

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

def ccw():
    global enc1
    global enc2
    enc1 = 0
    enc2 = 0
    m1_integral = 0
    m2_integral = 0
    period = 1/10
    m1_last_error = None
    m2_last_error = None
    while abs(enc1 - turn90ticks) > turn_error or abs(enc2 + turn90ticks) > turn_error:
        m1_current_error = turn90ticks - enc1
        m2_current_error = -turn90ticks - enc2
        m1_integral += m1_current_error * period
        m2_integral += m2_current_error * period
        m1_derivative = 0
        if not m1_last_error is None:
            m1_derivative = (m1_current_error - m1_last_error) / period
        m2_derivative = 0
        if not m2_last_error is None:
            m2_derivative = (m2_current_error - m2_last_error) / period
        m1Signed(kp * m1_current_error + ki * m1_integral + kd * m1_derivative)
        m2Signed(kp * m2_current_error + ki * m2_integral + kd * m2_derivative)
        m1_last_error = m1_current_error
        m2_last_error = m2_current_error
        print(f'{enc1} {enc2} {m1_current_error} {m2_current_error} {m1_integral} {m2_integral}')
        time.sleep(period)

setup()

while True:
    LED.off()
    ccw()
    LED.on()
    allStop()
    time.sleep(5)
