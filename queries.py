from inserts import createPlaylist
from sqlalchemy.orm import session
from sqlalchemy.sql.expression import and_, or_
from song import Song
from playlist import Playlist


def fetchPlaylist(session, playlist_title="", youtube_id=None, spotify_id=None):
    filterCondition = or_(
        and_(Playlist.youtube_id == youtube_id, Playlist.youtube_id != None), and_(
            Playlist.spotify_id == spotify_id, Playlist.spotify_id != None))
    playlistExists = session.query(session.query(
        Playlist).filter(filterCondition).exists()).scalar()
    if(playlistExists):
        playlist = session.query(Playlist).filter(filterCondition).all()
        return playlist[0]
    playlist = createPlaylist(session=session, title=playlist_title,
                              youtube_id=youtube_id, spotify_id=spotify_id)
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
