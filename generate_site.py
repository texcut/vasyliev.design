import os
import requests

# Fetch credentials from environment variables
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']
ALBUM_ID = os.environ['ALBUM_ID']

def get_access_token():
    response = requests.post(
        'https://oauth2.googleapis.com/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': 'refresh_token',
        }
    )
    response.raise_for_status()
    access_token = response.json()['access_token']
    print("Access Token:", access_token)  # Add this line
    return access_token

def get_album_photos(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
    photos = []
    next_page_token = None

    while True:
        data = {
            'albumId': ALBUM_ID,
            'pageSize': 100,
            'pageToken': next_page_token
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        photos.extend(result.get('mediaItems', []))
        next_page_token = result.get('nextPageToken')
        if not next_page_token:
            break
    return photos

def generate_html(photos):
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>My Google Photos Album</title>
    <style>
        img { width: 200px; margin: 10px; }
        body { font-family: Arial, sans-serif; text-align: center; }
        .gallery { display: flex; flex-wrap: wrap; justify-content: center; }
    </style>
</head>
<body>
    <h1>My Google Photos Album</h1>
    <div class="gallery">
'''
    for photo in photos:
        base_url = photo['baseUrl']
        img_url = f"{base_url}=w400-h300"  # Adjust as needed
        alt_text = photo.get('filename', 'Photo')
        html_content += f'        <img src="{img_url}" alt="{alt_text}">\n'

    html_content += '''    </div>
</body>
</html>'''
    return html_content

def main():
    access_token = get_access_token()
    photos = get_album_photos(access_token)
    html_content = generate_html(photos)

    with open('palms.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    main()