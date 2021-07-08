from sqlalchemy.orm import session
from sqlalchemy.sql.expression import or_
from song import Song
from playlist import Playlist


def fetchPlaylist(session, playlist_title=None, youtube_id=None, spotify_id=None):
    playlistExists = session.query(session.query(Playlist).filter(or_(
        Playlist.youtube_id == youtube_id, Playlist.spotify_id == spotify_id)).exists()).scalar()
    if(playlistExists):
        print("Fetching existing playlist")
        playlist = session.query(Playlist).filter(or_(
            Playlist.youtube_id == youtube_id, Playlist.spotify_id == spotify_id)).all()
        return playlist
    playlist = Playlist(
        playlist_title, youtube_id=youtube_id, spotify_id=spotify_id)
    session.add(playlist)
    session.commit()
    return playlist


def fetchSongs(playlist_id=None, youtube_playlist_id=None, spotify_playlist_id=None):
    playlist = None
    if(playlist_id == None):
        if(youtube_playlist_id != None):
            playlist = session.query(Playlist).filter(
                Playlist.youtube_id == youtube_playlist_id)
        elif(spotify_playlist_id != None):
            playlist = session.query(Playlist).filter(
                Playlist.spotify_id == spotify_playlist_id)
    else:
        playlist = session.query(Playlist).filter(Playlist.id == playlist_id)

    songs = session.query(Song).filter(Song.playlist_id == playlist.id)
    return songs
