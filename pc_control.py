import serial
import serial.tools.list_ports
import subprocess
import sys
import time
import webbrowser

BAUD_RATE  = 9600
# BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"


CREATE_NO_WINDOW = 0x08000000

def find_nano_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if any(keyword in port.description for keyword in ['CH340', 'Arduino', 'USB-SERIAL', 'USB Serial Port']):
            return port.device
    return None

def run_ps(script):
    subprocess.Popen(
        ['powershell', '-Command', script],
        creationflags=CREATE_NO_WINDOW
    )

def set_volume(direction):
    key = "[char]175" if direction == 'UP' else "[char]174"
    run_ps(f"(New-Object -ComObject WScript.Shell).SendKeys({key})")

def toggle_mute():
    run_ps("(New-Object -ComObject WScript.Shell).SendKeys([char]173)")

def set_brightness(level):
    run_ps(f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")

def media_key(key):
    run_ps(f"(New-Object -ComObject WScript.Shell).SendKeys({key})")

def launch_default_browser():
    webbrowser.open("https://www.google.com")

# Wait up to 10 seconds for Nano to be detected
port = None
for _ in range(10):
    port = find_nano_port()
    if port:
        break
    time.sleep(1)

if not port:
    sys.exit(1)  # ← no input() — just exit silently

with serial.Serial(port, BAUD_RATE, timeout=0) as ser:
    buffer = ""
    while True:
        data = ser.read(ser.in_waiting or 1).decode('utf-8', errors='ignore')
        if not data:
            continue
        buffer += data
        while '\n' in buffer:
            line, buffer = buffer.split('\n', 1)
            line = line.strip()
            if not line:
                continue

            if   line == 'CW':    set_volume('UP')
            elif line == 'CCW':   set_volume('DOWN')
            elif line == 'BTN':   toggle_mute()
            elif line == 'PLAY':  media_key("[char]179")
            elif line == 'NEXT':  media_key("[char]176")
            elif line == 'PREV':  media_key("[char]177")
            elif line == 'BRAVE': launch_default_browser()
            elif line.startswith('BRIGHT:'):
                set_brightness(int(line.split(':')[1]))