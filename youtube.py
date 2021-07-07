import os
import pickle
from google.oauth2 import credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.discovery
from google.auth.transport.requests import Request
import json


def credentialsHandling(scopes):
    credentials = None
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json",
                scopes
            )

            credentials = flow.run_console()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)
    return credentials


def main():
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    credentials = credentialsHandling(scopes)
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    request = youtube.playlists().list(
        part="snippet,contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()
    playlists = [{"id": item["id"], "title": item["snippet"]["title"]}
                 for item in response["items"] if "#sync" in item["snippet"]["description"]]
    print(playlists)
    for playlist in playlists:
        next_page_token = None
        songs = []
        while 1:
            request = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist["id"],
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            songs += [{"id": item["id"], "title": item["snippet"]["title"]}
                      for item in response['items']]
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break

        print(songs)


if __name__ == "__main__":
    main()
