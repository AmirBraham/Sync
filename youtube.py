from helper import titleCleanup
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google.auth.transport.requests import Request


def credentialsHandling(scopes):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file(
            'token.json', scopes=scopes)

    if creds and creds.expired and creds.refresh_token:
        print("refreshing")
        creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", scopes)
        creds = flow.run_console()
        print("creds", creds)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def youtubeAuthentication():
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    credentials = credentialsHandling(scopes)
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)
    return youtube


def fetchYoutubePlaylists(youtube):
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    playlists = [{"id": item["id"], "title": item["snippet"]["title"]}
                 for item in response["items"] if "#sync" in item["snippet"]["description"]]
    return playlists


def fetchYoutubePlaylistSongs(youtube, youtube_id):
    next_page_token = None
    youtube_songs = []
    while 1:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=youtube_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        youtube_songs += [{"id": item["snippet"]["resourceId"]["videoId"], "title": item["snippet"]["title"], "youtube_playlistItemId":item["id"]}
                          for item in response['items']]
        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break
    return youtube_songs


def searchSongOnYoutube(youtube, track_name):
    try:
        request = youtube.search().list(
            part="snippet",
            q=titleCleanup(track_name)
        )
        response = request.execute()
        songId = response["items"][0]["id"]["videoId"]
        return songId
    except:
        return -1


def addSongToYoutubePlaylist(youtube, youtube_playlist_id, youtube_song_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
             'snippet': {
                 'playlistId': youtube_playlist_id,
                 'resourceId': {
                     'kind': 'youtube#video',
                     'videoId': youtube_song_id
                 }
             }
        }
    )
    response = request.execute()
    return response["id"]


def createYoutubePlaylist(youtube, playlist_title):
    playlist = youtube.playlists().insert(
        part="snippet",
        body={
            'snippet': {
                "title": playlist_title,
                "description": "#sync"
            }
        }
    ).execute()
    return playlist


def searchYoutubePlaylist(youtube, playlist_title):
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    playlist_id = False
    for item in response["items"]:
        if(item["snippet"]["title"] == playlist_title and "#sync" in item["snippet"]["description"]):
            print("linking spotify and youtube playlist")
            playlist_id = item["id"]

    return playlist_id


def main():
    pass


if __name__ == "__main__":
    main()
