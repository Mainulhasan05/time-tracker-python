import pygetwindow as gw
import time
import json
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# File to store the time tracking data
data_file = 'time_tracking_data.json'

# Function to load the existing time tracking data from the file
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    else:
        return {}

# Function to save the time tracking data to the file
def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

# Dictionary to store the time spent on each application (in seconds)
app_time_spent = load_data()

# Function to log active window and time spent
def log_time():
    active_window = gw.getActiveWindow()
    if active_window:
        app_title = active_window.title

        # If the app is already in the dictionary, add the elapsed time to its record
        if app_title in app_time_spent:
            app_time_spent[app_title]['time_spent'] += 1
        else:
            # If it's a new app, add it with the current time spent as 1 second
            app_time_spent[app_title] = {
                'time_spent': 1,
                'last_active_time': datetime.now().isoformat()
            }

        # Save the updated data to the file
        save_data(app_time_spent)

    # Schedule the function to run every second
    root.after(1000, log_time)

# Function to update the Tkinter GUI with the latest time tracking data
def update_gui():
    # Clear the treeview before updating it
    for item in treeview.get_children():
        treeview.delete(item)

    # Update the treeview with the latest data
    for app, data in app_time_spent.items():
        hours = data['time_spent'] // 3600
        minutes = (data['time_spent'] % 3600) // 60
        seconds = data['time_spent'] % 60
        treeview.insert('', 'end', values=(app, f"{hours}h {minutes}m {seconds}s"))

    # Call the function every second to update the GUI
    root.after(1000, update_gui)

# Set up the Tkinter window
root = tk.Tk()
root.title("Time Tracker")

# Create a Treeview widget to display application names and time spent
treeview = ttk.Treeview(root, columns=("Application", "Time Spent"), show="headings")
treeview.heading("Application", text="Application")
treeview.heading("Time Spent", text="Time Spent")
treeview.pack(padx=10, pady=10, fill="both", expand=True)

# Start the time logging and GUI update loop
root.after(1000, log_time)
root.after(1000, update_gui)

# Start the Tkinter event loop
root.mainloop()
