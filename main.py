from queries import fetchPlaylist
from youtube import fetchYoutubePlaylists, youtubeAuthentication
from base import Base, engine, Session


Base.metadata.create_all(engine)
session = Session()

youtube = youtubeAuthentication()

playlists = fetchYoutubePlaylists(youtube)
summerPlaylist = playlists[0]
fetchPlaylist(session=session,
              playlist_title=summerPlaylist["title"], youtube_id=summerPlaylist["id"])
session.close()
