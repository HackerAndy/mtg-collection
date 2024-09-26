import requests
import pandas as pd
import os
import time
from datetime import datetime, timedelta

_mtgDataFileName = 'mtg_raw_data.json'
_url = 'https://data.scryfall.io/oracle-cards/oracle-cards-20240925090209.json'

_headers = {
    'Accept': 'application/json'  # Specify the content type you're expecting
}

def if_download(filename):
    # Check if the file exists
    if os.path.exists(_mtgDataFileName):
        # Get the current time and file creation time
        file_creation_time = os.path.getctime(_mtgDataFileName)
        file_creation_datetime = datetime.fromtimestamp(file_creation_time)
        
        # Calculate the time 24 hours ago from now
        time_24_hours_ago = datetime.now() - timedelta(hours=24)
        
        # Check if the file was created within the last 24 hours
        if file_creation_datetime > time_24_hours_ago:
            print(f"File:{filename} was created within the last 24 hours. \n !Skipping download!")
            return False
        else:
            print(f"File:{filename} is older than 24 hours. \n !Proceeding to download!")
            return True
    else:
        print(f"File:{filename} doesn't exist in current directory. \n !Proceeding to download!")
        return True
    
def download_file(dest_file_name):
    response = requests.get(_url, headers = _headers)

    if response.status_code == 200:
        # Save the JSON content to a file
        with open(dest_file_name, 'w') as json_file:
            json_file.write(response.text)
        print("File downloaded successfully!")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

if if_download(_mtgDataFileName):
    download_file(_mtgDataFileName)

# Read the JSON file into a DataFrame
selected_columns = ['name', 'color_identity', 'set_name', 'collector_number']

df = pd.read_json(_mtgDataFileName)
df = df[selected_columns]

# Display the first few rows of the DataFrame
print(df.columns)