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
CURRENT_TURN = 1
ACTIVE_TEAM = "HOME"

DIGIT_WIDTH = 24
DIGIT_HEIGHT = 30
DIGIT_THICKNESS = 4
DIGIT_TOP = 18
HOME_DIGIT_LEFT = 18
AWAY_DIGIT_LEFT = 86
DIVIDER_X = 63
TURN_TRACK_TOP = 54
TURN_START_X = 6
TURN_SPACING = 15

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
    segment_height = (DIGIT_HEIGHT // 2) - 1
    oled.fill_rect(x, y, DIGIT_THICKNESS, segment_height, 1)


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


def draw_team_header(label, x, active):
    if active:
        oled.rect(x - 2, 0, 32, 11, 1)
    oled.text(label, x, 2)


def draw_headers():
    draw_team_header("HOME", 8, ACTIVE_TEAM == "HOME")
    draw_team_header("AWAY", 88, ACTIVE_TEAM == "AWAY")
    oled.hline(0, 12, OLED_WIDTH, 1)
    oled.vline(DIVIDER_X, 14, 36, 1)


def draw_turn_track(current_turn):
    oled.hline(0, 50, OLED_WIDTH, 1)
    for turn in range(1, 9):
        x = TURN_START_X + (turn - 1) * TURN_SPACING
        if turn == current_turn:
            oled.fill_rect(x - 2, TURN_TRACK_TOP - 1, 10, 10, 1)
            oled.text(str(turn), x, TURN_TRACK_TOP, 0)
        else:
            oled.text(str(turn), x, TURN_TRACK_TOP, 1)


def draw_scoreboard(home_score, away_score, current_turn):
    oled.fill(0)
    draw_headers()
    draw_digit(HOME_DIGIT_LEFT, DIGIT_TOP, home_score)
    draw_digit(AWAY_DIGIT_LEFT, DIGIT_TOP, away_score)
    draw_turn_track(current_turn)
    oled.show()


print("bb-scoreboard OLED scoreboard test")
print("showing HOME={} AWAY={} TURN={}".format(HOME_SCORE, AWAY_SCORE, CURRENT_TURN))

draw_scoreboard(HOME_SCORE, AWAY_SCORE, CURRENT_TURN)

while True:
    sleep(REFRESH_DELAY_SECONDS)
