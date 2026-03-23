# bb-scoreboard

Minimal ESP32-S3 MicroPython test project for bringing up the board and confirming that flashing works.

This project uses Python for both:

- the host-side tooling in a dedicated virtual environment
- the application code running on the ESP32-S3 through MicroPython

The example does two things:

- prints a hello-world message to the serial console at 115200 baud
- drives a 4-pin traffic-light LED module with green always on

## Project layout

  bb-scoreboard/
  |- .gitignore
  |- main.py
  |- README.md
  `- requirements.txt

## Hardware

This project targets an ESP32-S3 DevKit style board.

Use the UART / COM USB port for flashing. On your Windows host that is currently COM6.

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

Notes:

- GPIO38 is the on-board RGB LED on ESP32-S3-DevKitC-1 v1.1 according to Espressif.
- On boards using ESP32-S3-WROOM-2, GPIO35, GPIO36, and GPIO37 may be reserved for internal flash/PSRAM use and not available externally.
- Power the traffic-light module from signal pins only if the module is designed for that; otherwise use the module GND plus the three signal pins only.

If flashing fails, force bootloader mode:

1. Hold BOOT
2. Press and release RESET
3. Release BOOT
4. Retry the command

## Traffic Light Wiring

The current main.py expects this wiring:

- module GND -> ESP32-S3 GND
- module R -> ESP32-S3 GPIO6
- module Y -> ESP32-S3 GPIO5
- module G -> ESP32-S3 GPIO4

ASCII wiring diagram:

    Traffic light module                 ESP32-S3 DevKit
    --------------------                 ----------------
    [ GND ] ---------------------------> [ GND ]
    [ R   ] ---------------------------> [ GPIO6 ]
    [ Y   ] ---------------------------> [ GPIO5 ]
    [ G   ] ---------------------------> [ GPIO4 ]

Pin summary:

    Module pin   ESP32-S3 pin   Purpose
    ----------   -------------   -------
    GND          GND             Ground
    R            GPIO6           Red LED control
    Y            GPIO5           Yellow LED control
    G            GPIO4           Green LED control

Notes:

- This assumes a typical GND plus three signal pins traffic-light module.
- If the module is just bare LEDs and resistors are not onboard, add a 220-330 ohm resistor in series with each color line.
- If the LEDs behave inverted, the module may be active-low and the logic in main.py should be inverted.

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

### 4. Upload main.py to the board

From the project directory on the Windows host, use a short delay after connecting before the filesystem copy:

    mpremote connect COM6 sleep 1 fs cp .\main.py :main.py

### 5. Reset the board and open the serial console

    mpremote connect COM6 reset
    mpremote connect COM6 repl

You should see lines like:

    bb-scoreboard traffic light test
    red=OFF yellow=OFF green=ON

Exit the REPL with Ctrl+].

### 6. Next time you work on the board

Open PowerShell in the project and reactivate the environment:

    cd C:\path\to\bb-scoreboard
    .\.venv\Scripts\Activate.ps1

Then upload the updated script again:

    mpremote connect COM6 sleep 1 fs cp .\main.py :main.py
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
