import sys
import spotipy
import spotipy.util as util
import subprocess as sp
import csv

scope = 'user-library-modify playlist-modify-private'
# client_id = ''
# client_secret = ''
# username = ''
redirect_uri = 'http://localhost:8888'  # Setup the call back you want to
playlist_name = 'x'


def createTemporaryServer():
    print("Starting Temporary Server")
    s = sp.Popen(['python', 'redirectServer.py'], shell=True)
    return s


def closeTemporaryServer(server):
    print("Closing Temporary Server")
    sp.Popen.terminate(server)


def createPlaylist(spManager, username):
    playlist = spManager.user_playlist_create(username, playlist_name, False)
    return playlist['id']


def searchTrack(spManager, tracksList, name, artist):
    song_str = name + ' by ' + artist
    res = spManager.search(q='artist:' + artist + ' track:' + name, type="track")

    tracks = res['tracks']['items']

    if len(tracks) < 1:
        print(song_str + " not found!")
        return

    track = res['tracks']['items'][0]
    tracksList.append(track['id'])
    print(song_str + ' added.')
    return


def csvParse(spManager, tracks, filename):
    try:
        parseFile = open(filename)
    except IOError:
        print("File Doesn't exist. Quitting script..")
        sys.exit()
    try:
        reader = csv.reader(parseFile)
        for row in reader:
            if row[0].strip() == '' or row[1].strip() == '':
                print("Error in CSV! Missing data! Skipping row")
            else:
                searchTrack(spManager, tracks, row[0], row[1])
    finally:
        parseFile.close()


def main():
    global playlist_name
    playlist_name = input("Enter playlist name:")
    filename = 'songs.csv'
    server = createTemporaryServer()
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
    closeTemporaryServer(server)

    if token:
        tracks = []
        spManager = spotipy.Spotify(auth=token)
        csvParse(spManager, tracks, filename)

        if len(tracks) > 0:
            playlistID = createPlaylist(spManager, username)
            # playlistID = 'copy paste your playlistID, if you want to add songs in existing playlist'
            spManager.user_playlist_add_tracks(username, playlistID, tracks)
            print("Playlist created!")
        else:
            print("No songs found!")
    else:
        print("Can't get token for", username)


if __name__ == '__main__':
    main()
