import base64
import json
import requests
from PIL import Image
from io import BytesIO
import csv
import os
import json
from concurrent.futures import ThreadPoolExecutor
import sys, getopt
from dotenv import load_dotenv
load_dotenv()


def read_artist_album_names_from_csv(file_path):
    artist_album_names = set()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        for row in data:
            artist_album_names.add((row[0], row[1]))
    return list(artist_album_names)


def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials'
    }
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
    }
    response = requests.post(auth_url, data=auth_data, headers=auth_header)
    if response.status_code == 200:
        return json.loads(response.text)['access_token']
    else:
        return None

def search_albums(artist, album, access_token):
    search_url = 'https://api.spotify.com/v1/search'
    search_params = {
        'q': f'artist:{artist} album:{album}',
        'type': 'album',
        'limit': 50
    }
    search_header = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(search_url, params=search_params, headers=search_header)
    if response.status_code == 200:
        albums = json.loads(response.text)['albums']['items']
        return [
            a for a in albums
            if a is not None
            and a.get('name') is not None
            and a['name'].lower() == album.lower()
            and any(
                artist.lower() in ar['name'].lower() for ar in a['artists'] if ar.get('name') is not None
            )
        ]
    else:
        return []

def download_album_cover(album, folder):
    image_url = album['images'][0]['url']
    image_name = album['name'] + '.jpg'
    
    # Sanitize the image name by replacing invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        image_name = image_name.replace(char, '_')
    
    image_path = os.path.join(folder, image_name)

    # Check if the file already exists
    if os.path.isfile(image_path):
        print(f"Skipped: {album['name']} (File already exists)")
        return

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded cover for {album['name']}")
    else:
        print(f"Failed to download cover for {album['name']}")

def download_worker(album):
    download_album_cover(album, 'album_covers')

def main(argv):
    # check if argument is passed
    if len(argv) == 0:
        print ("Please pass the csv file path as an argument")
    else:
        csv_file_path = argv[0]
    
    if not os.path.isfile(csv_file_path):
        print("The file path does not exist.")
        return
    
    if not csv_file_path.endswith('.csv'):
        print("The file is not a csv file.")
        return
    
    # Checks if second arguement is specified
    if len(argv) == 2:
        num_workers = int(argv[1])
    else:
        num_workers = 6

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    access_token = get_access_token(client_id, client_secret)
    
    if not access_token:
        print("Failed to authenticate with the Spotify API.")
        return
    
    artist_album_names = read_artist_album_names_from_csv(csv_file_path)
    print(artist_album_names)

    # Create the output folder if it doesn't exist
    os.makedirs('album_covers', exist_ok=True)

    print(f"Beginning task with {num_workers} workers.")

    # Using ThreadPoolExecutor to download album covers concurrently
    with ThreadPoolExecutor(num_workers) as executor:
        for artist, album_name in artist_album_names:
            albums = search_albums(artist, album_name, access_token)
            if albums:
                executor.submit(download_worker, albums[0])

if __name__ == "__main__":
    main(sys.argv[1:])