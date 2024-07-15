from flask import Flask, request, render_template
import pytubefix
from pytubefix import Playlist
import os

app = Flask(__name__)

path = ""

def downloadVideo(url):
    videoStream = pytubefix.YouTube(url).streams
    print("Downloading:", videoStream[0].title)
    pytubefix.YouTube(url).streams.get_highest_resolution().download(path)
    print("Downloaded:",videoStream[0].title, "🔥 successfully!")

def downloadPlaylist(url):
    playlist = Playlist(url)
    totalVideoCount = len(playlist.videos)
    os.mkdir("YoutubePlaylist")
    for index, video in enumerate(playlist.videos, start=1):
        print("Downloading:", video.title)
        video_size = video.streams.get_highest_resolution().filesize
        print("Size:", video_size // (1024 ** 2), " MB")
        video.streams.get_highest_resolution().download("./YoutubePlaylist")
        print("Downloaded:", video.title, "🔥 successfully!")
        print("Remaining Videos:", totalVideoCount - index)
    print("All videos downloaded successfully! 🥳")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download_video', methods=['POST'])
def download_video():
    url = request.form['url']
    downloadVideo(url)
    return "Video downloaded successfully!"

@app.route('/download_playlist', methods=['POST'])
def download_playlist():
    url = request.form['url']
    downloadPlaylist(url)
    return "Playlist downloaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)