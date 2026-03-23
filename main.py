from machine import Pin
from time import sleep

# Suggested wiring for a 4-pin traffic light LED module on ESP32-S3:
# module GND -> board GND
# module R   -> GPIO6
# module Y   -> GPIO5
# module G   -> GPIO4

RED_PIN = 6
YELLOW_PIN = 5
GREEN_PIN = 4
STEP_DELAY_SECONDS = 2

red = Pin(RED_PIN, Pin.OUT, value=0)
yellow = Pin(YELLOW_PIN, Pin.OUT, value=0)
green = Pin(GREEN_PIN, Pin.OUT, value=0)

print("bb-scoreboard traffic light test")
print("cycling green -> yellow -> red every 2 seconds")

while True:
    red.off()
    yellow.off()
    green.on()
    print("green=ON yellow=OFF red=OFF")
    sleep(STEP_DELAY_SECONDS)

    red.off()
    green.off()
    yellow.on()
    print("green=OFF yellow=ON red=OFF")
    sleep(STEP_DELAY_SECONDS)

    yellow.off()
    green.off()
    red.on()
    print("green=OFF yellow=OFF red=ON")
    sleep(STEP_DELAY_SECONDS)
