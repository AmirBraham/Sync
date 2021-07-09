from sqlalchemy.sql.expression import and_
from playlist import Playlist
from song import Song


def createPlaylist(session, title, youtube_id=None, spotify_id=None):
    playlist = Playlist(title=title, youtube_id=youtube_id,
                        spotify_id=spotify_id)
    session.add(playlist)
    return playlist


def addSongToPlaylist(session, playlist: Playlist, track_title, spotify_id=None, youtube_id=None):
    song = Song(track_title, spotify_id=spotify_id, youtube_id=youtube_id)
    songExists = False
    for s in playlist.songs:
        if((song.spotify_id != None and s.spotify_id == song.spotify_id) or (s.youtube_id == song.youtube_id and song.youtube_id != None)):
            songExists = True
    if(not songExists):
        playlist.songs.append(song)


def deleteSongFromPlaylist(session, playlist: Playlist, song):
    session.query(Song).filter(
        and_(Song.id == song.id, Song.playlist_id == playlist.id)).delete()
