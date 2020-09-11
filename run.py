# 1.
import os, sys, datetime, requests
from moviepy import video as my_video_py
from moviepy.editor import *
from sclib import SoundcloudAPI, Track, Playlist
from Google import Create_Service
from googleapiclient.http import MediaFileUpload

# Sample:
# py .\run.py 1 https://soundcloud.com/free-beats-io/out-of-sadness "https://vod-progressive.akamaized.net/exp=1599861906~acl=%2Fvimeo-prod-skyfire-std-us%2F01%2F4371%2F14%2F371855028%2F1544389777.mp4~hmac=814872fd8704ccd9196e70f65c5fc493e61408cf4dc7bbe625b7ee6107b326d7/vimeo-prod-skyfire-std-us/01/4371/14/371855028/1544389777.mp4?download=1&filename=MyFileName.mp4"

# GLOBAL - Common
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# Take from the user argument 1, either 1 image, 2 video, 3 visuallizer, based on the input, excute a certain function
# Take from the user argument 2, the value for argument 1 selection
# Take from the user argument 3, input, what type of song provider, 1 soundcloud, 2 youtube, 3 spotify
# Take from the user argument 4, the url of the sound

TYPE_OF_BACKGROUND = sys.argv[1]
BACKGROUND_URL = sys.argv[2]
TYPE_OF_SOUND = sys.argv[3]
SOUND_URL = sys.argv[4]

print(TYPE_OF_BACKGROUND)
print(BACKGROUND_URL)
print(TYPE_OF_SOUND)
print(SOUND_URL)

AUDIO = ""
BACKGROUND = ""
SOUND_FILE_NAME = ""
TRACK_ARTIST = ""
TRACK_TITLE = ""
VIDEO_FPS = 30

def upload_file(outfile):
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'
    request_body = {
        'snippet': {
            'categoryI': 19,
            'title': 'My Python Uploaded Music Video',
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
    #service.thumbnails().set(
    #    videoId=response_upload.get('id'),
        # media_body=MediaFileUpload('thumbnail.png')
    #).execute()
    print("Uploaded successfully")

def download_video(BACKGROUND_URL):
    r = requests.get(BACKGROUND_URL, allow_redirects=True)
    background_file_name = "working_directory/source_files/INPUT_VIDEO.mp4"
    open(background_file_name, 'wb').write(r.content)
    return VideoFileClip(background_file_name)

def download_image(BACKGROUND_URL):
    r = requests.get(BACKGROUND_URL, allow_redirects=True)
    background_file_name = "working_directory/source_files/INPUT_VIDEO.mp4"
    open(background_file_name, 'wb').write(r.content)
    return background_file_name

def download_soundcloud(SOUND_URL):
    global TRACK_ARTIST
    global TRACK_ARTIST
    global SOUND_FILE_NAME

    soundcolud_api = SoundcloudAPI()
    track = soundcolud_api.resolve(SOUND_URL)
    assert type(track) is Track

    TRACK_ARTIST = track.artist
    TRACK_TITLE = track.title
    SOUND_FILE_NAME = 'working_directory/source_files/SOURCE_SOUND.mp3'
    print(SOUND_FILE_NAME)
    with open(SOUND_FILE_NAME, 'wb+') as fp:
        track.write_mp3_to(fp)

def execute(TYPE_OF_BACKGROUND, BACKGROUND_URL, TYPE_OF_SOUND, SOUND_URL):
    global BACKGROUND

    if TYPE_OF_SOUND == "1":
        # it is Soundcloud
        download_soundcloud(SOUND_URL)
        # download a soundcloud audio
    elif TYPE_OF_SOUND == "2":
        # it is youtube
        print("Invalid selection of AUDIO type 2")
    elif TYPE_OF_SOUND == "3":
        # it is spotify
        print("Invalid selection of AUDIO type 3")
    else:
        print("Invalid selection of sound provider")
        sys.exit()


    # Get the Audio
    AUDIO = AudioFileClip(SOUND_FILE_NAME)
    print(AUDIO.duration)
    AUDIO_DURATION = AUDIO.duration


    if TYPE_OF_BACKGROUND == "1":
        # it is an image
        BACKGROUND_Filename = download_image(BACKGROUND_URL)
        BACKGROUND = ImageClip(BACKGROUND_Filename).set_duration(AUDIO_DURATION)
        print("IAM HERE")
    elif TYPE_OF_BACKGROUND == "2":
        # it is a video
        BACKGROUND = download_video(BACKGROUND_URL)
    elif TYPE_OF_BACKGROUND == "3":
        # it is a visuallizer
        print("Invalid selection of background type 3")
    else:
        print("Invalid selection of background type else")
        sys.exit()


    # Based on the type of background, set the duration for the background
    if TYPE_OF_BACKGROUND == "1":
        # it is an image
        # BACKGROUND.set_duration(AUDIO_DURATION)
        print("Invalid selection of background type 1")
    elif TYPE_OF_BACKGROUND == "2":
        # it is a video
        SOUND_DURATION = AUDIO.duration
        BACKGROUND_DURATION = BACKGROUND.duration
        REPEAT_TIMES = SOUND_DURATION / BACKGROUND_DURATION
        BACKGROUND.set_duration(AUDIO.duration)
        BACKGROUND = my_video_py.fx.all.loop(BACKGROUND, n=REPEAT_TIMES, duration=None)
        BACKGROUND.set_duration(AUDIO.duration)
    elif TYPE_OF_BACKGROUND == "3":
        # it is a visuallizer
        print("Invalid selection of background type")
    else:
        print("Invalid selection of background type")
        sys.exit()


    # Merge all together

    print(type(AUDIO_DURATION))

    BACKGROUND.set_audio(AUDIO)
    OUT_FILE_NAME = "working_directory/destination_files/OUTPUT_FILE.mp4"
    BACKGROUND.write_videofile(OUT_FILE_NAME, fps=VIDEO_FPS)


    # Upload to youtube
    upload_file(OUT_FILE_NAME)


# Run the tiddied functions
execute(TYPE_OF_BACKGROUND, BACKGROUND_URL, TYPE_OF_SOUND, SOUND_URL)

sys.exit()
