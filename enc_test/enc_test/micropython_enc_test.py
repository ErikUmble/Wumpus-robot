import machine
from machine import Pin
from rotary_irq_rp2 import RotaryIRQ

machine.freq(100000000) # set the CPU frequency to 240 MHz

enc1p1 = Pin(25)
enc1p2 = Pin(15)
enc2p1 = Pin(7)
enc2p2 = Pin(27)
enc1 = RotaryIRQ(
    pin_num_clk=15,
    pin_num_dt=25,
    min_val=0,
    max_val=20000,
    incr=1,
    reverse=False,
    range_mode=RotaryIRQ.RANGE_UNBOUNDED,
    pull_up=True,
    half_step=False,
    invert=False)

enc2 = RotaryIRQ(
    pin_num_clk=27,
    pin_num_dt=7,
    min_val=0,
    max_val=20000,
    incr=1,
    reverse=False,
    range_mode=RotaryIRQ.RANGE_UNBOUNDED,
    pull_up=True,
    half_step=False,
    invert=False)


while True:
    # print(f'{enc1p1.value()} {enc1p2.value()} {enc2p1.value()} {enc2p2.value()}')
    print(f'{enc1.value()} {enc2.value()}')
