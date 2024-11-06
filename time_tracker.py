import pygetwindow as gw
import time
import json
from datetime import datetime
import os

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
    # Get the current active window
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

        # Print out the time spent on each app
        # print(f"\n{datetime.now()} - Active Window: {app_title}")
        # for app, data in app_time_spent.items():
        #     hours = data['time_spent'] // 3600
        #     minutes = (data['time_spent'] % 3600) // 60
        #     seconds = data['time_spent'] % 60
            # print(f"App: {app}, Time Spent: {hours}h {minutes}m {seconds}s")

        # Save the updated data to the file
        save_data(app_time_spent)

    time.sleep(1)  # Simulate some time delay to log periodically

while True:
    log_time()
