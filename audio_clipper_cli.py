
import argparse
import logging
from library.snippet import Snippet, extract_snippet
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



if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    # get_and_snip_video("Here comes the sun","https://www.youtube.com/watch?v=KQetemT1sWc",Snippet(14,24,fade_out=1))
    get_and_snip_video("The Fear", "https://www.youtube.com/watch?v=7F-lqOrRcIY",Snippet(26.5, 36.4, fade_in=2))
    # get_and_snip_video("Dark Side of the Moon", "https://www.youtube.com/watch?v=n3_5SPQIfQw", Snippet(58, 71, fade_out=1))
    # get_and_snip_video("The Queen is dead", "https://www.youtube.com/watch?v=eubgWMwSD0k", Snippet(59,72, fade_in=1, fade_out=1))
    # get_and_snip_video("Stayin Alive", "https://www.youtube.com/watch?v=fNFzfwLM72c", Snippet(76, 82.5, fade_in=1, fade_out=0.1))
    # get_and_snip_video("News of the World", "https://www.youtube.com/watch?v=Mcc6IZO7di4", Snippet(96, 115, fade_in=2, fade_out=0.5))
    # get_and_snip_video("Daily Mail", "https://www.youtube.com/watch?v=McuHVXgR8dA", Snippet(60, 90, fade_in=1, fade_out=2))
    # get_and_snip_video("Sunday Papers", "https://www.youtube.com/watch?v=BgTcsdltfec", Snippet(36.5, 59.5, fade_in=0.5, fade_out=0.5))
    # get_and_snip_video("Wombling Free", "https://www.youtube.com/watch?v=XWQMMPFtoG4", Snippet(30, 39.2, fade_in=0.5))
    # get_and_snip_video("Mingulay", "", Snippet(8388, 8628))
    #get_and_snip_video("Mingulay Boat Song", "", Snippet(1.2, 236, fade_in=1, fade_out=2))
    # get_and_snip_video("R_20241006-104333", "", Snippet(36*60+9, 62*60+46), source_type="wav")
    # get_and_snip_video("Gal 4 Sho C-D", "", Snippet(29*60+4, 74*60+1), source_type="wav")
