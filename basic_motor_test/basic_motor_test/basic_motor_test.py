import time
from machine import Pin

m1pin1 = Pin(21, Pin.OUT)
m1pin2 = Pin(5, Pin.OUT)
m2pin1 = Pin(18, Pin.OUT)
m2pin2 = Pin(17, Pin.OUT)

LED = Pin(6, Pin.OUT)

def m1Forward():
    m1pin1.on()
    m1pin2.off()

def m1Backward():
    m1pin1.off()
    m1pin2.on()

def m2Forward():
    m2pin1.on()
    m2pin2.off()

def m2Backward():
    m2pin1.off()
    m2pin2.on()

def allStop():
    m1pin1.off()
    m1pin2.off()
    m2pin1.off()
    m2pin2.off()

while True:
    allStop()
    time.sleep(2)
    m1Forward()
    time.sleep(2)
    m1Backward()
    time.sleep(2)
    m2Forward()
    time.sleep(2)
    m2Backward()
    time.sleep(2)
