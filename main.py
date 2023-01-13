# Josh's reflex trainer.

import time 
import math 
import plasma 
import random
from plasma import plasma2040
from pimoroni_i2c import PimoroniI2C
from pimoroni import RGBLED, Analog
from breakout_ioexpander import BreakoutIOExpander
sense = Analog(plasma2040.CURRENT_SENSE, plasma2040.ADC_GAIN, plasma2040.SHUNT_RESISTOR)

numleds = 144
led_strip = plasma.WS2812(numleds, 0, 0, plasma2040.DAT)
led_strip.start()

PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}
i2c = PimoroniI2C(**PINS_PICO_EXPLORER)
ioe = BreakoutIOExpander(i2c, address=0x18)

for i in range(14):
    ioe.set_mode(i+1, BreakoutIOExpander.PIN_IN_PU)
    


poz = [0,26,62,98,134]
width = 8

state = 0

wupc = 0
def warmup():
    global wupc
    wupc = wupc +0.04
    for n in range(72):
        cos = math.ceil((math.cos(wupc+(n/4))+1)*127)
        minicos = math.floor(cos*0.4)
        led_strip.set_rgb(n, cos,minicos,0)
        led_strip.set_rgb(143-n, cos,minicos,0)
        
target = 3
while True:
    warmup()

        
