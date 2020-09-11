# 1.
import os, sys
from moviepy.editor import *

from sclib import SoundcloudAPI, Track, Playlist


# Argument 1 is the sound link, argument two is the image filename

print(sys.argv[1])
print(sys.argv[2])


# To Download a soundcloud audio
api = SoundcloudAPI()  # never pass a Soundcloud client ID that did not come from this library

track = api.resolve(sys.argv[1])

assert type(track) is Track

sc_filename = f'./{track.artist} - {track.title}.mp3'

with open(sc_filename, 'wb+') as fp:
    track.write_mp3_to(fp)


# https://soundcloud.com/free-beats-io/out-of-sadness






# 2.
# audio = AudioFileClip(sys.argv[1])
audio = AudioFileClip(sc_filename)
image = ImageClip(sys.argv[2]).set_duration(audio.duration)

video = image.set_audio(audio)
outfile = f"{os.path.splitext(sc_filename)[0]}_with_image.mp4" # 3.

video.write_videofile(outfile, fps=1)

# Use line below if you want to preserve the name of both files.
# 1. outfile = f"{os.path.splitext(sys.argv[1])[0]}_with_image_{os.path.splitext(sys.argv[2])[0]}.mp4"
