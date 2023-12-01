from thefuzz import fuzz, process
import time
from datetime import datetime
list = [['Elecktrotechnick', 'Mechanick', 'Physik', 'mathe','banana'], ['Mechanick', 'Physik', 'mathe','banana']]
#print(process.extract("bandna", list[0], scorer=fuzz.token_set_ratio))

import time
from datetime import datetime
import random
import json

# Create a list of datetime objects
time_objects = []

for i in range(4):
    time.sleep(1)
    time_objects.append(datetime.strptime(time.asctime(), "%a %b %d %H:%M:%S %Y") )
    
import time
from datetime import datetime
import json

# Create a list of datetime objects
time_objects = [datetime.strptime(time.asctime(), "%a %b %d %H:%M:%S %Y") for _ in range(5)]

# Sort the list based on datetime
sorted_time_objects = sorted(time_objects)

# Convert datetime objects to formatted strings
sorted_time_strings = [time_obj.strftime("%a %b %d %H:%M:%S %Y") for time_obj in sorted_time_objects]

# Dump the sorted time strings into a JSON file
json_file_path = 'sorted_times.json'
with open(json_file_path, 'w') as json_file:
    json.dump(sorted_time_strings, json_file)

print(f"Sorted time strings dumped to {json_file_path}")
