from spotify import addSongToSpotifyPlaylist, fetchSpotifyPlaylistSongs, fetchSpotifyPlaylists, searchSongOnSpotify, spotifyAuthentication
from inserts import addSongToPlaylist, deleteSongFromPlaylist
from queries import fetchPlaylist
from youtube import addSongToYoutubePlaylist, fetchYoutubePlaylistSongs, fetchYoutubePlaylists, searchSongOnYoutube, youtubeAuthentication
from base import Base, engine, Session


Base.metadata.create_all(engine)
session = Session()
''' 
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
        else:
            # checking for deletion
            SongExists = False
            for s in youtube_playlist_songs:
                if(s["id"] == song.youtube_id):
                    SongExists = True
            if(not SongExists):
                deleteSongFromPlaylist(
                    session=session, playlist=playlist, song=song)

                # add songs from youtube playlist to db
    for youtube_song in youtube_playlist_songs:
        addSongToPlaylist(session=session, playlist=playlist,
                          youtube_id=youtube_song["id"], track_title=youtube_song["title"])
    session.commit() '''

spotify = spotifyAuthentication()
spotify_playlists = fetchSpotifyPlaylists(spotify)
for spotify_playlist in spotify_playlists:
    playlist = fetchPlaylist(
        session=session, playlist_title=spotify_playlist["title"], spotify_id=spotify_playlist["id"])
    playlist_songs = playlist.songs
    spotify_playlist_songs = fetchSpotifyPlaylistSongs(
        sp=spotify, spotify_id=playlist.spotify_id)
    # add songs from db to spotify playlist
    for song in playlist_songs:
        if song.spotify_id == None:
            songId = searchSongOnSpotify(
                spotify=spotify, track_name=song.title)
            addSongToSpotifyPlaylist(
                spotify=spotify, spotify_playlist_id=spotify_playlist["id"], spotify_song_id=songId)
            song.spotify_id = songId
        else:
            # checking for deletion
            SongExists = False
            for s in spotify_playlist_songs:
                if(s["id"] == song.spotify_id):
                    SongExists = True
            if(not SongExists):
                deleteSongFromPlaylist(
                    session=session, playlist=playlist, song=song)
    # add songs from spotify playlist to db
    for spotify_song in spotify_playlist_songs:
        addSongToPlaylist(session=session, playlist=playlist,
                          spotify_id=spotify_song["id"], track_title=spotify_song["title"])
    session.commit()
session.close()
