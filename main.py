from machine import Pin
from time import sleep

# Suggested wiring for a 4-pin traffic light LED module on ESP32-S3:
# module GND -> board GND
# module R   -> GPIO6
# module Y   -> GPIO5
# module G   -> GPIO4
#
# Suggested wiring for a 5-pin button module:
# module GND -> board GND
# module K1  -> GPIO7
# module K2  -> GPIO15
# module K3  -> GPIO16
# module K4  -> GPIO17
#
# The button inputs use internal pull-ups, so each input reads:
# 1 when not pressed
# 0 when pressed

RED_PIN = 6
YELLOW_PIN = 5
GREEN_PIN = 4
K1_PIN = 7
K2_PIN = 15
K3_PIN = 16
K4_PIN = 17
POLL_DELAY_SECONDS = 0.05

red = Pin(RED_PIN, Pin.OUT, value=0)
yellow = Pin(YELLOW_PIN, Pin.OUT, value=0)
green = Pin(GREEN_PIN, Pin.OUT, value=0)
k1 = Pin(K1_PIN, Pin.IN, Pin.PULL_UP)
k2 = Pin(K2_PIN, Pin.IN, Pin.PULL_UP)
k3 = Pin(K3_PIN, Pin.IN, Pin.PULL_UP)
k4 = Pin(K4_PIN, Pin.IN, Pin.PULL_UP)


def set_leds(red_on, yellow_on, green_on):
    red.value(1 if red_on else 0)
    yellow.value(1 if yellow_on else 0)
    green.value(1 if green_on else 0)


print("bb-scoreboard traffic light button test")
print("K1=red K2=yellow K3=green K4=all")
set_leds(False, False, False)

while True:
    if k4.value() == 0:
        set_leds(True, True, True)
        print("K4 pressed -> red=ON yellow=ON green=ON")
    elif k1.value() == 0:
        set_leds(True, False, False)
        print("K1 pressed -> red=ON yellow=OFF green=OFF")
    elif k2.value() == 0:
        set_leds(False, True, False)
        print("K2 pressed -> red=OFF yellow=ON green=OFF")
    elif k3.value() == 0:
        set_leds(False, False, True)
        print("K3 pressed -> red=OFF yellow=OFF green=ON")
    else:
        set_leds(False, False, False)

    sleep(POLL_DELAY_SECONDS)
