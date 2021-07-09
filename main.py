from spotify import addSongToSpotifyPlaylist, createSpotifyPlaylist, fetchSpotifyPlaylistSongs, fetchSpotifyPlaylists, searchSongOnSpotify, spotifyAuthentication
from inserts import addSongToPlaylist, deleteSongFromPlaylist
from queries import fetchPlaylist
from youtube import addSongToYoutubePlaylist, createYoutubePlaylist, fetchYoutubePlaylistSongs, fetchYoutubePlaylists, searchSongOnYoutube, youtubeAuthentication
from base import Base, engine, Session


Base.metadata.create_all(engine)
session = Session()

youtube = youtubeAuthentication()
youtube_playlists = fetchYoutubePlaylists(youtube)
spotify = spotifyAuthentication()
spotify_playlists = fetchSpotifyPlaylists(spotify)

# create new playlists in youtube and spotify
for youtube_playlist in youtube_playlists:
    playlist = fetchPlaylist(session=session,
                             playlist_title=youtube_playlist["title"], youtube_id=youtube_playlist["id"])
    spotify_playlist = None
    if(playlist.spotify_id == None):
        spotify_playlist = createSpotifyPlaylist(
            sp=spotify, playlist_title=playlist.title)
        playlist.spotify_id = spotify_playlist["id"]
    session.commit()

for spotify_playlist in spotify_playlists:
    playlist = fetchPlaylist(
        session=session, playlist_title=spotify_playlist["title"], spotify_id=spotify_playlist["id"])
    youtube_playlist = None
    if(playlist.youtube_id == None):
        youtube_playlist = createYoutubePlaylist(
            youtube=youtube, playlist_title=playlist.title
        )
        playlist.youtube_id = youtube_playlist["id"]
    session.commit()

youtube_playlists = fetchYoutubePlaylists(youtube)
spotify_playlists = fetchSpotifyPlaylists(spotify)

for youtube_playlist in youtube_playlists:
    playlist = fetchPlaylist(session=session,
                             playlist_title=youtube_playlist["title"], youtube_id=youtube_playlist["id"])
    playlist_songs = playlist.songs
    youtube_playlist_songs = fetchYoutubePlaylistSongs(
        youtube=youtube, youtube_id=playlist.youtube_id)

    # add songs from db to youtube playlist
    for song in playlist_songs:
        if song.youtube_id == None:
            print("searchnig song on youtube ", song)
            songId = searchSongOnYoutube(
                youtube=youtube, track_name=song.title)
            if(songId == -1):
                continue
            youtube_playlistItemId = addSongToYoutubePlaylist(
                youtube=youtube, youtube_playlist_id=youtube_playlist["id"], youtube_song_id=songId)
            song.youtube_id = songId
            song.youtube_playlistItemId = youtube_playlistItemId
        else:
            # checking for deletion
            SongExists = False
            for s in youtube_playlist_songs:
                if(s["id"] == song.youtube_id):
                    SongExists = True
            if(not SongExists):
                print("deleting song ", song, playlist)
                deleteSongFromPlaylist(
                    session=session, youtube=youtube, sp=spotify, playlist=playlist, song=song)

                # add songs from youtube playlist to db
    for youtube_song in youtube_playlist_songs:
        addSongToPlaylist(playlist=playlist,
                          youtube_id=youtube_song["id"], youtube_playlistItemId=youtube_song["youtube_playlistItemId"], track_title=youtube_song["title"])
    session.commit()

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
                sp=spotify, track_name=song.title)

            if(songId == -1):
                continue
            addSongToSpotifyPlaylist(
                sp=spotify, spotify_playlist_id=spotify_playlist["id"], spotify_song_id=songId)
            song.spotify_id = songId
        else:
            # checking for deletion
            SongExists = False
            for s in spotify_playlist_songs:
                if(s["id"] == song.spotify_id):
                    SongExists = True
            if(not SongExists):
                print("deleting song ", song, playlist)
                deleteSongFromPlaylist(
                    session=session, youtube=youtube, sp=spotify, playlist=playlist, song=song)
    # add songs from spotify playlist to db
    for spotify_song in spotify_playlist_songs:
        addSongToPlaylist(playlist=playlist,
                          spotify_id=spotify_song["id"], track_title=spotify_song["title"])
    session.commit()
session.close()
