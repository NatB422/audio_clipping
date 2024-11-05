
from dataclasses import dataclass
from pathlib import Path
from pydub import AudioSegment


@dataclass
class Snippet:
    start: float
    end: float
    fade_in: "float|None"=0
    fade_out: "float|None"=0


def extract_snippet(input_path:Path, snippet:Snippet, output_path:Path):

    start_ms = int(snippet.start*1000)
    end_ms = int(snippet.end*1000)

    source = AudioSegment.from_file(input_path.absolute()) # type: AudioSegment

    segment = source[start_ms:end_ms]
    ffmpeg_parameters = []

    fade_parameters = []
    if snippet.fade_in:
        fade_parameters.append(f"afade=t=in:st=0:d={snippet.fade_in}")
    if snippet.fade_out:
        duration = snippet.end - snippet.start
        fade_parameters.append(f"afade=t=out:st={duration - snippet.fade_out}:d={snippet.fade_out}")

    if fade_parameters:
        ffmpeg_parameters.append("-af")
        ffmpeg_parameters.append(",".join(fade_parameters))


    segment.export(str(output_path), format="mp3", parameters=ffmpeg_parameters)
