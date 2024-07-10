import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import config
import pandas as pd
scope = "user-library-read"

sp_oauth = SpotifyOAuth( client_id    =config.SPOTIPY_CLIENT_ID,
                    client_secret=config.SPOTIPY_CLIENT_SECRET,
                    redirect_uri =config.SPOTIPY_REDIRECT_URI,
                    scope=scope)

sp = spotipy.Spotify(auth_manager=sp_oauth)


# Fetch user's saved tracks (max limit by api call is 50)
track_limit = 50
results = sp.current_user_saved_tracks(limit=track_limit)

# Create a list to store track information
tracks_data = []

# Extract desired information
for item in results['items']:
    track = item['track']
    track_info = {
        'Song Name': track['name'],
        'Artist Name': track['artists'][0]['name'],
        'Album Name': track['album']['name'],
        'Release Date': track['album']['release_date']
    }
    tracks_data.append(track_info)

# Create a DataFrame from the list
df = pd.DataFrame(tracks_data)

# Save the DataFrame to a CSV file
df.to_csv('saved_tracks.csv', index=False)

print("Data has been saved to saved_tracks.csv")
