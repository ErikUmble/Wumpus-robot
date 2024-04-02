from machine import Pin
from rotary_irq_rp2 import RotaryIRQ

enc1p1 = Pin(25)
enc1p2 = Pin(15)
enc2p1 = Pin(7)
enc2p2 = Pin(27)

enc1 = RotaryIRQ(pin_num_clk=25,
              pin_num_dt=15,
              min_val=0,
              max_val=20000,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)


enc2 = RotaryIRQ(pin_num_clk=7,
            pin_num_dt=27,
            min_val=0,
            max_val=20000,
            reverse=False,
            range_mode=RotaryIRQ.RANGE_WRAP)


while True:
    # print(f'{enc1p1.value()} {enc1p2.value()} {enc2p1.value()} {enc2p2.value()}')
    print(f'{enc1.value()} {enc2.value()}')
