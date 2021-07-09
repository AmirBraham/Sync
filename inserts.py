from sqlalchemy.sql.expression import and_
from playlist import Playlist
from song import Song


def createPlaylist(session, title, youtube_id=None, spotify_id=None):
    playlist = Playlist(title=title, youtube_id=youtube_id,
                        spotify_id=spotify_id)
    session.add(playlist)
    session.commit()
    return playlist


def addSongToPlaylist(playlist: Playlist, track_title, spotify_id=None, youtube_id=None, youtube_playlistItemId=None):
    song = Song(track_title, spotify_id=spotify_id, youtube_id=youtube_id,
                youtube_playlistItemId=youtube_playlistItemId)
    songExists = False
    for s in playlist.songs:
        if((song.spotify_id != None and s.spotify_id == song.spotify_id) or (s.youtube_id == song.youtube_id and song.youtube_id != None)):
            songExists = True
    if(not songExists):
        playlist.songs.append(song)


def deleteSongFromPlaylist(session, youtube, sp, playlist: Playlist, song: Song, youtube_playlistItemId=None):
    try:
        sp.playlist_remove_all_occurrences_of_items(
            playlist.spotify_id, song.spotify_id)
        if(youtube_playlistItemId != None):
            youtube.playlistItems().delete(
                id=youtube_playlistItemId
            ).execute()
        session.query(Song).filter(
            and_(Song.id == song.id, Song.playlist_id == playlist.id)).delete()
    except:
        print("could not delete ", song)
