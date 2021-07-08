from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from base import Base


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    songs = relationship("Song", backref="playlists")

    def __init__(self, title):
        self.title = title
