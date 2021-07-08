from re import S
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from base import Base


class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    spotify_id = Column(String)
    youtube_id = Column(String)
    playlist_id = Column(Integer, ForeignKey("playlists.id"))

    def __init__(self, title, spotify_id=None, youtube_id=None):
        self.title = title
        self.spotify_id = spotify_id
        self.youtube_id = youtube_id

    def addToPlaylist(self, playlistName):
        # Code to add as an entry in database for the specific playlist
        pass

    def removeFromPlaylist(self, playlistName):
        # Code to remove entry from database for the specific playlist
        pass
