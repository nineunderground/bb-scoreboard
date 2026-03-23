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

red = Pin(RED_PIN, Pin.OUT, value=0)
yellow = Pin(YELLOW_PIN, Pin.OUT, value=0)
green = Pin(GREEN_PIN, Pin.OUT, value=1)

print("bb-scoreboard traffic light test")
print("red=OFF yellow=OFF green=ON")

while True:
    sleep(1)
