
import datetime
import json
import logging
from pathlib import Path
import urllib.parse
import requests

from spotdl.utils.config import SPOTIFY_OPTIONS
from spotdl import Downloader, DownloaderOptions, Song, SpotifyClient

from pydub.utils import which
FFMPEG_PATH = which("ffmpeg")

DOWNLOADER = Downloader(DownloaderOptions(ffmpeg=FFMPEG_PATH,format="mp3",))


def initialise():
    """Initialise connection to Spotify
    Can we load ceredentials from local?"""
    # start the cli running?
    spotify_settings = SPOTIFY_OPTIONS
    spotify_settings["user_auth"] = True
    SpotifyClient.init(**spotify_settings)
    logging.info("Initialised Spotify client")


def get_download_link_for_track(track_id:str, cache_folder:Path):

    name, url = load_download_link_from_cache(track_id, cache_folder)
    if url:
        return name, url

    name, url = create_download_link_for_track(track_id)
    save_download_link_to_cache(track_id, name, url, cache_folder)

    return name, url


def save_download_link_to_cache(track_id:str, name: str, url:str, cache_folder:Path):

    query_string = "".join(url.split("?")[1:])
    qs_dict = urllib.parse.parse_qs(query_string)

    expiry_str = qs_dict["expire"]
    if isinstance(expiry_str, list):
        expiry_str = expiry_str[0]

    timestamp = datetime.datetime.fromtimestamp(int(expiry_str))

    save_file = cache_folder / track_id
    with save_file.open("w") as myfile:
        json.dump({
            "track_id": track_id,
            "name": name,
            "url": url,
            "expiry": timestamp.isoformat()
        }, myfile)


def load_download_link_from_cache(track_id:str, cache_folder:Path):
    save_file = cache_folder / track_id
    if not save_file.exists():
        return None, None

    with save_file.open() as myfile:
        contents = json.load(myfile)

    expiry = datetime.datetime.fromisoformat(contents["expiry"])
    if expiry < datetime.datetime.now():
        return None, None

    return contents["name"], contents["url"]


def create_download_link_for_track(track_id:str):

    url = f"https://open.spotify.com/track/{track_id}"

    initialise()

    song = Song.from_url(url)
    data = DOWNLOADER.search(song)
    download_url = DOWNLOADER.audio_providers[0].get_download_metadata(data)["url"]
    return song.name, download_url


def download_song(file_name:str, url:str, download_folder:Path):
    # open in binary mode
    file_path = download_folder / (file_name+".mp3")

    # get request
    response = requests.get(url)

    with file_path.open("wb") as file:
        # write to file
        file.write(response.content)

    return file_path
