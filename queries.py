from sqlalchemy.orm import session
from song import Song
from playlist import Playlist
from base import Session

session = Session()
playlists = session.query(Playlist).all()
for playlist in list(playlists):
    print(playlist.title)
