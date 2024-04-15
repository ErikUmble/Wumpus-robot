
import time 
from machine import Pin #RP2040 Recognizes this library
from machine import ADC
from rotary_irq_rp2 import RotaryIRQ
import bluetooth
from ble_advertising import advertising_payload

m1pin1 = Pin(9, Pin.OUT) #D9 GPIO
m1pin2 = Pin(10, Pin.OUT)

enc1 = RotaryIRQ(pin_num_clk=25,
              pin_num_dt=15,
              min_val=0,
              max_val=20000,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)

enc1pin1 = Pin(2)
enc1pin2 = Pin(3)

m2pin1 = Pin(6, Pin.OUT)
m2pin2 = Pin(5, Pin.OUT)

enc2 = RotaryIRQ(pin_num_clk=7,
            pin_num_dt=27,
            min_val=0,
            max_val=20000,
            reverse=False,
            range_mode=RotaryIRQ.RANGE_WRAP)

enc2pin1 = Pin(11)
enc2pin2 = Pin(21)

ir1pin = Pin(28)
ir2pin = Pin(29)
adc_ir1 = ADC(ir1pin)
adc_ir2 = ADC(ir2pin)

OK_ERROR = 30.0

#Variables for speed control:
slow = 45
medium = 60
turnProportion = 0.05 #Turn speed
maxDuty = 70
intProportion = 0.0025 #Constant for P in PID
maxIntPower = 300

block_Delay = 1.2
#The two motors aren't ^exactly^ identical, they need a
#small correcting factor if they're going to run at the same speed  
m2_scale = 1.0403

# number of encoder ticks in one block
ticksAfterLine = 950

# number of encoder ticks in each wheel
# to turn 90 degrees
turn90ticks = 600

#This is about the point where I'm not very confident with the adaptation:
nanoBotService = bluetooth.UUID(0x180A) #Unique bluetooth service ID
#BLE Characteristic for transmitting scent - custom 128-bit UUID, read and writable by central
scentCharacteristic = bluetooth.UUID(0x2A57) #Need to include BLERead and BLEWrite args
#central = bluetooth() #Attempt at BLEdevice instantiation

def ir_left():
#returns true if the left infrared sensor detects white
    ir1_val = adc_ir1.read_u16()
    return ir1_val < (1023/2)

def ir_right():
#returns true if the left infrared sensor detects white
    ir2_val = adc_ir2.read_u16()
    return ir2_val < (1023/2)

def m1Forward( dutyCycle):
    if (dutyCycle >= maxDuty):
        analogWrite(m1pin1, maxDuty)
        analogWrite(m1pin2, 0)
    else:
        analogWrite(m1pin1, dutyCycle)
        analogWrite(m1pin2, 0)    

def m1Backward( dutyCycle):
    if (dutyCycle >= maxDuty):
        analogWrite(m1pin1, 0)
        analogWrite(m1pin2, maxDuty)
    else:
        analogWrite(m1pin1, 0)
        analogWrite(m1pin2, dutyCycle)

def m2Forward(dutyCycle):
    if (dutyCycle * m2_scale >= maxDuty):
        analogWrite(m2pin1, maxDuty)
        analogWrite(m2pin2, 0)
    else:
        analogWrite(m2pin1, dutyCycle * m2_scale)
        analogWrite(m2pin2, 0)

def m2Backward(dutyCycle):
    if (dutyCycle * m2_scale >= maxDuty):
        analogWrite(m2pin1, 0)
        analogWrite(m2pin2, dutyCycle * m2_scale)

def m1SignedDirection(dutyCycle):
    if(dutyCycle > 0):
        m1Forward(dutyCycle)
    else:
        m1Backward(-1*dutyCycle)
def AllForward(dutyCycle):
    m1Forward(dutyCycle)
    m2Forward(dutyCycle)

def AllBackward(dutyCycle):
    m1Backward(dutyCycle)
    m2Backward(dutyCycle)  

def AllStop():
    analogWrite(m1pin1,0)
    analogWrite(m1pin2,0)
    analogWrite(m2pin1,0)
    analogWrite(m2pin2,0)      

def move_forward():
    #This version calls many of the functions written above, but also calls rot_ccw, rot_cw, and forwardTicks
    #move forward and then make corrections until both sensors detect white at the same time
    white_left = False
    white_right = False
    left_time = 0
    right_time = 0
    error_threshold_ms = 20
    while (True):
        count = 0
        AllForward(slow)
        while( not white_left or not white_right):
            count += 1
            time.sleep(0.001) #Delays for 1ms
            if (not white_left and ir_left()):
                white_left = True
                left_time = count
            if (not white_left and ir_right()):
                white_right = True 
                right_time = count   
        AllStop()    
        if (abs(left_time - right_time) < error_threshold_ms):
            break 
        #Back-up and rotate to correct angle offset
        AllBackward(medium)
        time.sleep(0.5)
        AllStop()

        if(left_time < right_time):
             rot_ccw(right_time - left_time)
        else: 
            rot_cw( (left_time - right_time)*2 )
            white_left = False
            white_right = False
            left_time = 0
            right_time = 0
        forwardTicks(slow, ticksAfterLine)
        time.sleep(block_Delay*0.5) 
        AllStop()         
