
import argparse
import logging
from library.snippet import Snippet, extract_snippet, extract_multiple_snippets
from library.yt_download import download_youtube_audio
from library.browser_playback import chrome_playback
from library.paths import MP3_FOLDER


def get_and_snip_video(name, url, snippet:Snippet, source_type:str="mp3"):
    fullsong_filepath = MP3_FOLDER / f"{name}.{source_type}"
    if not fullsong_filepath.exists():
        logging.info(f"could not find {fullsong_filepath}")
        download_youtube_audio(url, MP3_FOLDER, name)

    snippet_file_path = MP3_FOLDER/"output" /f"{name}_{int(snippet.start*1000)}_to_{int(snippet.end*1000)}.mp3"
    extract_snippet(fullsong_filepath, snippet, snippet_file_path)

    logging.debug(snippet_file_path)
    chrome_playback(snippet_file_path)


def get_and_snip_video_multiple(name, url, snippets:"list[Snippet]", source_type:str="mp3"):
    fullsong_filepath = MP3_FOLDER / f"{name}.{source_type}"
    if not fullsong_filepath.exists():
        logging.info(f"could not find {fullsong_filepath}")
        download_youtube_audio(url, MP3_FOLDER, name)

    snippet_file_path = MP3_FOLDER/"output" /f"{name}_multipart.mp3"
    extract_multiple_snippets(fullsong_filepath, snippet_file_path, snippets)

    logging.debug(snippet_file_path)
    chrome_playback(snippet_file_path)



if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    get_and_snip_video_multiple(
        "R_20241013-102905", "",
        [
            Snippet(60*16+10, 60*32+45, fade_out=5),
            Snippet(60*36+50, 60*53+4)
        ],
        "wav"
    )
