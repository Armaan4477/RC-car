# Wi-Fi Controlled RC Car and Device Controller

An embedded systems and IoT robotics project powered by the ESP8266 microcontroller. This repository provides firmware and desktop control software to operate a remote-controlled (RC) vehicle over Wi-Fi, featuring an embedded web server, a real-time Python keyboard and GUI controller, and a PyQt6 UDP-based device discovery and multi-channel relay management interface.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Hardware Specifications](#hardware-specifications)
  - [Required Components](#required-components)
  - [Pinout and Wiring Configuration](#pinout-and-wiring-configuration)
- [Firmware Configuration and Flashing](#firmware-configuration-and-flashing)
  - [Prerequisites](#prerequisites)
  - [Configuring Wi-Fi Credentials](#configuring-wi-fi-credentials)
  - [Flashing via Arduino IDE](#flashing-via-arduino-ide)
- [Desktop Control Software](#desktop-control-software)
  - [Environment Setup](#environment-setup)
  - [1. Keyboard and GUI RC Controller](#1-keyboard-and-gui-rc-controller)
  - [2. Web Browser Dashboard](#2-web-browser-dashboard)
  - [3. PyQt6 UDP Discovery and Relay Management Tool](#3-pyqt6-udp-discovery-and-relay-management-tool)
  - [4. Diagnostic UDP Listener](#4-diagnostic-udp-listener)
- [Communication Protocol and API Reference](#communication-protocol-and-api-reference)
  - [HTTP REST Endpoints](#http-rest-endpoints)
  - [UDP Discovery and Control Protocol](#udp-discovery-and-control-protocol)
- [Repository Structure](#repository-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

This project provides end-to-end communication between a host computer or mobile device and an ESP8266 microcontroller driving dual DC motors via an H-bridge motor driver.

Key capabilities include:
- **Embedded Web Server**: The ESP8266 hosts an on-chip web dashboard serving HTML/JavaScript controls for direct browser-based operation without third-party apps.
- **Low-Latency REST Control**: HTTP endpoints allow programmatic manipulation of individual GPIO pins for directional control (forward, reverse, left, right, and stop).
- **Dual Desktop Interfaces**:
  - A lightweight Tkinter GUI coupled with global keyboard hooks (`W`, `A`, `S`, `D`, `Space`) for driving.
  - An advanced PyQt6 application that listens for UDP discovery broadcasts from network devices and provides an interactive relay control interface.
- **Diagnostic Tooling**: Minimalist UDP socket scripts for network verification and debugging.

---

## System Architecture

```text
+-------------------------------------------------------------+
|                     Control Interfaces                      |
|                                                             |
|   +--------------------+     +--------------------------+   |
|   | Desktop Python App |     | Web Browser Dashboard    |   |
|   | (Tkinter / Keys)   |     | (Phone / PC / Tablet)    |   |
|   +---------+----------+     +------------+-------------+   |
|             |                             |                 |
|             +--------------+--------------+                 |
|                            | HTTP (Port 80)                 |
+----------------------------|--------------------------------+
                             |
                             v
               +---------------------------+
               |  ESP8266 Microcontroller  |
               |  (NodeMCU / ESP-12E)      |
               +-------------+-------------+
                             |
         +-------------------+-------------------+
         | GPIO 5 (D1)       | GPIO 4 (D2)       |
         | GPIO 0 (D3)       | GPIO 2 (D4)       |
         v                   v                   v
+-------------------------------------------------------------+
|              L298N / Dual H-Bridge Driver                   |
|                                                             |
|     +--------------------+       +--------------------+     |
|     |  Motor A (Left)    |       |  Motor B (Right)   |     |
|     +--------------------+       +--------------------+     |
+-------------------------------------------------------------+
```

---

## Hardware Specifications

### Required Components

- **Microcontroller**: ESP8266 NodeMCU development board (v2 or v3) or ESP-12E module.
- **Motor Driver**: L298N or L293D dual H-bridge motor driver module.
- **Motors**: 2x or 4x TT gear DC motors (3V to 6V DC).
- **Chassis**: 2WD or 4WD robotic car chassis with wheels and caster.
- **Power Supply**:
  - Independent battery pack for motors (e.g., 2x 18650 3.7V Li-ion cells in series = 7.4V, or a 9V-12V DC source).
  - ESP8266 power source (via 5V pin from the L298N regulator or a dedicated 5V USB power bank).
- **Wiring**: Dupont jumper wires (male-to-female, female-to-female).
- **Optional**: 4-channel 5V relay module (for use with the PyQt6 discovery and relay controller).

### Pinout and Wiring Configuration

The firmware designates four digital output pins connected to the motor driver logic inputs:

| ESP8266 Physical Pin | GPIO Number | Firmware Variable | Motor Driver Input | Motor Operation |
|:---------------------|:------------|:------------------|:-------------------|:----------------|
| **D1**               | GPIO 5      | `pin1`            | IN1                | Motor A Forward |
| **D2**               | GPIO 4      | `pin2`            | IN2                | Motor A Reverse |
| **D3**               | GPIO 0      | `pin3`            | IN3                | Motor B Forward |
| **D4**               | GPIO 2      | `pin4`            | IN4                | Motor B Reverse |
| **GND**              | GND         | Ground Reference  | GND                | Common Ground   |
| **VIN / 5V**         | 5V Power    | Power Input       | 5V OUT             | Logic Power     |

> Note: Ensure a common ground connection between the ESP8266 GND and the motor driver GND to establish a shared electrical reference.

#### Directional Logic Truth Table

| Action | `pin1` (GPIO5) | `pin2` (GPIO4) | `pin3` (GPIO0) | `pin4` (GPIO2) | Motor Output Behavior |
|:---|:---|:---|:---|:---|:---|
| **Forward** | HIGH | LOW | HIGH | LOW | Both motors drive forward |
| **Reverse** | LOW | HIGH | LOW | HIGH | Both motors drive backward |
| **Turn Left** | HIGH | LOW | LOW | LOW | Left motor powered, right idle |
| **Turn Right** | LOW | LOW | HIGH | LOW | Right motor powered, left idle |
| **Stop** | LOW | LOW | LOW | LOW | All motor channels unpowered |

---

## Firmware Configuration and Flashing

The firmware is located at:
`arduino rc working/working/working.ino`

### Prerequisites

1. Install the [Arduino IDE](https://www.arduino.cc/en/software) (version 2.0 or newer).
2. Install the ESP8266 Board Package:
   - Navigate to **Preferences** in the Arduino IDE.
   - Add the following URL to **Additional Boards Manager URLs**:
     ```text
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
   - Open **Tools** > **Board** > **Boards Manager**, search for `esp8266`, and install version 3.0.0 or higher.

### Configuring Wi-Fi Credentials

Open `arduino rc working/working/working.ino` in your editor or Arduino IDE and modify lines 4 and 5 with your local network details:

```cpp
const char *ssid = "YOUR_WIFI_SSID";
const char *password = "YOUR_WIFI_PASSWORD";
```

### Flashing via Arduino IDE

1. Connect the ESP8266 board to your development workstation using a micro-USB data cable.
2. Select your board model under **Tools** > **Board** > **ESP8266 Boards** (e.g., `NodeMCU 1.0 (ESP-12E Module)`).
3. Select the active serial port under **Tools** > **Port** (e.g., `/dev/cu.usbserial-*` on macOS, `COM*` on Windows, or `/dev/ttyUSB*` on Linux).
4. Set the upload speed to `115200` baud.
5. Click **Upload**.
6. Once flashing is complete, open the **Serial Monitor** at `115200` baud. Note the assigned IP address displayed once connection is established:
   ```text
   WiFi connected
   Server started
   ```

---

## Desktop Control Software

### Environment Setup

The desktop software requires Python 3.8 or higher.

1. Clone the repository (if not already local):
   ```bash
   git clone https://github.com/Armaan4477/RC-car.git
   cd RC-car
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # On Windows:
   # venv\Scripts\activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   Alternatively, install them individually:
   ```bash
   pip install requests keyboard PyQt6
   ```

---

### 1. Keyboard and GUI RC Controller

File: `arduino rc working/python cmd.py`

This script provides an interactive window and binds hardware keystrokes to HTTP requests sent to the ESP8266.

#### Configuration
Update line 7 of `arduino rc working/python cmd.py` with the current IP address of your ESP8266 board:
```python
esp8266_ip = "192.168.29.4"  # Replace with your ESP8266 IP
```

#### Execution
Run the script using Python:
```bash
python3 "arduino rc working/python cmd.py"
```

> Important Note for macOS and Linux Users:
> The `keyboard` module intercepts global key events. On macOS, terminal applications require Accessibility permissions under **System Settings** > **Privacy & Security** > **Accessibility**. On Linux, global keyboard capture may require execution with administrative privileges (`sudo`).

#### Control Key Bindings

| Key | Movement Action | Target Endpoint | Description |
|:---|:---|:---|:---|
| **W** | Forward | `/activatePin1` | Activates forward drive on both motors |
| **S** | Reverse | `/reversePin1` | Activates reverse drive on both motors |
| **A** | Turn Left | `/activatePin2` | Drives right side to steer left |
| **D** | Turn Right | `/reversePin2` | Drives left side to steer right |
| **Space** | Stop | `/deactivatePin1` | Cuts power to all motor pins |

The script also displays a Tkinter graphical interface with clickable buttons corresponding to each directional command.

---

### 2. Web Browser Dashboard

The ESP8266 hosts an internal web page accessible directly from any web browser on the same Wi-Fi network:

1. Open a browser and navigate to:
   ```text
   http://<ESP8266_IP_ADDRESS>/
   ```
2. The page renders an interface with buttons to:
   - Activate Forward (`/activatePin1`)
   - Deactivate Forward (`/deactivatePin1`)
   - Activate Reverse (`/reversePin1`)
   - Activate Left (`/activatePin2`)
   - Deactivate Direction (`/deactivatePin2`)
   - Activate Right (`/reversePin2`)

Each button dispatches an asynchronous `fetch()` request without refreshing the page.

---

### 3. PyQt6 UDP Discovery and Relay Management Tool

File: `main.py`

A desktop application designed for automated network discovery and peripheral relay control over UDP.

#### Execution
```bash
python3 main.py
```

#### Capabilities
- **Automated UDP Listener**: Binds to UDP port `4210` in a background daemon thread.
- **Dynamic Device List**: Parses incoming JSON broadcast beacons containing device metadata (`{"device": "<name>", "ip": "<ip_address>"}`) and populates the device list.
- **Connection Handshake**: Dispatches a `"connected"` UDP handshake datagram to the target IP on port `4210`.
- **4-Channel Relay Control**: Launches a modal dialog with dedicated controls to toggle four individual relays via JSON payloads (e.g., `{"relay1": "toggle"}`).

---

### 4. Diagnostic UDP Listener

File: `basic.py`

A lightweight diagnostic script for inspecting incoming UDP packets on port `4210`.

#### Execution
```bash
python3 basic.py
```

Prints raw UDP payloads and originating IP addresses to the standard output for network debugging.

---

## Communication Protocol and API Reference

### HTTP REST Endpoints

The ESP8266 web server handles the following HTTP `GET` endpoints on port 80:

| HTTP Method | Route | Description | Response Status | Response Body |
|:---|:---|:---|:---|:---|
| `GET` | `/` | Serves root HTML/JS web dashboard | 200 OK | HTML Document |
| `GET` | `/activatePin1` | Drives vehicle forward | 200 OK | `Pin 1 activated` |
| `GET` | `/deactivatePin1` | Stops all motors | 200 OK | `Pin 1 deactivated` |
| `GET` | `/reversePin1` | Drives vehicle in reverse | 200 OK | `Motor 1 reversed` |
| `GET` | `/activatePin2` | Turns vehicle left | 200 OK | `Pin 2 activated` |
| `GET` | `/deactivatePin2` | Resumes forward drive | 200 OK | `Pin 2 deactivated` |
| `GET` | `/reversePin2` | Turns vehicle right | 200 OK | `Motor 2 reversed` |

### UDP Discovery and Control Protocol

- **Port**: `4210`
- **Socket Options**: Broadcast enabled (`SO_BROADCAST`)

#### Discovery Beacon Format (Device to Host)
```json
{
  "device": "ESP8266_Car",
  "ip": "192.168.1.150"
}
```

#### Connection Handshake (Host to Device)
Raw UTF-8 byte stream:
```text
connected
```

#### Relay Toggle Payload (Host to Device)
JSON payload targeting a specific relay channel:
```json
{
  "relay1": "toggle"
}
```

---

## Repository Structure

```text
RC-car/
|-- README.md                             # Comprehensive project documentation
|-- requirements.txt                      # Python dependencies specification
|-- basic.py                              # Minimal UDP listener diagnostic utility
|-- main.py                               # PyQt6 UDP discovery and relay control GUI
|-- arduino rc working/
|   |-- python cmd.py                     # Keyboard and Tkinter desktop motor controller
|   `-- working/
|       `-- working.ino                   # ESP8266 Arduino firmware and HTTP server
|-- .gitattributes                        # Repository line-ending and attribute settings
```

---

## Troubleshooting

### ESP8266 Fails to Connect to Wi-Fi
- Verify that your Wi-Fi network operates on the 2.4 GHz frequency band. The ESP8266 does not support 5 GHz Wi-Fi networks.
- Confirm that the credentials entered in `working.ino` match your network SSID and passphrase exactly.
- Check that the USB cable provides both data and power (some charging cables do not include data lines).

### Motors Do Not Rotate or Stutter
- Ensure the motor power supply is adequate (at least 7V DC for an L298N driver due to internal voltage drops).
- Verify that the ground (GND) pin of the ESP8266 is tied to the ground (GND) pin of the motor driver.
- If the motors emit a high-pitched whine without turning, increase the supply voltage or inspect the wheels for mechanical binding.

### Python Keyboard Input Not Registering
- On macOS, open **System Settings** > **Privacy & Security** > **Accessibility** and ensure your terminal emulator (Terminal, iTerm2, or VS Code) is enabled.
- On Linux, execute the script with administrative privileges: `sudo python3 "arduino rc working/python cmd.py"`.

### Cannot Reach the ESP8266 Web Server
- Verify both your computer and the ESP8266 are on the same subnet and local network.
- Confirm the IP address via the Arduino Serial Monitor at 115200 baud.
- Use `ping <ESP8266_IP>` in your terminal to verify connectivity.

---

## License

This project is open-source and available under the standard MIT License. Feel free to modify and adapt the code for educational and hobbyist robotics applications.
