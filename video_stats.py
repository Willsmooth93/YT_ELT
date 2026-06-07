import requests
import json

import os
from dotenv import load_dotenv

API_KEY = os.getenv("API_KEY")

load_dotenv(dotenv_path="./.env")

CHANNEL_HANDLE = 'MrBeast'

def get_playlist_id():
    
    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)

        response.raise_for_status()
    
        data = response.json()

        #print(json.dumps(data, indent=4))

        channel_items = data["items"][0]
        channel_playlist_id = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlist_id)
        return channel_playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e
        

if __name__ == "__main__":
    # print("get_playlist_id will be executed.")
    get_playlist_id()
# else:
#     print("get_playlist_id will not be executed.")