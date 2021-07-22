
import re
import requests
import urllib.request
import json


def gettrackinfo(playlisturl):
    trackstart = []
    trackend = []
    playliststart = []
    playlistend = []
    trackdetails = []
    response = urllib.request.urlopen(playlisturl)
    response = response.read().decode('utf-8')
    for a in re.finditer('{"title":', response):
        trackstart.append(a.start())
    for b in re.finditer('} </span>', response):
        trackend.append(b.end())
    for c in re.finditer('{"source":', response):
        playliststart = c.start()
    for d in re.finditer('}</span>', response):
        playlistend = int(d.start()) + 1
    playlistinfo = json.loads(response[playliststart:playlistend])
    numtracks = playlistinfo['trackcount']
    playlistname = playlistinfo['title']
    if len(trackstart) == len(trackend) and numtracks > 0:
        for i in range(0, len(trackstart)):
            j = response[trackstart[i]:trackend[i]]
            j = j[:-7]
            # print(j)
            # k=0
            trackdetails.append(json.loads(j))
    else:
        trackdetails = []
    return playlistname, numtracks, trackdetails
