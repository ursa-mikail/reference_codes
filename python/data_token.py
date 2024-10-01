import random
from datetime import datetime, timedelta
import time

def generate_random_timestamp(start, end):
    """Generate a random timestamp between start and end dates."""
    start_time = datetime.strptime(start, "%Y-%m-%d_%H%M_%S")
    end_time = datetime.strptime(end, "%Y-%m-%d_%H%M_%S")
    
    random_time = start_time + (end_time - start_time) * random.random()
    return random_time.strftime("%Y-%m-%d_%H%M_%S")

def timestamp_to_unix(timestamp):
    """Convert a timestamp to Unix time."""
    dt = datetime.strptime(timestamp, "%Y-%m-%d_%H%M_%S")
    return int(time.mktime(dt.timetuple()))

def unix_to_timestamp(unix_time):
    """Convert Unix time back to a timestamp."""
    dt = datetime.fromtimestamp(unix_time)
    return dt.strftime("%Y-%m-%d_%H%M_%S")

def is_expired(timestamp):
    """Check if the given timestamp is expired."""
    current_time = datetime.now()
    timestamp_time = datetime.strptime(timestamp, "%Y-%m-%d_%H%M_%S")
    return (timestamp_time - current_time).total_seconds() <= 0

# Example usage
time_start = "2023-09-01_0000_00"
time_end = "2024-09-01_0000_00"

random_timestamp = generate_random_timestamp(time_start, time_end)
print("Random Timestamp:", random_timestamp)

unix_time = timestamp_to_unix(random_timestamp)
print("Unix Time:", unix_time)

converted_timestamp = unix_to_timestamp(unix_time)
print("Converted Timestamp:", converted_timestamp)

expired = is_expired(random_timestamp)
print("Is Expired:", expired)

"""
Random Timestamp: 2024-08-30_0207_57
Unix Time: 1724983677
Converted Timestamp: 2024-08-30_0207_57
Is Expired: True
"""

import json

def create_json_with_dictionary(data_dict):
    """Update the given dictionary with a random timestamp and return it as a JSON string."""
    time_start = data_dict.get('time_start', '2023-09-01_0000_00')
    time_end = data_dict.get('time_end', '2024-09-01_0000_00')
    random_timestamp = generate_random_timestamp(time_start, time_end)
    data_dict['timestamp'] = random_timestamp
    return json.dumps(data_dict, indent=4, sort_keys=True)

def check_field_in_json(filename, field):
    """Check if a specific field exists in the JSON and return its value if it does."""
    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            if field in data:
                return data[field]
            else:
                return None
    except FileNotFoundError:
        return None

def store_json_as_file(data_json, json_filename):
    with open(json_filename, 'w') as json_file:
        json_file.write(data_json)

def read_json_from_file(json_filename):
    """Read the JSON content from a file and return it."""
    try:
        with open(json_filename, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"The file {json_filename} does not exist.")

def print_json(json_data):
    """Print the contents of a JSON in a pretty format."""
    print(json.dumps(json_data, indent=4, sort_keys=True))


# Example usage
json_filename = "data.json"

# Store timestamp in JSON
data_dict = {
    'event': 'example_event',
    'details': 'This is an example data dictionary.',
    'time_start': "2023-09-01_0000_00",
    'time_end': "2024-09-01_0000_00"
}

# Create JSON with dictionary
data_json = create_json_with_dictionary(data_dict)
print("Updated JSON String:")
print(data_json)

print(f"Data stored in {json_filename}")
store_json_as_file(data_json, json_filename)

json_data_recovered = read_json_from_file(json_filename)

# Check field in JSON
field_tag_to_look_for = 'time_start' # 'timestamp'
field_value = check_field_in_json(json_filename, field_tag_to_look_for)
if field_value:
    print(f"Field 'timestamp' exists in {json_filename} with value: {field_value}")
else:
    print(f"Field 'timestamp' does not exist in {json_filename}")

# Print JSON file
print("Pretty JSON Content:")
print_json(json_data_recovered)

"""
Updated JSON String:
{
    "details": "This is an example dictionary.",
    "event": "example_event",
    "time_end": "2024-09-01_0000_00",
    "time_start": "2023-09-01_0000_00",
    "timestamp": "2024-03-15_0159_11"
}
Data stored in data.json
Field 'timestamp' exists in data.json with value: 2023-09-01_0000_00
Pretty JSON Content:
{
    "details": "This is an example dictionary.",
    "event": "example_event",
    "time_end": "2024-09-01_0000_00",
    "time_start": "2023-09-01_0000_00",
    "timestamp": "2024-03-15_0159_11"
}
"""