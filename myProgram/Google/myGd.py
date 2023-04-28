import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
import os
from pytube import YouTube

# set up the credentials flow
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    '/home/midnight-wrangler/Documents/CS6348/myProgram/Credentials/client_secret_328977920138-f584r71j9fse29l4rb09ufrllkghnftb.apps.googleusercontent.com.json', scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

# authorize the user
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)

# the URL of the video to download
url = 'https://www.youtube.com/watch?v=1eI8HpJtq-s'

# download the video using PyTube
yt = YouTube(url)
stream = yt.streams.get_highest_resolution()
stream.download()

print('Video downloaded successfully!')