# bb-scoreboard

Minimal ESP32-S3 MicroPython test project for bringing up the board and confirming that flashing works.

This project uses Python for both:

- the host-side tooling in a dedicated virtual environment
- the application code running on the ESP32-S3 through MicroPython

The example does two things:

- prints a hello-world message to the serial console at 115200 baud
- drives a 4-pin traffic-light LED module from a 4-button input module

## Project layout

  bb-scoreboard/
  |- .gitignore
  |- main.py
  |- README.md
  `- requirements.txt

## Hardware

This project targets an ESP32-S3 DevKit style board.

Use the UART / COM USB port for flashing. On your Windows host that is currently COM6.

## OLED Driver Source

The earlier `micropython/micropython` raw URL returned `404 Not Found`. Use this working public source instead:

    https://raw.githubusercontent.com/stlehmann/micropython-ssd1306/master/ssd1306.py

Download it into the project directory with:

    wget https://raw.githubusercontent.com/stlehmann/micropython-ssd1306/master/ssd1306.py -O ssd1306.py

License note:

- This MicroPython SSD1306 driver is MIT-licensed.
- Keep the copyright and license notice that comes with the downloaded `ssd1306.py` file.

## Full Pin Diagram

This full diagram matches the official ESP32-S3-DevKitC-1 v1.1 J1 and J3 header layout from Espressif. If your board silkscreen differs, follow the board silkscreen over this README.

Top view, USB connectors at the top:

    Left header J1                          Right header J3
    ---------------------------             ---------------------------
    3V3                                   GND
    3V3                                   TX  (GPIO43, U0TXD)
    RST                                   RX  (GPIO44, U0RXD)
    GPIO4                                 GPIO1
    GPIO5                                 GPIO2
    GPIO6                                 GPIO42
    GPIO7                                 GPIO41
    GPIO15                                GPIO40
    GPIO16                                GPIO39
    GPIO17                                GPIO38
    GPIO18                                GPIO37
    GPIO8                                 GPIO36
    GPIO3                                 GPIO35
    GPIO46                                GPIO0
    GPIO9                                 GPIO45
    GPIO10                                GPIO48
    GPIO11                                GPIO47
    GPIO12                                GPIO21
    GPIO13                                GPIO20  (USB D+)
    GPIO14                                GPIO19  (USB D-)
    5V                                    GND
    GND                                   GND

Traffic-light pins used by this project:

    Module GND -> J1 GND
    Module R   -> J1 GPIO6
    Module Y   -> J1 GPIO5
    Module G   -> J1 GPIO4

Button-module pins used by this project:

    Module GND -> J3 GND
    Module K1  -> J1 GPIO7
    Module K2  -> J1 GPIO15
    Module K3  -> J1 GPIO16
    Module K4  -> J1 GPIO17

OLED-module pins used by this project:

    Module VCC -> J1 3V3
    Module GND -> J3 GND
    Module SCL -> J1 GPIO8
    Module SDA -> J1 GPIO9

Notes:

- Many 0.96 inch 4-pin OLED modules label the clock pin as `SCL`, but some silkscreens are blurry and can look like `SDL` or `SDI`. For this setup, that pin is the I2C clock line and goes to GPIO8.
- GPIO38 is the on-board RGB LED on ESP32-S3-DevKitC-1 v1.1 according to Espressif.
- On boards using ESP32-S3-WROOM-2, GPIO35, GPIO36, and GPIO37 may be reserved for internal flash/PSRAM use and not available externally.
- The button inputs are configured with internal pull-ups, so each button line is normally high and goes low when pressed.

If flashing fails, force bootloader mode:

1. Hold BOOT
2. Press and release RESET
3. Release BOOT
4. Retry the command

## Wiring

The current `main.py` expects this wiring:

- traffic-light module GND -> ESP32-S3 GND
- traffic-light module R -> ESP32-S3 GPIO6
- traffic-light module Y -> ESP32-S3 GPIO5
- traffic-light module G -> ESP32-S3 GPIO4
- button module GND -> ESP32-S3 GND
- button module K1 -> ESP32-S3 GPIO7
- button module K2 -> ESP32-S3 GPIO15
- button module K3 -> ESP32-S3 GPIO16
- button module K4 -> ESP32-S3 GPIO17
- OLED module VCC -> ESP32-S3 3V3
- OLED module GND -> ESP32-S3 GND
- OLED module SCL -> ESP32-S3 GPIO8
- OLED module SDA -> ESP32-S3 GPIO9

Behavior:

- no button pressed -> all LEDs off
- K1 pressed -> red LED on
- K2 pressed -> yellow LED on
- K3 pressed -> green LED on
- K4 pressed -> all LEDs on
- the OLED shows `NONE`, `RED`, `YELLOW`, `GREEN`, or `ALL` to match the current LED state

If more than one button is pressed at the same time, the code gives priority in this order: `K4`, `K1`, `K2`, `K3`.

ASCII wiring diagram:

    Traffic light module                 ESP32-S3 DevKit
    --------------------                 ----------------
    [ GND ] ---------------------------> [ GND ]
    [ R   ] ---------------------------> [ GPIO6 ]
    [ Y   ] ---------------------------> [ GPIO5 ]
    [ G   ] ---------------------------> [ GPIO4 ]

    Button module                        ESP32-S3 DevKit
    -------------                        ----------------
    [ GND ] ---------------------------> [ GND ]
    [ K1  ] ---------------------------> [ GPIO7 ]
    [ K2  ] ---------------------------> [ GPIO15 ]
    [ K3  ] ---------------------------> [ GPIO16 ]
    [ K4  ] ---------------------------> [ GPIO17 ]

    OLED module                          ESP32-S3 DevKit
    -----------                          ----------------
    [ VCC ] ---------------------------> [ 3V3 ]
    [ GND ] ---------------------------> [ GND ]
    [ SCL ] ---------------------------> [ GPIO8 ]
    [ SDA ] ---------------------------> [ GPIO9 ]

Pin summary:

    Module pin   ESP32-S3 pin   Purpose
    ----------   -------------   -------
    LED GND      GND             Ground
    R            GPIO6           Red LED control
    Y            GPIO5           Yellow LED control
    G            GPIO4           Green LED control
    BTN GND      GND             Button module ground
    K1           GPIO7           Red button input
    K2           GPIO15          Yellow button input
    K3           GPIO16          Green button input
    K4           GPIO17          All-on button input
    OLED VCC     3V3             OLED power
    OLED GND     GND             OLED ground
    OLED SCL     GPIO8           I2C clock
    OLED SDA     GPIO9           I2C data

Notes:

- This assumes the button module is a simple shared-ground key module where each K pin is shorted to GND when pressed.
- If the LEDs behave inverted, the LED module may be active-low and the logic in `main.py` should be inverted.
- If the button module outputs high when pressed instead of low when pressed, the input logic in `main.py` should also be inverted.
- If the OLED stays blank, common fixes are checking the `SCL` and `SDA` wiring, verifying `3V3` power, and trying I2C address `0x3D` instead of `0x3C` in `main.py`.
- If the traffic-light module is just bare LEDs and resistors are not onboard, add a 220-330 ohm resistor in series with each color line.

## Flash and run from Windows

### 1. Create a dedicated Python environment

Open PowerShell on the Windows machine and create a virtual environment inside the project:

    cd C:\path\to\bb-scoreboard
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -U pip
    python -m pip install -r requirements.txt

If py is not available, replace the venv creation command with:

    python -m venv .venv

After activation, every command below should run from that same PowerShell session.

### 2. Download MicroPython firmware for ESP32-S3

Official download page:

    https://micropython.org/download/ESP32_GENERIC_S3/

Current stable generic ESP32-S3 firmware on that page as of 2026-03-23:

    https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251209-v1.27.0.bin

Save the downloaded file somewhere accessible on your Windows host, for example:

    wget https://micropython.org/resources/firmware/ESP32_GENERIC_S3-20251209-v1.27.0.bin -o ESP32_GENERIC_S3-20251209-v1.27.0.bin 

### 3. Erase and flash the MicroPython runtime to COM6

    # Check the serial port, e.g. COM6
    Get-WmiObject Win32_PnPEntity | Where-Object { $_.Name -like "*SERIAL*" } | Select-Object Name

    python -m esptool --chip esp32s3 --port COM6 erase-flash
    python -m esptool --chip esp32s3 --port COM6 --baud 460800 write-flash -z 0 ESP32_GENERIC_S3-20251209-v1.27.0.bin

### 4. Upload Python files to the board

From the project directory on the Windows host, use a short delay after connecting before the filesystem copy:

    mpremote connect COM6 sleep 1 fs cp .\main.py :main.py
    mpremote connect COM6 sleep 1 fs cp .\ssd1306.py :ssd1306.py

### 5. Reset the board and open the serial console

    mpremote connect COM6 reset
    mpremote connect COM6 repl

You should see lines like:

    bb-scoreboard traffic light button test
    K1=red K2=yellow K3=green K4=all

Exit the REPL with Ctrl+].

### 6. Next time you work on the board

Open PowerShell in the project and reactivate the environment:

    cd C:\path\to\bb-scoreboard
    .\.venv\Scripts\Activate.ps1

Then upload the updated script again:

    mpremote connect COM6 sleep 1 fs cp .\main.py :main.py
    mpremote connect COM6 sleep 1 fs cp .\ssd1306.py :ssd1306.py
    mpremote connect COM6 reset

## Files

- main.py: MicroPython application copied to the board
- requirements.txt: host-side Python dependencies for flashing and file upload
- .gitignore: ignores the local virtual environment

## Notes

- This keeps the project Python-first. There is no C++ firmware in the repo.
- The first flash installs the MicroPython runtime. After that, normal iteration is usually just updating main.py.
- If GPIO 48 is not correct for your board, change the fallback pin in main.py.
- If your board has Octal PSRAM, use the ESP32-S3 spiram-oct firmware variant from the same MicroPython download page.
- If mpremote reports "could not enter raw repl", the board usually finished booting correctly; the failure is often timing-related, so adding sleep 1 or sleep 2 after connect is the first thing to try.
