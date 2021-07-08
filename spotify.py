from helper import dumpToJson
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

spotify_client_secret = open("spotify_client_secret.json")

SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI = json.load(
    spotify_client_secret).values()
scope = ["playlist-read-private",
         "playlist-modify-private", "user-library-modify", "playlist-modify-public"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID,
                     client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))

''' 
res = sp.current_user_playlists()
search_res = sp.search(q="mxmtoon - blame game", type="track")
track_id = search_res["tracks"]["items"][0]["id"]
sp.playlist_add_items("69D8RPFzuIorGGpFBBFFwC", [track_id])
 '''
