from helper import titleCleanup
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from base import Base


class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    spotify_id = Column(String)
    youtube_id = Column(String)
    youtube_playlistItemId = Column(String)
    playlist_id = Column(Integer, ForeignKey("playlists.id"))
    tried_to_sync = Column(Boolean, default=False)

    def __init__(self, title, spotify_id=None, youtube_id=None, youtube_playlistItemId=None, tried_to_sync=False):
        self.title = titleCleanup(title=title)
        self.spotify_id = spotify_id
        self.youtube_id = youtube_id
        self.youtube_playlistItemId = youtube_playlistItemId
        self.tried_to_sync = tried_to_sync

    def __str__(self):
        super().__str__()
        return "title : {} , spotify_id: {}, youtube_id:{},playlist_id:{} ,youtube_playlistItemId:{},tried_to_sync:{}".format(self.title, self.spotify_id, self.youtube_id, self.playlist_id, self.youtube_playlistItemId, self.tried_to_sync)
