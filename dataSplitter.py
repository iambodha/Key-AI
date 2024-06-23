import json
import os
import random

# Function to split a list into chunks
def split_list(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

# Read the JSON file
with open('abstracts.json', 'r') as file:
    data = json.load(file)

# Shuffle the data randomly
random.shuffle(data)

# Ensure the Data directory exists
os.makedirs('Data', exist_ok=True)

# Split the data into chunks of 100 elements each
chunks = list(split_list(data, 100))

# Save each chunk as a new JSON file with ascending numbers
for idx, chunk in enumerate(chunks):
    with open(f'Data/abstract_{idx}.json', 'w') as outfile:
        json.dump(chunk, outfile, indent=4)

print("Splitting and saving JSON files completed.")
