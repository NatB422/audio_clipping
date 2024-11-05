import glob
import os
import shutil

import youtube_dl # client to many multimedia portals


def newest_mp3_filename():
    # lists all mp3s in local directory
    list_of_mp3s = glob.glob('./*.mp3')
    # returns mp3 with highest timestamp value
    return max(list_of_mp3s, key = os.path.getctime)


# downloads yt_url to the same directory from which the script runs
def download_audio(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])


def run():
    url = "https://www.youtube.com/watch?v=WfTdNusm99Q"
    download_audio(url)
    filename = newest_mp3_filename()
    from library.paths import MP3_FOLDER
    dest = MP3_FOLDER / "Mingulay.mp3"
    shutil.move(filename, dest)

if __name__ == "__main__":
    run()
