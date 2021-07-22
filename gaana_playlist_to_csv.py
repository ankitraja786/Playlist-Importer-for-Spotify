import string

from gaanaparser import gettrackinfo
import csv

name, numtracks, tracks = gettrackinfo('https://gaana.com/playlist/gaana-dj-gaana-international-top-50')

print(name + ' has ' + str(len(tracks)) + ' songs!!')


def chk(e):
    if e.isalnum():
        return True
    elif e == ' ':
        return True
    return False


with open('songs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for song in tracks:
        title = song['title']
        artist = song['artist'].split('#')[0]
        # print(artist)
        album = song['albumtitle']
        artist = ''.join(e for e in artist if chk(e))
        a = [title, artist]
        writer.writerow(a)
