import pygetwindow as gw
import time
import json
import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import threading
import pyperclip  # For copying to clipboard
from tkinter import simpledialog

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

# Track if the app is paused
is_paused = False

# Function to log active window and time spent
def log_time():
    if not is_paused:
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
    filtered_data = filter_data()

    for app, data in filtered_data.items():
        hours = data['time_spent'] // 3600
        minutes = (data['time_spent'] % 3600) // 60
        seconds = data['time_spent'] % 60
        treeview.insert('', 'end', values=(app, f"{hours}h {minutes}m {seconds}s"))

    # Call the function every second to update the GUI
    root.after(1000, update_gui)

# Function to filter the data based on the selected date and application
def filter_data():
    filtered_data = app_time_spent.copy()

    # Date filter: If a specific date is selected
    # if selected_date.get():
    #     filtered_data = {app: data for app, data in filtered_data.items() if datetime.fromisoformat(data['last_active_time']).date() == selected_date.get()}

    # Application filter: If a specific application is selected
    if selected_application.get():
        filtered_data = {app: data for app, data in filtered_data.items() if app == selected_application.get()}

    return filtered_data

# Function to toggle the pause state
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    pause_button.config(text='Resume' if is_paused else 'Pause')

# Function to copy today's log as text to the clipboard
def copy_today_log():
    today = datetime.today().date()
    log_text = f"Time Log for {today}\n\n"
    
    filtered_data = {app: data for app, data in app_time_spent.items() if datetime.fromisoformat(data['last_active_time']).date() == today}

    for app, data in filtered_data.items():
        hours = data['time_spent'] // 3600
        minutes = (data['time_spent'] % 3600) // 60
        seconds = data['time_spent'] % 60
        log_text += f"{app}: {hours}h {minutes}m {seconds}s\n"

    pyperclip.copy(log_text)
    print("Today's log copied to clipboard.")

# Create a system tray icon
def create_icon():
    icon_image = Image.new('RGB', (64, 64), color=(255, 255, 255))
    draw = ImageDraw.Draw(icon_image)
    draw.rectangle([16, 16, 48, 48], fill="blue")

    icon = Icon("TimeTracker", icon_image, menu=Menu(MenuItem('Pause', toggle_pause), MenuItem('Exit', exit_program)))
    icon.run()

# Function to exit the program
def exit_program(icon, item):
    save_data(app_time_spent)  # Save data when exiting
    icon.stop()
    root.quit()

# Set up the Tkinter window
root = tk.Tk()
root.title("Time Tracker")

# Create a Treeview widget to display application names and time spent
treeview = ttk.Treeview(root, columns=("Application", "Time Spent"), show="headings")
treeview.heading("Application", text="Application")
treeview.heading("Time Spent", text="Time Spent")
treeview.pack(padx=10, pady=10, fill="both", expand=True)

# Add Pause/Resume Button
pause_button = tk.Button(root, text="Pause", command=toggle_pause)
pause_button.pack(pady=10)

# Date filter
# date_label = tk.Label(root, text="Select Date:")
# date_label.pack(pady=5)
# selected_date = tk.StringVar()
# date_entry = ttk.Entry(root, textvariable=selected_date)
# date_entry.pack(pady=5)

# Application filter
app_label = tk.Label(root, text="Select Application:")
app_label.pack(pady=5)
selected_application = tk.StringVar()
app_combobox = ttk.Combobox(root, textvariable=selected_application, values=list(app_time_spent.keys()))
app_combobox.pack(pady=5)

# Copy Button
copy_button = tk.Button(root, text="Copy Today's Log", command=copy_today_log)
copy_button.pack(pady=10)

# Start the time logging and GUI update loop
root.after(1000, log_time)
root.after(1000, update_gui)

# Run the system tray icon in a separate thread
tray_thread = threading.Thread(target=create_icon)
tray_thread.daemon = True
tray_thread.start()

# Start the Tkinter event loop
root.mainloop()

