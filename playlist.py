from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from base import Base


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    youtube_id = Column(String)
    spotify_id = Column(String)
    songs = relationship("Song", backref="playlists")

    def __init__(self, title, youtube_id=None, spotify_id=None):
        self.title = title
        self.spotify_id = spotify_id
        self.youtube_id = youtube_id

    def __str__(self):
        super().__str__()
        return "title : {} , spotify_id: {}, youtube_id:{},playlist_id:{}".format(self.title, self.spotify_id, self.youtube_id, self.id)
