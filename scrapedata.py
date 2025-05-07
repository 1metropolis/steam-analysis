import json
from urllib.request import urlretrieve
import zipfile
import os

# Download data from Kaggle
# Dataset used: https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
download = ("https://www.kaggle.com/api/v1/datasets/download/fronkongames/steam-games-dataset") 
filename = "dataset.zip"

print("Downloading file...")
urlretrieve(download, filename)
print("Download complete.")

# the file is too large, needs to be split in order to stay below github's 100mb filesize limit
# split the jsons to each contain 'n' objects.
def json_splitter(filepath, objectcount):
    
    print("Starting JSON Splitter.")
    # unzip
    with zipfile.ZipFile(filepath, 'r') as z:
        
        # cycle through unzipped files
        for filename in z.namelist():
            
            # skip non-jasons
            if not filename.lower().endswith(".json"):
                print(f"Skipping {filename} because it isn't a JSON.")
                continue
            
            # from stackoverflow: decode zip from binary in utf-8
            with z.open(filename) as f:
                print(f"Opening and reading {filename}...")
                data = f.read()
                data_str = data.decode("utf-8")
                d = json.loads(data_str)
                
                # split jsons by object count
                objects = list(d.keys())
                for i in range(0, len(objects), objectcount): # from 1 to total length of objects, every 'n' objects
                    
                    json_chunk = {game_id: d[game_id] for game_id in objects[i:i + objectcount]}
                    
                    # create an output file "data_part_n.json" in folder "data"
                    output_file = f'data/data_{i // objectcount + 1}.json'
                    print(f'Creating file {output_file}...')
                    
                    # open output file
                    with open (output_file, 'w') as output:
                        # write json chunk to output_file
                        print(f'Writing information into {output_file}...')
                        json.dump(json_chunk, output, indent=4)
                        
    # clean up
    print('Cleaning up...')
    os.remove(filepath)

# split zip into smaller json files
json_splitter(filename, 7000)