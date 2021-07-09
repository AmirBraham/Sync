from helper import dumpToJson, titleCleanup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json


def spotifyAuthentication():
    spotify_client_secret = open("spotify_client_secret.json")

    SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI = json.load(
        spotify_client_secret).values()
    scope = ["playlist-read-private",
             "playlist-modify-private", "user-library-modify", "playlist-modify-public"]
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI))
    return sp


def fetchSpotifyPlaylists(sp):
    res = sp.current_user_playlists()
    playlists = [{"id": item["id"], "title": item["name"]}
                 for item in res["items"] if "#sync" in item["description"]]
    return playlists


def fetchSpotifyPlaylistSongs(sp, spotify_id):
    pl_id = spotify_id
    offset = 0
    res = []
    while True:
        response = sp.playlist_items(pl_id,
                                     offset=offset,
                                     fields='items.track.id,total,items.track.name,items.track.artists',
                                     additional_types=['track'])
        res += response['items']

        if len(response['items']) == 0:
            break
        offset = offset + len(response['items'])
    songs = [{"id": item["track"]["id"], "title": item["track"]["artists"][0]["name"] + " " + item["track"]["name"]}
             for item in res]
    return songs


def searchSongOnSpotify(sp, track_name):
    try:
        result = sp.search(titleCleanup(track_name))
        return result["tracks"]["items"][0]["id"]
    except:
        return -1


def addSongToSpotifyPlaylist(sp, spotify_playlist_id, spotify_song_id):
    sp.playlist_add_items(spotify_playlist_id, [spotify_song_id])


def createSpotifyPlaylist(sp, playlist_title):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(
        user_id, playlist_title, description="#sync")
    return playlist
