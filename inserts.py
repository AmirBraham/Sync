from playlist import Playlist
from song import Song


def createPlaylist(session, title, youtube_id=None, spotify_id=None):
    session.add(
        Playlist(title=title, youtube_id=youtube_id, spotify_id=spotify_id))
    session.commit()
