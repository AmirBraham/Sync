from inserts import addSongToPlaylist
from queries import fetchPlaylist
from youtube import fetchYoutubePlaylistSongs, fetchYoutubePlaylists, youtubeAuthentication
from base import Base, engine, Session


Base.metadata.create_all(engine)
session = Session()

youtube = youtubeAuthentication()

youtube_playlists = fetchYoutubePlaylists(youtube)
for youtube_playlist in youtube_playlists:
    playlist = fetchPlaylist(session=session,
                             playlist_title=youtube_playlist["title"], youtube_id=youtube_playlist["id"])
    songs = fetchYoutubePlaylistSongs(
        youtube=youtube, youtube_id=playlist.youtube_id)
    for youtube_song in songs:
        addSongToPlaylist(session=session, playlist=playlist,
                          youtube_id=youtube_song["id"], track_title=youtube_song["title"])
session.close()
