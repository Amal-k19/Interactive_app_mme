# 🎛️ Resolume Serial OSC Controller

A cross-platform desktop GUI built with **PyQt5** that listens to serial commands and sends OSC messages to **Resolume Arena**. Designed for performers, VJs, and interactive installations using microcontrollers (like Arduino/ESP32) to control visuals.

---

## 🚀 Features

- Serial port auto-detection and dropdown selection
- Configurable baud rate input
- User-defined command mappings (e.g. "A" triggers column 1)
- Sends OSC messages to Resolume Arena
- Real-time serial and OSC log view
- Modern PyQt5 GUI with dynamic resizing and image-based design
- Supports up to 2 custom commands mapped to different Resolume columns

---

## 🖥️ Demo

![UI Screenshot](ui.png)  
_
---

## 🧰 Tech Stack

- **Python 3.7+**
- **PyQt5** – GUI Framework
- **pyserial** – Serial communication
- **python-osc** – OSC messaging
- **Pillow** – Image support for PNG/JPEG icons

---

## 📦 Installation

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/resolume-serial-osc-controller.git
cd resolume-serial-osc-controller
