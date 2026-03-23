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
# module K1  -> GPIO7   (increase turn)
# module K2  -> GPIO15  (increase HOME score)
# module K3  -> GPIO16  (increase AWAY score)
# module K4  -> GPIO17  (reset scores and turn)
#
# JMDO 96C-1 OLED module (I2C):
# module VCC -> board 3V3
# module GND -> board GND
# module SCL -> GPIO8
# module SDA -> GPIO9

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

TURN_MIN = 1
TURN_MAX = 8
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

red = Pin(RED_PIN, Pin.OUT, value=0)
yellow = Pin(YELLOW_PIN, Pin.OUT, value=0)
green = Pin(GREEN_PIN, Pin.OUT, value=0)
k1 = Pin(K1_PIN, Pin.IN, Pin.PULL_UP)
k2 = Pin(K2_PIN, Pin.IN, Pin.PULL_UP)
k3 = Pin(K3_PIN, Pin.IN, Pin.PULL_UP)
k4 = Pin(K4_PIN, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(OLED_SCL_PIN), sda=Pin(OLED_SDA_PIN), freq=400000)
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_I2C_ADDR)

home_score = 0
away_score = 0
current_turn = 1
active_team = "HOME"

last_k1 = 1
last_k2 = 1
last_k3 = 1
last_k4 = 1


def set_leds(red_on, yellow_on, green_on):
    red.value(1 if red_on else 0)
    yellow.value(1 if yellow_on else 0)
    green.value(1 if green_on else 0)


# HOME uses red, AWAY uses green, any unexpected state falls back to yellow.
def update_active_team_led(team):
    if team == "HOME":
        set_leds(True, False, False)
    elif team == "AWAY":
        set_leds(False, False, True)
    else:
        set_leds(False, True, False)


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


def draw_headers(team):
    draw_team_header("HOME", 8, team == "HOME")
    draw_team_header("AWAY", 88, team == "AWAY")
    oled.hline(0, 12, OLED_WIDTH, 1)
    oled.vline(DIVIDER_X, 14, 36, 1)


def draw_turn_track(turn):
    oled.hline(0, 50, OLED_WIDTH, 1)
    for value in range(TURN_MIN, TURN_MAX + 1):
        x = TURN_START_X + (value - 1) * TURN_SPACING
        if value == turn:
            oled.fill_rect(x - 2, TURN_TRACK_TOP - 1, 10, 10, 1)
            oled.text(str(value), x, TURN_TRACK_TOP, 0)
        else:
            oled.text(str(value), x, TURN_TRACK_TOP, 1)


def draw_scoreboard():
    oled.fill(0)
    draw_headers(active_team)
    draw_digit(HOME_DIGIT_LEFT, DIGIT_TOP, home_score % 10)
    draw_digit(AWAY_DIGIT_LEFT, DIGIT_TOP, away_score % 10)
    draw_turn_track(current_turn)
    oled.show()


def refresh_outputs():
    update_active_team_led(active_team)
    draw_scoreboard()
    print(
        "HOME={} AWAY={} TURN={} ACTIVE={}".format(
            home_score, away_score, current_turn, active_team
        )
    )


def toggle_active_team():
    global active_team
    if active_team == "HOME":
        active_team = "AWAY"
    else:
        active_team = "HOME"


def handle_turn_button():
    global current_turn
    current_turn += 1
    if current_turn > TURN_MAX:
        current_turn = TURN_MIN
    toggle_active_team()


def handle_home_button():
    global home_score
    home_score = (home_score + 1) % 10


def handle_away_button():
    global away_score
    away_score = (away_score + 1) % 10


def handle_reset_button():
    global home_score, away_score, current_turn, active_team
    home_score = 0
    away_score = 0
    current_turn = 1
    active_team = "HOME"


print("bb-scoreboard interactive scoreboard test")
print("K1=turn K2=HOME+1 K3=AWAY+1 K4=reset")

refresh_outputs()

while True:
    current_k1 = k1.value()
    current_k2 = k2.value()
    current_k3 = k3.value()
    current_k4 = k4.value()
    changed = False

    if last_k1 == 1 and current_k1 == 0:
        handle_turn_button()
        changed = True
    if last_k2 == 1 and current_k2 == 0:
        handle_home_button()
        changed = True
    if last_k3 == 1 and current_k3 == 0:
        handle_away_button()
        changed = True
    if last_k4 == 1 and current_k4 == 0:
        handle_reset_button()
        changed = True

    last_k1 = current_k1
    last_k2 = current_k2
    last_k3 = current_k3
    last_k4 = current_k4

    if changed:
        refresh_outputs()

    sleep(POLL_DELAY_SECONDS)
