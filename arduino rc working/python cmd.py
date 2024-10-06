import requests
import keyboard
import time
import tkinter as tk

# Replace with the IP address of your ESP8266
esp8266_ip = "192.168.29.4"

# Define the URLs for controlling functions on the ESP8266
activate_pin1_url = f"http://{esp8266_ip}/activatePin1"
deactivate_pin1_url = f"http://{esp8266_ip}/deactivatePin1"
reverse_pin1_url = f"http://{esp8266_ip}/reversePin1"
activate_pin2_url = f"http://{esp8266_ip}/activatePin2"
deactivate_pin2_url = f"http://{esp8266_ip}/deactivatePin2"
reverse_pin2_url = f"http://{esp8266_ip}/reversePin2"

# Function to send a GET request to the ESP8266
def send_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Map keys to corresponding functions
key_mapping = {
    'w': activate_pin1_url,
    's': reverse_pin1_url,
    'a': activate_pin2_url,
    'd': reverse_pin2_url,
    'space': deactivate_pin1_url,  # Pressing space deactivates both motors
}

# Function to handle key press events
def on_key_press(event):
    key = event.name.lower()
    if key in key_mapping:
        send_request(key_mapping[key])

# Function to handle key release events
def on_key_release(event):
    key = event.name.lower()
    if key == 'space':
        send_request(deactivate_pin1_url)  # Pressing space deactivates both motors

# Set up key event handlers
keyboard.on_press(on_key_press)
keyboard.on_release(on_key_release)

# Tkinter GUI
root = tk.Tk()
root.title("ESP8266 Control")

# Function to activate a pin
def activate_pin(pin_url):
    send_request(pin_url)

# Function to deactivate both motors
def deactivate_motors():
    send_request(deactivate_pin1_url)

# Create buttons in the GUI
forward_button = tk.Button(root, text="Forward (W)", command=lambda: activate_pin(activate_pin1_url))
reverse_button = tk.Button(root, text="Reverse (S)", command=lambda: activate_pin(reverse_pin1_url))
left_button = tk.Button(root, text="Left (A)", command=lambda: activate_pin(activate_pin2_url))
right_button = tk.Button(root, text="Right (D)", command=lambda: activate_pin(reverse_pin2_url))
stop_button = tk.Button(root, text="Stop (Space)", command=deactivate_motors)

# Grid layout
forward_button.grid(row=0, column=1)
reverse_button.grid(row=2, column=1)
left_button.grid(row=1, column=0)
right_button.grid(row=1, column=2)
stop_button.grid(row=1, column=1)

# Run the Tkinter event loop
root.mainloop()
