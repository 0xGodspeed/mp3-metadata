# mp3-metadata
Adds metadata to mp3 using spotify api and also renames the file

Uses spotify's api to get song title, album name, artist name, track number, release year and album cover.
Uses mutagen to edit metadata of the mp3 file.
Renames the mp3 file to format - "<track number> <track title>"
To add the cover image to the file, it saves the cover png temporarily in the folder.

Requirements - mutagen, spotipy.
