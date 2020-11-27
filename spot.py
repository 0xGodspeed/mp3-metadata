import spotipy, requests, os
from mutagen.id3 import ID3, TIT2, TRCK, TALB, TPE1, TDRC, APIC, ID3NoHeaderError
from mutagen.mp3 import MP3
from credentials import client_id, client_secret
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

fname = input("File name:") + '.mp3'
search_query = input("Search query: ")
search_query = '+'.join(search_query.split())
a = sp.search(search_query, limit=1, offset=0, type='track', market=None)
song_name = a["tracks"]["items"][0]["name"]
artist_name = a["tracks"]["items"][0]["artists"][0]["name"]
album_name = a["tracks"]["items"][0]["album"]["name"]
album_year = a["tracks"]["items"][0]["album"]["release_date"][0:4]
song_cover = a["tracks"]["items"][0]["album"]["images"][0]["url"]
track_number = str(a["tracks"]["items"][0]["track_number"])
total_tracks = a["tracks"]["items"][0]["album"]["total_tracks"]

print(song_name, album_name, artist_name, album_year, track_number)

audio = MP3(fname, ID3=ID3)

r = requests.get(song_cover, allow_redirects=True)
open('temp.png', "wb").write(r.content)

picture_path = song_cover

try: 
    tags = ID3(fname)
except ID3NoHeaderError:
    print("Adding ID3 header")


tags["TIT2"] = TIT2(encoding=3, text=song_name)
tags["TALB"] = TALB(encoding=3, text=album_name)
tags["TPE1"] = TPE1(encoding=3, text=artist_name)
tags["TDRC"] = TDRC(encoding=3, text=album_year)
tags["TRCK"] = TRCK(encoding=3, text=track_number)
audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data=open('temp.png','rb').read()))


audio.save()
tags.save(fname)
os.rename(fname, f"{track_number} {song_name}.mp3")
