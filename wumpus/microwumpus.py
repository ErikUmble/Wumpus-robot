
import time 
from machine import Pin #RP2040 Recognizes this library
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

OK_ERROR = 30.0

#Variables for speed control:
slow = 45
medium = 60
turnProportion = 0.05 #Turn speed
maxDuty = 70
intProportion = 0.0025 #Constant for P in PID
maxIntPower = 300

block_Delay = 1200
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
#scentCharacteristic 