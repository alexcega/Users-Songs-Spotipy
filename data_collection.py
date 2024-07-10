# data_collection.py
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import config
import time


# Authentication - without user
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.SPOTIPY_CLIENT_ID, client_secret=config.SPOTIPY_CLIENT_SECRET))


def get_track_details(track):
    track_id = track['id']
    features = sp.audio_features(track_id)[0]

    # Combine track info and features into a single dictionary
    track_info = {
        'name': track['name'],
        'album': track['album']['name'],
        'artist': track['artists'][0]['name'],
        'release_date': track['album']['release_date'],
        'track_id': track_id,
        'length': track['duration_ms'],
        'popularity': track['popularity'],
        'acousticness': features['acousticness'],
        'danceability': features['danceability'],
        'energy': features['energy'],
        'instrumentalness': features['instrumentalness'],
        'liveness': features['liveness'],
        'loudness': features['loudness'],
        'speechiness': features['speechiness'],
        'tempo': features['tempo'],
        'time_signature': features['time_signature']
    }
    return track_info

def get_all_liked_songs():
    tracks = []
    limit_step = 40

    tracks = sp.current_user_saved_tracks(limit = limit_step)
    # for offset in range(0, 10000000, limit_step):
    #     response = sp.current_user_saved_tracks(
    #         limit=limit_step,
    #         offset=offset,
    #     )
    #     print(response)
    #     if len(response) == 0:
    #         break
    #     tracks.extend(response)
    return tracks

def get_liked_songs_info():
    results = get_all_liked_songs()
    tracks = []
    
    while results:
        for item in results['items']:
            track = item['track']
            track_info = get_track_details(track)
            tracks.append(track_info)
            time.sleep(0.1)  # Pause to avoid hitting rate limits
        
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    
    return tracks

mysongs = get_all_liked_songs()
print(len(mysongs))


# Fetch liked songs
# liked_songs = get_liked_songs_info()

# Convert to DataFrame
# df = pd.DataFrame(liked_songs)

# Save to CSV
# df.to_csv('liked_songs.csv', index=False)

# print(f"Saved {len(liked_songs)} liked songs to liked_songs.csv")
