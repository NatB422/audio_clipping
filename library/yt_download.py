
import logging
from pathlib import Path
from pytube import YouTube, Stream, monostate, extract


def download_youtube_audio(yt_url:str, output_folder:Path, filename:str):

    yt = YouTube(yt_url)
    logging.info(yt_url, extract.playability_status(yt.watch_html))
    try:
        yt.streams
    except Exception as e:
        logging.warning(e)

    all_formats = yt.streaming_data["adaptiveFormats"]
    audio_stream = [f for f in all_formats if "audio" in f["mimeType"]]

    for yt_audio_dict in audio_stream:
        try:
            yt_audio_stream = Stream(yt_audio_dict, monostate.Monostate(None, None))
            break
        except Exception:
            continue
    else:
        raise Exception("No compatible audio stream found")

    output = yt_audio_stream.download(
        output_path=output_folder,
        filename=f"{filename}.mp3",
    )
    return output
