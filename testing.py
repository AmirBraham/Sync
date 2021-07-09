from base import Base, engine, Session
from youtube import createYoutubePlaylist, youtubeAuthentication

Base.metadata.create_all(engine)
session = Session()

youtube = youtubeAuthentication()
p = createYoutubePlaylist(youtube=youtube, playlist_title="new")
print(p)
