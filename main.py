import usb.core
import usb.util
import keyboard
import tkinter as tk
from tkinter import messagebox

#5.5s strzał
# Find the device
dev = usb.core.find(idVendor=0x0a81, idProduct=0x0701)

if dev is None:
    raise ValueError('Device not found')

# Set configuration (assuming there's only one configuration)
dev.set_configuration()

# Function to send data to the USB device
def send_data(data):
    try:
        dev.ctrl_transfer(0x21, 0x09, 0x0200, 0, data)
        print(f"Sent data: {data}")  # Optional: Print what was sent
    except usb.core.USBError as e:
        print(f"Error sending data: {e}")

# Function to handle key presses
def handle_key_press(key):
    if key == 'left' or key == 'a':
        send_data([0x4])
    elif key == 'right'  or key == 'd':
        send_data([0x8])
    elif key == 'up'  or key == 'w':
        send_data([0x2])
    elif key == 'down'  or key == 's':
        send_data([0x1])
    elif key == 'space':
        send_data([0x10])
    elif key == 'esc':
        exit_program()

# Function to handle key release
def handle_key_release(key):
    send_data([0x20])  # Send release command

# Function to handle key press events in the GUI
def on_key_event(event):
    if event.event_type == keyboard.KEY_DOWN:  # Check for key press
        handle_key_press(event.name)  # Use event.name for key identifier
    elif event.event_type == keyboard.KEY_UP:  # Check for key release
        handle_key_release(event.name)  # Use event.name for key identifier

# Function to exit the application
def exit_program():
    send_data([0x20])  # Send release command
    print("Exiting...")
    root.destroy()

# Set up the GUI
root = tk.Tk()
root.title("USB Control")

# Add a label to instruct the use
label = tk.Label(root, text="\n          strzałka w górę/w          \n\nstrzałka w lewo/a          strzałka w prawo/d\n\n          strzałka w dół/s          \n\nspacja (przytrzymaj 5.5s)\n\nEsc żeby wyjść")
label.pack(pady=20)

# Bind keyboard events using the keyboard library for global detection
keyboard.hook(on_key_event)  # Use on_key_event to handle keyboard events

# Bind the exit function to the window close event
root.protocol("WM_DELETE_WINDOW", exit_program)

# Start the Tkinter event loop
root.mainloop()
