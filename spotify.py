from helper import titleCleanup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from fuzzywuzzy import fuzz


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
    print("searching ,", titleCleanup(track_name), "on spotify ")
    try:
        result = sp.search(titleCleanup(track_name))
        topSongId = -1
        topSongRatio = 0
        for song in result["tracks"]["items"]:
            song_id = song["id"]
            song_name = song["name"]
            r = fuzz.ratio(song_name.lower(), titleCleanup(track_name).lower())
            if(r >= topSongRatio):
                topSongId = song_id
                topSongRatio = r
        print("top song ratio : ", topSongRatio)
        if(topSongRatio < 50):
            return -1
        return topSongId
    except:
        return -1


def addSongToSpotifyPlaylist(sp, spotify_playlist_id, spotify_song_id):
    sp.playlist_add_items(spotify_playlist_id, [spotify_song_id])


def createSpotifyPlaylist(sp, playlist_title):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(
        user_id, playlist_title, description="#sync")
    return playlist


def searchSpotifyPlaylist(sp, playlist_title):
    res = sp.current_user_playlists()
    playlist_id = False
    for item in res["items"]:
        if(item["name"] == playlist_title and "#sync" in item["description"]):
            print("linking spotify and youtube playlist")
            playlist_id = item["id"]

    return playlist_id
