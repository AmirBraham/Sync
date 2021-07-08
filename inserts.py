from playlist import Playlist
from song import Song
from base import Base, engine, Session

Base.metadata.create_all(engine)
session = Session()

indie = Playlist("indie")
song = Song("Illusion Of Seclusion",
            "6gqJJwkvzyXXj8SUEJgP4g?si=8e11fac8fe314f10", "XNftK7U2cYo")

indie.songs = [song]
session.add(indie)

session.commit()
session.close()
