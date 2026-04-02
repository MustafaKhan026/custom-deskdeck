# DeskDeck

A DIY USB PC control board using an Arduino Nano that lets you control system volume, display brightness, and media playback using a rotary encoder, potentiometer, and push buttons. No drivers, no bloatware — just plug in and run.

---

## Features

- **Rotary encoder** — Volume up/down + mute toggle (press)
- **Potentiometer** — Laptop screen brightness control
- **Button 1** — Play / Pause
- **Button 2** — Next track
- **Button 3** — Previous track
- **Button 4** — Launch custom app (default: Brave Browser)
- **Auto COM port detection** — works on any Windows PC without configuration

---

## Components

| Component | Quantity |
|---|---|
| Arduino Nano | 1 |
| Rotary encoder (EC11) | 1 |
| Potentiometer (10kΩ) | 1 |
| Push buttons (6x6 tactile) | 4 |
| Breadboard | 1 |
| Jumper wires | ~20 |
| USB cable (Mini or Micro USB for Nano) | 1 |

> **Arduino Uno** works too — same pins, same code. Nano is recommended for demos due to its smaller size and breadboard-friendly form factor.

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

### Rotary Encoder

```
Encoder CLK  →  Arduino Pin 2
Encoder DT   →  Arduino Pin 3
Encoder SW   →  Arduino Pin 4
Encoder +    →  Arduino 5V
Encoder GND  →  Arduino GND
```

> No external resistors needed — uses Arduino internal pull-ups.

### Potentiometer

```
Left pin    →  Arduino GND
Middle pin  →  Arduino A0  (signal)
Right pin   →  Arduino 5V
```

### Push Buttons

```
Button 1 leg A  →  Arduino Pin 5
Button 2 leg A  →  Arduino Pin 6
Button 3 leg A  →  Arduino Pin 7
Button 4 leg A  →  Arduino Pin 8
All buttons leg B  →  Arduino GND
```

> **Important:** Buttons must straddle the center gap of the breadboard — one leg on each side. If the action triggers without pressing, rotate the button 90°.

---

## Arduino Code

Upload `pc_control.ino` to your Arduino Nano via Arduino IDE.

### Arduino IDE Settings for Nano

```
Tools → Board     → Arduino Nano
Tools → Processor → ATmega328P (Old Bootloader)   ← use this if upload fails
Tools → Port      → your COM port
```


### Serial Commands Reference

| Command | Trigger | Action |
|---|---|---|
| `CW` | Encoder clockwise | Volume up |
| `CCW` | Encoder counter-clockwise | Volume down |
| `BTN` | Encoder press | Mute toggle |
| `BRIGHT:XX` | Potentiometer turn | Set brightness to XX% |
| `PLAY` | Button 1 press | Play / Pause |
| `NEXT` | Button 2 press | Next track |
| `PREV` | Button 3 press | Previous track |
| `BRAVE` | Button 4 press | Launch app |

---

## Python Script (Windows)

### Requirements

```bash
pip install pyserial
```

### Setup

No COM port configuration needed — the script auto-detects the Nano. Just update `BRAVE_PATH` if your app is installed elsewhere.


### Run on Startup

1. Save `pc_control.py` to a folder e.g. `C:\Users\YourName\DeskDeck\`
2. Create `run.bat` in the same folder:

```bat
@echo off
pythonw "%~dp0pc_control.py"
```

3. Press `Win + R` → type `shell:startup` → paste a shortcut to `run.bat` there

---

## Run Without Python (Standalone .exe)

Build a standalone executable — no Python needed on the target PC.

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole pc_control.py
```

The `.exe` will be in the `dist\` folder. Copy it to any Windows PC and run directly.

### Using on a Different Laptop

1. Plug in the Nano via USB
2. Windows 10/11 installs the CH340 driver automatically
3. Run `DeskDeck.exe`

That's it — no Python, no COM port setup, no configuration needed. The exe auto-detects the Nano.

> **Driver not installing?** On older Windows versions, manually install the CH340 driver from [sparks.gogo.co.nz/ch340.html](https://sparks.gogo.co.nz/ch340.html)

---

## Troubleshooting

| Problem | Fix |
|---|---|
| No output in Serial Monitor | Check wiring, ensure `INPUT_PULLUP` is set for CLK and DT |
| Encoder spins but shows wrong direction | Swap CLK and DT wires |
| Button triggers without pressing | Rotate button 90° on breadboard so legs straddle the center gap |
| Python script: device not found | Make sure Nano is plugged in before running script |
| Nano not detected in Arduino IDE | Try `Tools → Processor → ATmega328P (Old Bootloader)` |
| Brightness flickering | Already fixed with 5-sample averaging and deadband of 5 in sketch |
| Brightness not changing | Only works on laptop built-in displays — external monitors not supported via WMI |
| Volume not changing | Ensure no other app has exclusive audio control |

---

## Repo Structure

```
DeskDeck/
├── pc_control.ino       # Arduino sketch
├── pc_control.py        # Python listener (Windows)
├── run.bat              # Startup helper
└── README.md            # This file
```

---

## Roadmap

- [x] Working breadboard prototype with Arduino Uno
- [x] Ported to Arduino Nano for compact demos
- [x] Auto COM port detection
- [x] Standalone .exe (no Python needed)
- [ ] Custom PCB using ATmega328P (no Nano needed)
- [ ] 3D printed enclosure
- [ ] System tray icon for Windows
- [ ] OLED display showing volume / track info
- [ ] macOS and Linux support
- [ ] External monitor brightness via DDC/CI

---

## License

MIT License — free to use, modify, and distribute.

---

## Contributing

Pull requests welcome! If you add macOS/Linux support, new button actions, or hardware improvements, feel free to open a PR.