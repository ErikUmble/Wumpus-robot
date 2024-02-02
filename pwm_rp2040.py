import time
from machine import Pin, PWM

m1pin1 = Pin(21, Pin.OUT)
m1pin2 = Pin(5, Pin.OUT)
m2pin1 = Pin(18, Pin.OUT)
m2pin2 = Pin(17, Pin.OUT)

m1pwm1 = PWM(m1pin1, freq=1000, duty_u16=0)
m1pwm2 = PWM(m1pin2, freq=1000, duty_u16=0)
m2pwm1 = PWM(m2pin1, freq=1000, duty_u16=0)
m2pwm2 = PWM(m2pin2, freq=1000, duty_u16=0)


stdFreq = 1000 # operating frequency (unvarying)
slow = 18 # slow speed
turn = 20 # turn speed

max_duty = 65535 # constant


# scale motor 2's duty cycle by a constant to adjust for differences
# in hardware between the two motors
m2_scale = 1.0232;

def calc_duty(duty_100):
    return int(duty_100 / 100 * max_duty)

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
    m1pwm1.freq(1000)
    m1pwm2.freq(1000)
    m2pwm1.freq(1000)
    m2pwm2.freq(1000)

# setup()

while True:
    # time.sleep(5)
    m1Forward(50)
    '''time.sleep_ms(2000)

    m1Forward(50)
    time.sleep_ms(2000)

    m1Backward(100)
    time.sleep_ms(2000)

    m1Backward(50)
    time.sleep_ms(2000)

    allStop()

    m2Forward(100)
    time.sleep_ms(2000)

    m2Forward(50)
    time.sleep_ms(2000)

    m2Backward(100)
    time.sleep_ms(2000)

    m2Forward(50)
    time.sleep_ms(2000)

    allStop()'''





