from machine import Pin
from time import sleep

try:
    led = Pin("LED", Pin.OUT)
except Exception:
    # Common built-in LED pin on many ESP32-S3 dev boards.
    led = Pin(48, Pin.OUT)

print("bb-scoreboard hello world")
print("MicroPython firmware booted successfully")

counter = 0
while True:
    led.on()
    print("hello from ESP32-S3, tick=%d" % counter)
    sleep(0.5)
    led.off()
    sleep(0.5)
    counter += 1
