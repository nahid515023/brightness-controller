

import tkinter as tk
from tkinter import Scale, Entry, Button, Label, Frame
import subprocess

# Function to get current brightness using ddcutil
def get_current_brightness():
    try:
        # Run ddcutil to get the current brightness value
        result = subprocess.run(['ddcutil', 'getvcp', '10'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')

        # Parse the output for the brightness value
        # Example expected output line: "VCP code 0x10 (Brightness): current value = 75, max value = 100"
        for line in output.splitlines():
            if "current value" in line:
                # Extract the current value using split() or a regular expression
                current_value = int(line.split('=')[1].split(',')[0].strip())
                return current_value  # Return brightness as a percentage (0 to 100)
    except Exception as e:
        print(f"Error fetching brightness: {e}")
        return 100  # Default to 100% if fetching fails

# Function to change brightness using ddcutil
def change_brightness(value):
    """
    This function takes the brightness value (as a percentage) and sets the display brightness
    using ddcutil. It also updates the current brightness label.
    """
    try:
        brightness_value = int(float(value))  # Already in percentage
        cmd = ['ddcutil', 'setvcp', '10', str(brightness_value)]
        print("Running command:", cmd)  # Debugging output
        subprocess.run(cmd)
        # Update the live brightness label
        current_brightness_label.config(text=f"Current Brightness: {brightness_value}%")
    except Exception as e:
        print(f"Error: {e}")

# Function to update brightness from input box
def update_brightness_from_input():
    """
    This function reads the value entered in the input box, validates it, and then sets the 
    brightness accordingly. It syncs the value with the slider.
    """
    try:
        value = int(input_box.get())  # Get value in percentage
        if 0 <= value <= 100:
            brightness_slider.set(value)  # Sync the slider with the input box
            change_brightness(value)
        else:
            feedback_label.config(text="Brightness value should be between 0 and 100%", fg="red")
    except ValueError:
        feedback_label.config(text="Invalid input! Please enter a valid number between 0 and 100", fg="red")

# Create GUI window
root = tk.Tk()
root.title("Secondary Display Brightness Control")
root.geometry("400x300")  # Set the size of the window

# Create a Frame for better layout
main_frame = Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title label for the application
title_label = Label(main_frame, text="Brightness Control", font=("Arial", 16))
title_label.pack(pady=10)

# Fetch current brightness from the system
current_brightness = get_current_brightness()

# Slider to control brightness (now from 0 to 100)
brightness_slider = Scale(main_frame, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, label="Adjust Brightness (%)", command=change_brightness)
brightness_slider.set(current_brightness)  # Set the slider to the current brightness
brightness_slider.pack(pady=10)

# Input box for manual brightness entry
input_label = Label(main_frame, text="Enter Brightness (0 to 100%):")
input_label.pack()
input_box = Entry(main_frame, justify="center")
input_box.pack(pady=5)

# Button to apply the value from the input box
apply_button = Button(main_frame, text="Set Brightness", command=update_brightness_from_input, bg="#4CAF50", fg="white", font=("Arial", 12), padx=10, pady=5)
apply_button.pack(pady=10)

# Feedback label for input validation
feedback_label = Label(main_frame, text="", font=("Arial", 10))
feedback_label.pack()

# Live display of current brightness
current_brightness_label = Label(main_frame, text=f"Current Brightness: {current_brightness}%", font=("Arial", 12), fg="blue")
current_brightness_label.pack(pady=10)

# Center the window on the screen
root.eval('tk::PlaceWindow . center')

# Start the Tkinter event loop
root.mainloop()

