# auto
"""
import requests

def notify_client(data):
    url = "http://127.0.0.1:5000/webhook"
    response = requests.post(url, json=data)
    return response.status_code

# Example of sending a notification
data = {
    'event': 'zero-day vulnerability',
    'details': 'A new zero-day vulnerability has been discovered in XYZ software.'
}
print(notify_client(data))
"""

# manual
import requests
import json
import time
import random
from datetime import datetime

# Define the server URL
SERVER_URL = "http://127.0.0.1:5000/webhook"

def send_data(data):
    """Send the webhook data to the server."""
    response = requests.post(SERVER_URL, json=data)
    if response.status_code == 200:
        print(f"Sent data: {data}")
    else:
        print(f"Failed to send data: {response.status_code}")

def main():
    # Loop to allow sending multiple events
    while True:
        # Choose the event type (either 'new' or 'resolved')
        event_type = input("Enter event type ('new' or 'resolved', or 'clear' to remove last data): ").strip().lower()
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H%M_%S')  # Get current timestamp

        if event_type == 'new':
            data = {
                'event': 'zero-day vulnerability',
                'details': 'A new zero-day vulnerability has been discovered in XYZ software.',
                'timestamp': timestamp  # Add timestamp to data
            }
            send_data(data)

        elif event_type == 'resolved':
            data = {
                'event': 'zero-day vulnerability resolved',
                'details': 'The previously reported zero-day vulnerability in XYZ software has been resolved.',
                'timestamp': timestamp  # Add timestamp to data
            }
            send_data(data)

        elif event_type == 'clear':
            clear_option = input("Do you want to clear the data before the next send? (yes/no): ").strip().lower()
            if clear_option == 'yes':
                print("Clearing data...")
                # Clear the data variable (if any processing is required, add it here)
                data = {
                    'event': '------------------',
                    'details': '------------------',
                    'timestamp': timestamp  # Add timestamp to data
                }
                send_data(data)
                
                continue  # Skip to the next iteration

        else:
            print("Invalid event type. Please enter 'new', 'resolved', or 'clear'.")
            continue  # Ask again

        # Sleep for a random interval before the next send
        time.sleep(random.randint(5, 10))

if __name__ == "__main__":
    main()


