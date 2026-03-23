from machine import I2C, Pin
from time import sleep

from ssd1306 import SSD1306_I2C

# JMDO 96C-1 OLED module (I2C):
# module VCC -> board 3V3
# module GND -> board GND
# module SCL -> GPIO8
# module SDA -> GPIO9

OLED_SCL_PIN = 8
OLED_SDA_PIN = 9
OLED_WIDTH = 128
OLED_HEIGHT = 64
OLED_I2C_ADDR = 0x3C
REFRESH_DELAY_SECONDS = 1

HOME_SCORE = 2
AWAY_SCORE = 7

DIGIT_WIDTH = 24
DIGIT_HEIGHT = 38
DIGIT_THICKNESS = 4
DIGIT_TOP = 20
HOME_DIGIT_LEFT = 18
AWAY_DIGIT_LEFT = 86
DIVIDER_X = 63

SEGMENTS = {
    "0": (1, 1, 1, 1, 1, 1, 0),
    "1": (0, 1, 1, 0, 0, 0, 0),
    "2": (1, 1, 0, 1, 1, 0, 1),
    "3": (1, 1, 1, 1, 0, 0, 1),
    "4": (0, 1, 1, 0, 0, 1, 1),
    "5": (1, 0, 1, 1, 0, 1, 1),
    "6": (1, 0, 1, 1, 1, 1, 1),
    "7": (1, 1, 1, 0, 0, 0, 0),
    "8": (1, 1, 1, 1, 1, 1, 1),
    "9": (1, 1, 1, 1, 0, 1, 1),
}

i2c = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=400000)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_I2C_ADDR)


def draw_horizontal_segment(x, y):
    oled.fill_rect(x, y, DIGIT_WIDTH, DIGIT_THICKNESS, 1)


def draw_vertical_segment(x, y):
    oled.fill_rect(x, y, DIGIT_THICKNESS, DIGIT_HEIGHT // 2, 1)


def draw_digit(x, y, value):
    a, b, c, d, e, f, g = SEGMENTS[str(value)]
    middle_y = y + (DIGIT_HEIGHT // 2) - (DIGIT_THICKNESS // 2)
    bottom_y = y + DIGIT_HEIGHT - DIGIT_THICKNESS
    right_x = x + DIGIT_WIDTH - DIGIT_THICKNESS

    if a:
        draw_horizontal_segment(x, y)
    if b:
        draw_vertical_segment(right_x, y)
    if c:
        draw_vertical_segment(right_x, middle_y)
    if d:
        draw_horizontal_segment(x, bottom_y)
    if e:
        draw_vertical_segment(x, middle_y)
    if f:
        draw_vertical_segment(x, y)
    if g:
        draw_horizontal_segment(x, middle_y)


def draw_headers():
    oled.text("HOME", 8, 2)
    oled.text("AWAY", 88, 2)
    oled.hline(0, 12, OLED_WIDTH, 1)
    oled.vline(DIVIDER_X, 14, OLED_HEIGHT - 14, 1)


def draw_scoreboard(home_score, away_score):
    oled.fill(0)
    draw_headers()
    draw_digit(HOME_DIGIT_LEFT, DIGIT_TOP, home_score)
    draw_digit(AWAY_DIGIT_LEFT, DIGIT_TOP, away_score)
    oled.show()


print("bb-scoreboard OLED scoreboard test")
print("showing HOME={} AWAY={}".format(HOME_SCORE, AWAY_SCORE))

draw_scoreboard(HOME_SCORE, AWAY_SCORE)

while True:
    sleep(REFRESH_DELAY_SECONDS)
