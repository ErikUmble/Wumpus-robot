from machine import Pin
import Encoder


enc1 = Encoder(25, 15)
enc2 = Encoder(7, 27)

while True:
    # print(f'{enc1p1.value()} {enc1p2.value()} {enc2p1.value()} {enc2p2.value()}')
    print(f'{enc1.read()} {enc2.read()}')
