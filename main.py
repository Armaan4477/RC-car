import sys
import socket
import threading
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QListWidget, QMessageBox, QDialog, QHBoxLayout
)

# UDP port to listen on
UDP_PORT = 4210
BUFFER_SIZE = 1024

class RelayControlDialog(QDialog):
    def __init__(self, device_ip):
        super().__init__()
        self.device_ip = device_ip
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Relay Control - {self.device_ip}')
        self.setGeometry(100, 100, 300, 200)
        
        self.layout = QVBoxLayout()

        self.relay_buttons = []
        for i in range(4):
            button = QPushButton(f'Toggle Relay {i+1}', self)
            button.clicked.connect(lambda checked, i=i: self.toggle_relay(i+1))
            self.layout.addWidget(button)
            self.relay_buttons.append(button)

        self.setLayout(self.layout)

    def toggle_relay(self, relay_number):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            message = json.dumps({f'relay{relay_number}': 'toggle'}).encode()
            sock.sendto(message, (self.device_ip, UDP_PORT))
            QMessageBox.information(self, 'Success', f'Toggled Relay {relay_number}')
        except Exception as e:
            QMessageBox.critical(self, 'Failed', f'Failed to toggle Relay {relay_number}: {e}')

class ESPDiscoveryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.discovered_devices = set()

    def initUI(self):
        self.setWindowTitle('ESP8266 Discovery')
        self.setGeometry(100, 100, 300, 200)
        
        self.layout = QVBoxLayout()

        self.button = QPushButton('Discover Devices', self)
        self.button.clicked.connect(self.discover_devices)
        self.layout.addWidget(self.button)

        self.device_list = QListWidget(self)
        self.layout.addWidget(self.device_list)
        
        self.connect_button = QPushButton('Connect to Selected Device', self)
        self.connect_button.clicked.connect(self.connect_device)
        self.layout.addWidget(self.connect_button)

        self.setLayout(self.layout)

    def discover_devices(self):
        self.device_list.clear()
        self.discovered_devices.clear()

        # Start a thread to listen for UDP broadcasts
        self.listen_thread = threading.Thread(target=self.listen_for_devices)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def listen_for_devices(self):
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(('', UDP_PORT))
        
        print(f"Listening for discovery messages on UDP port {UDP_PORT}")

        while True:
            try:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                message = data.decode()
                print(f"Received message: {message} from {addr}")
                try:
                    device_info = json.loads(message)
                    device_ip = device_info["ip"]
                    if device_ip not in self.discovered_devices:
                        self.discovered_devices.add(device_ip)
                        self.device_list.addItem(f"{device_info['device']} ({device_ip})")
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON message: {message}")
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def connect_device(self):
        selected_items = self.device_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select a device to connect to.')
            return
        
        selected_device = selected_items[0].text().split('(')[-1][:-1]  # Extract IP from item text
        
        # Send the "connected" command to the selected device
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b'connected', (selected_device, UDP_PORT))
            QMessageBox.information(self, 'Connected', f'Connected to {selected_device}')
            
            # Open relay control dialog
            relay_control_dialog = RelayControlDialog(selected_device)
            relay_control_dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, 'Connection Failed', f'Failed to connect to {selected_device}: {e}')

def main():
    app = QApplication(sys.argv)
    ex = ESPDiscoveryApp()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
