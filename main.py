from inserts import addSongToPlaylist
from queries import fetchPlaylist
from youtube import addSongToYoutubePlaylist, fetchYoutubePlaylistSongs, fetchYoutubePlaylists, searchSongOnYoutube, youtubeAuthentication
from base import Base, engine, Session


Base.metadata.create_all(engine)
session = Session()

youtube = youtubeAuthentication()

youtube_playlists = fetchYoutubePlaylists(youtube)
for youtube_playlist in youtube_playlists:
    playlist = fetchPlaylist(session=session,
                             playlist_title=youtube_playlist["title"], youtube_id=youtube_playlist["id"])
    playlist_songs = playlist.songs
    youtube_playlist_songs = fetchYoutubePlaylistSongs(
        youtube=youtube, youtube_id=playlist.youtube_id)

    # add songs from db to youtube playlist
    for song in playlist_songs:
        if song.youtube_id == None:
            songId = searchSongOnYoutube(
                youtube=youtube, track_name=song.title)
            addSongToYoutubePlaylist(
                youtube=youtube, youtube_playlist_id=youtube_playlist["id"], youtube_song_id=songId)
            song.youtube_id = songId
    # add songs from youtube playlist to db
    for youtube_song in youtube_playlist_songs:
        addSongToPlaylist(session=session, playlist=playlist,
                          youtube_id=youtube_song["id"], track_title=youtube_song["title"])
    session.commit()

session.close()
