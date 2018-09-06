# Requirements
import random, time, ugfx
from machine import Neopix
from tilda import Buttons, LED, Sensors
from utime import sleep_ms

# Lights
n = Neopix()

# Graphics
ugfx.init()
ugfx.orientation(270)

# Controls for Lights: Enable / Disable
enable = False

def set_enable(new_enable):
    print('Lights Enabled: ', new_enable)
    global enable
    enable = new_enable

Buttons.enable_interrupt(Buttons.BTN_A,lambda enable:set_enable(True),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_B,lambda disable:set_enable(False),on_press=True)

# Controls for Lights: Slower / Faster
speed = 1024

def faster():
    global speed
    speed = int(speed / 2)
    if speed < 1:
        speed = 1
    print('LESS Delay: ', speed)

Buttons.enable_interrupt(Buttons.JOY_Up,lambda speed:faster(),on_press=True)
Buttons.enable_interrupt(Buttons.JOY_Right,lambda speed:faster(),on_press=True)

def slower():
    global speed
    speed = int(speed * 2)
    if speed > 65536:
        speed = 65536
    print('MORE Delay: ', speed)

Buttons.enable_interrupt(Buttons.JOY_Down,lambda speed:slower(),on_press=True)
Buttons.enable_interrupt(Buttons.JOY_Left,lambda speed:slower(),on_press=True)

# Controls for Graphics: Artwork Selection
def new_art(art):
    print('Loading Art: ', art)
    ugfx.clear(ugfx.BLACK)
    ugfx.display_image(0,0,str(art)+'.png')
    global timer
    timer = time.time()

Buttons.enable_interrupt(Buttons.BTN_1,lambda art:new_art(1),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_2,lambda art:new_art(2),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_3,lambda art:new_art(3),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_4,lambda art:new_art(4),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_5,lambda art:new_art(5),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_6,lambda art:new_art(6),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_7,lambda art:new_art(7),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_8,lambda art:new_art(8),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_9,lambda art:new_art(9),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_0,lambda art:new_art(10),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_Star,lambda art:new_art(11),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_Hash,lambda art:new_art(12),on_press=True)
Buttons.enable_interrupt(Buttons.BTN_Menu,lambda art:new_art(random.randint(1,12)),on_press=True)

# RNG Seed / Random Art on Boot
random.seed( int( Sensors.get_tmp_temperature() + Sensors.get_hdc_temperature() + Sensors.get_hdc_humidity() + Sensors.get_lux() ) )
new_art(random.randint(1,12))

# Main Loop
while True:

    sleep_ms(speed)
    if enable:
        LED(LED.GREEN).toggle()
    else:
        LED(LED.GREEN).off()

    sleep_ms(speed)
    if enable:
        n.display( [ 0, random.randrange( 0x000000, 0xFFFFFF ) ] )
    else:
        n.display( [ 0, 0 ] )

    sleep_ms(speed)
    if enable:
        LED(LED.RED).toggle()
    else:
        LED(LED.RED).off()

    sleep_ms(speed)
    if enable:
        n.display( [ random.randrange( 0x000000, 0xFFFFFF ), 0 ] )
    else:
        n.display( [ 0, 0 ] )

    # Change Art every 60 seconds
    if timer + 60 < time.time():
        new_art(random.randint(1,12))