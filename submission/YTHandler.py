from pytube import YouTube
import os
import google_auth_oauthlib.flow
import googleapiclient.errors
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YThandler:
    def __init__(self):
        self.__dict__['_YThandler__handlers'] = {}

    def download(self, link):
        yt = YouTube(link)
        mp4_files = yt.streams.filter(file_extension="mp4")
        mp4_720p_files = mp4_files.get_by_resolution("720p")
        return mp4_720p_files.download()

    def upload(self, video_file, title, desc):
        CLIENT_SECRETS_FILE = "submission/Credentials/client_secret_328977920138-f584r71j9fse29l4rb09ufrllkghnftb.apps.googleusercontent.com.json"
        API_NAME = "youtube"
        API_VERSION = "v3"
        SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

        # Replace with the path to your video file
        VIDEO_FILE = video_file

        # Authorize the API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server()
        youtube = build(API_NAME, API_VERSION, credentials=credentials)

        # Upload the video
        media = MediaFileUpload(VIDEO_FILE)
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": desc
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=media
        )
        response = request.execute()
        print(response)
