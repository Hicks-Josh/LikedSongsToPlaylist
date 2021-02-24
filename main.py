import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from json.decoder import JSONDecodeError
import spotify_credentials as sc

scope = 'user-read-private playlist-modify-public user-library-read'
username = sc.username
client_id = sc.client_id
client_secret = sc.client_secret
redirect_uri = 'https://www.google.com/callback/'
playlist_id = sc.playlist_id
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

# Erase cache and prompt for user permission
try:
    # token = client_credentials_manager.get_access_token()
    token = util.prompt_for_user_token(username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)  # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)  # add scope
    # token = client_credentials_manager.get_access_token()

# Create spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)

# due to how results gets put into paginated sections,
# and due to the issue where there is a limit to how many
# songs can be moved at a time, every time I get a section
# I immediately upload them
results = spotifyObject.current_user_saved_tracks(offset=0)
tracks = results['items']
while results['next']:
    track_uris = []
    for track in tracks:
        track_uris.append(track['track']['uri'])
        print(track['track']['name'])
    spotifyObject.user_playlist_add_tracks(username, playlist_id,
                                           track_uris)
    
    results = spotifyObject.next(results)
    tracks = results['items']
