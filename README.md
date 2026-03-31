# Arduino PC Control Board

A DIY USB PC control board using an Arduino Uno that lets you control system volume, display brightness, and media playback using a rotary encoder, potentiometer, and push buttons.

---

## Features

- **Rotary encoder** — Volume up/down + mute toggle (press)
- **Potentiometer** — Laptop screen brightness control
- **Button 1** — Play / Pause
- **Button 2** — Next track
- **Button 3** — Previous track
- **Button 4** — Launch custom app (default: Brave Browser)

---

## Components

| Component | Quantity |
|---|---|
| Arduino Uno | 1 |
| Rotary encoder (EC11) | 1 |
| Potentiometer (10kΩ) | 1 |
| Push buttons (6x6 tactile) | 4 |
| Breadboard | 1 |
| Jumper wires | ~20 |
| USB cable (Type-B) | 1 |

---

## Wiring

### Pin Map

| Component | Pin | Arduino Pin |
|---|---|---|
| Rotary encoder CLK | CLK | D2 |
| Rotary encoder data | DT | D3 |
| Rotary encoder button | SW | D4 |
| Rotary encoder power | + | 5V |
| Rotary encoder ground | GND | GND |
| Potentiometer signal | Middle | A0 |
| Potentiometer ground | Left | GND |
| Potentiometer power | Right | 5V |
| Button 1 (Play/Pause) | Leg A | D5 |
| Button 2 (Next) | Leg A | D6 |
| Button 3 (Previous) | Leg A | D7 |
| Button 4 (Custom) | Leg A | D8 |
| All buttons ground | Leg B | GND |

### Rotary Encoder Wiring

```
Encoder CLK  →  Arduino Pin 2
Encoder DT   →  Arduino Pin 3
Encoder SW   →  Arduino Pin 4
Encoder +    →  Arduino 5V
Encoder GND  →  Arduino GND
```

> No external resistors needed — uses Arduino internal pull-ups.

### Potentiometer Wiring

```
Left pin    →  Arduino GND
Middle pin  →  Arduino A0  (signal)
Right pin   →  Arduino 5V
```

### Push Button Wiring

```
Button 1 leg A  →  Arduino Pin 5
Button 2 leg A  →  Arduino Pin 6
Button 3 leg A  →  Arduino Pin 7
Button 4 leg A  →  Arduino Pin 8
All buttons leg B  →  Arduino GND
```

> **Important:** Buttons must straddle the center gap of the breadboard. One leg on each side of the gap. If the action triggers without pressing, rotate the button 90°.

---

## Arduino Code

Upload `sketch/pc_control.ino` to your Arduino Uno via Arduino IDE.

## Python Script (Windows)

### Requirements

```bash
pip install pyserial
```

### Setup

1. Find your Arduino COM port: **Device Manager → Ports (COM & LPT)**
2. Update `SERIAL_PORT` in `pc_control.py`
3. Update `BRAVE_PATH` if your app is installed elsewhere


### Run on Startup

1. Save `pc_control.py` to a folder e.g. `C:\Users\YourName\ArduinoControl\`
2. Create `run.bat` in the same folder:

```bat
@echo off
pythonw "C:\Users\YourName\ArduinoControl\pc_control.py"
```

3. Press `Win + R` → type `shell:startup` → paste a shortcut to `run.bat` there

---

## Run Without Python (Standalone .exe)

Build a standalone executable using PyInstaller — no Python needed on the target PC.

```bash
pip install pyinstaller
cd path\to\your\project
pyinstaller --onefile --noconsole pc_control.py
```

The `.exe` will be in the `dist\` folder. Copy it to any Windows PC and run directly.

> **Note:** The Arduino COM port may differ on different PCs. Check Device Manager on the target PC and update the port in the script before building the exe.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| No output in Serial Monitor | Check wiring, ensure `INPUT_PULLUP` is set for CLK and DT |
| Encoder spins but shows wrong direction | Swap CLK and DT wires |
| Button triggers without pressing | Button legs are shorting — rotate button 90° on breadboard so legs straddle center gap |
| Python script: port error | Close Arduino IDE completely before running script |
| Python script: wrong COM port | Check Device Manager → Ports for correct COM number |
| Brightness not changing | Only works on laptop built-in displays. External monitors not supported via WMI |
| Volume not changing | Ensure no other app has exclusive audio control |

---

## Repo Structure

```
arduino-pc-control/
├── sketch/
│   └── pc_control.ino       # Arduino sketch
├── pc_control.py             # Python listener script
├── run.bat                   # Windows startup helper
└── README.md                 # This file
```

---

## Roadmap / Future Ideas

- [ ] Auto-detect COM port (no manual config needed)
- [ ] Standalone `.exe` with system tray icon
- [ ] Custom PCB using ATmega328P (no Arduino Uno needed)
- [ ] 3D printed enclosure
- [ ] OLED display showing current volume / track info
- [ ] Support for external monitors via DDC/CI

---

## License

MIT License — free to use, modify, and distribute.

---

## Contributing

Pull requests welcome! If you add support for macOS/Linux or new features, feel free to open a PR.
