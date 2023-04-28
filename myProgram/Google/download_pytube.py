# # import pytube

# # # Replace with your video ID
# # VIDEO_ID = "ladyKuD0f4M"

# # # Create a YouTube object
# # youtube = pytube.YouTube(f"https://www.youtube.com/watch?v={VIDEO_ID}")

# # # Get the first stream object with both audio and video
# # stream = youtube.streams.filter(progressive=True).first()

# # # Download the video to the current directory
# # stream.download()
from pytube import YouTube

yt = YouTube("https://www.youtube.com/watch?v=Huhzd161X7E")
mp4_files = yt.streams.filter(file_extension="mp4")
mp4_720p_files = mp4_files.get_by_resolution("720p")
mp4_720p_files.download("./downloadedVideo.mp4")

# importing the module
# import pytube

# # Get the video URL
# video_url = "https://www.youtube.com/watch?v=2KknXzalXfg"

# # Create a YouTube object
# youtube = pytube.YouTube(video_url)

# # Get the video stream
# video_stream = youtube.streams.first()

# # Download the video stream to a file
# video_stream.download("my_video.mp4")
