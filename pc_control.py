import serial
import serial.tools.list_ports
import subprocess
import sys

BAUD_RATE  = 9600
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

def find_nano_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if any(keyword in port.description for keyword in ['CH340', 'Arduino', 'USB-SERIAL']):
            print(f"Found device on {port.device}: {port.description}")
            return port.device
    return None

def set_volume(direction):
    key = "[char]175" if direction == 'UP' else "[char]174"
    subprocess.Popen(['powershell', '-Command',
        f"(New-Object -ComObject WScript.Shell).SendKeys({key})"])

def toggle_mute():
    subprocess.Popen(['powershell', '-Command',
        "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"])

def set_brightness(level):
    subprocess.Popen(['powershell', '-Command',
        f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"])
    print(f"Brightness: {level}%")

def media_key(key):
    subprocess.Popen(['powershell', '-Command',
        f"(New-Object -ComObject WScript.Shell).SendKeys({key})"])

def launch_brave():
    subprocess.Popen([BRAVE_PATH])
    print("Launching Brave!")

print("Searching for DeskDeck...")
port = find_nano_port()

if not port:
    print("ERROR: DeskDeck not found! Make sure the Nano is plugged in.")
    input("Press Enter to exit...")
    sys.exit(1)

print(f"Connected on {port}!")

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
            print(f"Received: {line}")

            if   line == 'CW':    set_volume('UP')
            elif line == 'CCW':   set_volume('DOWN')
            elif line == 'BTN':   toggle_mute()
            elif line == 'PLAY':  media_key("[char]179")
            elif line == 'NEXT':  media_key("[char]176")
            elif line == 'PREV':  media_key("[char]177")
            elif line == 'BRAVE': launch_brave()
            elif line.startswith('BRIGHT:'):
                set_brightness(int(line.split(':')[1]))