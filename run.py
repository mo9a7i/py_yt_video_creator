# 1.
import os, sys, datetime
from moviepy.editor import *

from sclib import SoundcloudAPI, Track, Playlist
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

# GLOBAL
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


# download a soundcloud audio
api = SoundcloudAPI()
track = api.resolve(sys.argv[1])
assert type(track) is Track
sc_filename = f'./{track.artist} - {track.title}.mp3'
with open(sc_filename, 'wb+') as fp:
    track.write_mp3_to(fp)

# adding the audio and background image together
audio = AudioFileClip(sc_filename)
background = ImageClip(sys.argv[2]).set_duration(audio.duration)
video = background.set_audio(audio)
outfile = f"{os.path.splitext(sc_filename)[0]}.mp4" # 3.
video.write_videofile(outfile, fps=1)

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
# upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'
request_body = {
    'snippet': {
        'categoryI': 19,
        'title': f'{track.artist} - {track.title}',
        'description': 'This video was created automatically by an AI agent by Eng. Dr. MD. Wsaam',
        'tags': ['Travel', 'video test', 'Travel Tips']
    },
    'status': {
        'privacyStatus': 'public',
        'selfDeclaredMadeForKids': False,
    },
    'notifySubscribers': False
}

mediaFile = MediaFileUpload(outfile)

response_upload = service.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=mediaFile
).execute()


service.thumbnails().set(
    videoId=response_upload.get('id'),
    media_body=MediaFileUpload('thumbnail.png')
).execute()

