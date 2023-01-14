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
    

poz = [0,30,62,96,129]
width = 15

state = 0

b = [14,12,10,8,6]




#the idle animation with the orange lights before any input
wupc = 0
def warmup():
    global wupc
    wupc = wupc +0.04
    for n in range(72):
        cos = math.ceil((math.cos(wupc+(n/4))+1)*127)
        minicos = math.floor(cos*0.4)
        led_strip.set_rgb(n, cos,minicos,0)
        led_strip.set_rgb(143-n, cos,minicos,0)



#loading animation (green lines)
gr = 0
def greenload():
    global gr
    global state
    if gr == 0:
        for n in range(144):
            led_strip.set_rgb(n, 0,0,0)
    gr = gr + 1
    time.sleep(0.02)
    led_strip.set_rgb(gr, 0,200,0)
    led_strip.set_rgb(144-gr, 0,200,0)
    if gr > 73:
        state = 2


#WHEN FIRST LOADING; this function selects a new target button to press (0 - 4)
selected = 0
prevselected = 0



def releasecheck():
    released = 5
    for n in range(5):
        if ioe.input(b[n]) == 1:
            released = released-1
        if released == 0:
            return(True)
        
        

def fselect():
    global state
    global chosen 
    global selected
    global prevselected
    global width
    selected = random.randint(0, 4)
    if selected == prevselected:
        selected = random.randint(0, 4)
    if selected == prevselected:
        selected = random.randint(0, 4)
    for n in range(width):
        led_strip.set_rgb(n+(poz[selected]), 255,125,0)
    for n in range(0,poz[selected]):
        led_strip.set_rgb(n, 0,0,0)
    for n in range((poz[selected]+width),144):
        led_strip.set_rgb(n, 0,0,0)
    if releasecheck() == True:
        state = 3



def select():
    global state
    global chosen 
    global selected
    global prevselected
    global width
    randy = random.randint(1, 4)
    selected = (selected+randy)%5
    print(selected, "selected")
    for n in range(0,poz[selected]):
        led_strip.set_rgb(n, 0,0,0)
    for n in range((poz[selected]+width),144):
        led_strip.set_rgb(n, 0,0,0)
    if releasecheck() == True:
        state = 9

count = 0
def fplaying():
    global width
    global selected
    global count
    count = count+0.01
    br = math.ceil(((math.sin(count)+1)*100)+50)
    mbr = math.ceil(br/2)
    for n in range(width):
        led_strip.set_rgb(n+(poz[selected]), br,mbr,0)


def resflash(a):
    global count
    if count < 250:
        count = count +2
        if a == 1:
            for n in range(width):
                led_strip.set_rgb(n+(poz[selected]), 0,255-count,0)

        elif a == 2:
            for n in range(width):
                led_strip.set_rgb(n+(poz[selected]), 255-count,0,0)     
    elif releasecheck() == True:
        state = 8
        select()
   

            
target = 3
while True:
    if state == 0:
        warmup()
        for n in range(4):
            if (ioe.input(b[n]) == 0):
                state = 1
                print("let's go!")
                prevselected = n
    elif state == 1 and releasecheck() == True:
        greenload()
    elif state == 2 and releasecheck() == True:
        fselect()
    elif state == 3:
        fplaying()
        for n in range(5):
            if (ioe.input(b[n]) == 0):
                if n == selected:
                    print("good")
                    state = 4
                    count = 0 
                    for n in range(width):
                        led_strip.set_rgb(n+(poz[selected]), 0,255,0)

                else:
                    print("bad")
                    state = 5
                    count = 0 
                    for n in range(width):
                        led_strip.set_rgb(n+(poz[selected]), 255,0,0)



    elif state == 4 and releasecheck() == True:
        count = 0
        state = 6
    elif state == 5 and releasecheck() == True:
        count = 0
        state = 7
    elif state == 6: # good
        resflash(1)
    elif state == 7: # bad
        resflash(2)
    elif state == 9:
        fplaying()
        for n in range(5):
            if (ioe.input(b[n]) == 0):
                if n == selected:
                    print("good")
                    state = 4
                    count = 0 
                    for n in range(width):
                        led_strip.set_rgb(n+(poz[selected]), 0,255,0)

                else:
                    print("bad")
                    state = 5
                    count = 0 
                    for n in range(width):
                        led_strip.set_rgb(n+(poz[selected]), 255,0,0)


