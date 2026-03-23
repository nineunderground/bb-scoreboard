from machine import I2C, Pin
from time import sleep

from ssd1306 import SSD1306_I2C

# Traffic light LED module:
# module GND -> board GND
# module R   -> GPIO6
# module Y   -> GPIO5
# module G   -> GPIO4
#
# Button module:
# module GND -> board GND
# module K1  -> GPIO7
# module K2  -> GPIO15
# module K3  -> GPIO16
# module K4  -> GPIO17
#
# JMDO 96C-1 OLED module (I2C):
# module VCC -> board 3V3
# module GND -> board GND
# module SCL -> GPIO8
# module SDA -> GPIO9
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
OLED_SCL_PIN = 8
OLED_SDA_PIN = 9
OLED_WIDTH = 128
OLED_HEIGHT = 64
OLED_I2C_ADDR = 0x3C
POLL_DELAY_SECONDS = 0.05

STATE_NONE = "NONE"
STATE_RED = "RED"
STATE_YELLOW = "YELLOW"
STATE_GREEN = "GREEN"
STATE_ALL = "ALL"

red = Pin(RED_PIN, Pin.OUT, value=0)
yellow = Pin(YELLOW_PIN, Pin.OUT, value=0)
green = Pin(GREEN_PIN, Pin.OUT, value=0)
k1 = Pin(K1_PIN, Pin.IN, Pin.PULL_UP)
k2 = Pin(K2_PIN, Pin.IN, Pin.PULL_UP)
k3 = Pin(K3_PIN, Pin.IN, Pin.PULL_UP)
k4 = Pin(K4_PIN, Pin.IN, Pin.PULL_UP)

i2c = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=400000)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_I2C_ADDR)


def set_leds(red_on, yellow_on, green_on):
    red.value(1 if red_on else 0)
    yellow.value(1 if yellow_on else 0)
    green.value(1 if green_on else 0)


def show_status(state):
    oled.fill(0)
    oled.text("BB SCOREBOARD", 0, 0)
    oled.text("LED STATUS:", 0, 16)
    oled.text(state, 0, 32)
    oled.show()


def read_state():
    if k4.value() == 0:
        return STATE_ALL
    if k1.value() == 0:
        return STATE_RED
    if k2.value() == 0:
        return STATE_YELLOW
    if k3.value() == 0:
        return STATE_GREEN
    return STATE_NONE


def apply_state(state):
    if state == STATE_ALL:
        set_leds(True, True, True)
    elif state == STATE_RED:
        set_leds(True, False, False)
    elif state == STATE_YELLOW:
        set_leds(False, True, False)
    elif state == STATE_GREEN:
        set_leds(False, False, True)
    else:
        set_leds(False, False, False)


print("bb-scoreboard traffic light button test")
print("K1=red K2=yellow K3=green K4=all")
print("OLED shows NONE/RED/YELLOW/GREEN/ALL")

last_state = None

while True:
    state = read_state()
    if state != last_state:
        apply_state(state)
        show_status(state)
        print("state={}".format(state))
        last_state = state

    sleep(POLL_DELAY_SECONDS)
