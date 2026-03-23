# bb-scoreboard

Minimal ESP32-S3 MicroPython test project for bringing up the board and confirming that flashing works.

This project uses Python for both:

- the host-side tooling in a dedicated virtual environment
- the application code running on the ESP32-S3 through MicroPython

The example does two things:

- prints a hello-world message to the serial console at 115200 baud
- blinks the built-in LED when the board exposes Pin("LED"), otherwise it tries GPIO 48

## Project layout

  bb-scoreboard/
  |- .gitignore
  |- main.py
  |- README.md
  `- requirements.txt

## Hardware

This project targets an ESP32-S3 DevKit style board.

Use the UART / COM USB port for flashing. On your Windows host that is currently COM6.

If flashing fails, force bootloader mode:

1. Hold BOOT
2. Press and release RESET
3. Release BOOT
4. Retry the command

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

    C:\Users\you\Downloads\ESP32_GENERIC_S3-20251209-v1.27.0.bin

### 3. Erase and flash the MicroPython runtime to COM6

    python -m esptool --chip esp32s3 --port COM6 erase-flash
    python -m esptool --chip esp32s3 --port COM6 --baud 460800 write-flash -z 0 C:\Users\you\Downloads\ESP32_GENERIC_S3-20251209-v1.27.0.bin

### 4. Upload main.py to the board

From the project directory on the Windows host:

    mpremote connect COM6 fs cp .\main.py :main.py

### 5. Reset the board and open the serial console

    mpremote connect COM6 reset
    mpremote connect COM6 repl

You should see lines like:

    bb-scoreboard hello world
    MicroPython firmware booted successfully
    hello from ESP32-S3, tick=0
    hello from ESP32-S3, tick=1

Exit the REPL with Ctrl+].

### 6. Next time you work on the board

Open PowerShell in the project and reactivate the environment:

    cd C:\path\to\bb-scoreboard
    .\.venv\Scripts\Activate.ps1

Then upload the updated script again:

    mpremote connect COM6 fs cp .\main.py :main.py
    mpremote connect COM6 reset

## Files

- main.py: MicroPython application copied to the board
- requirements.txt: host-side Python dependencies for flashing and file upload
- .gitignore: ignores the local virtual environment

## Notes

- This keeps the project Python-first. There is no C++ firmware in the repo.
- The first flash installs the MicroPython runtime. After that, normal iteration is usually just updating main.py.
- If the LED does not blink, the serial output is still enough to verify that the board is running main.py.
- If GPIO 48 is not correct for your board, change the fallback pin in main.py.
