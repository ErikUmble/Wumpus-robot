import micropython
from machine import Pin
import time

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
            enc2dir = 1
        else:
            enc2dir = -1


enc1p1.irq(lambda pin: enc_pin_high(15), Pin.IRQ_RISING)
enc1p2.irq(lambda pin: enc_pin_high(25), Pin.IRQ_RISING)
enc2p1.irq(lambda pin: enc_pin_high(7), Pin.IRQ_RISING)
enc2p2.irq(lambda pin: enc_pin_high(27), Pin.IRQ_RISING)


# Similar setup for the second encoder pins if needed

while True:
    time.sleep(0.5)
    print(f'{enc1} {enc2}')
