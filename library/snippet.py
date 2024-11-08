
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from pydub import AudioSegment
from pydub.logging_utils import log_subprocess_output


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


def extract_multiple_snippets(input_path:Path, output_path:Path, snippets:"list[Snippet]", part_completion_callback=None):

    total_stages = len(snippets) + 1
    part_filepaths = [] # type: list[Path]
    output_path_for_parts = output_path.parent
    if not output_path_for_parts.exists():
        output_path_for_parts.mkdir()

    # Extract each segment to a new file
    for index, snip in enumerate(snippets, start=1):
        part_filepath = output_path_for_parts / f"{output_path.name}_part{index}.mp3"
        part_filepaths.append(part_filepath)
        extract_snippet(input_path, snip, part_filepath)

        if part_completion_callback:
            completion_percentage = index / total_stages
            part_completion_callback(completion_percentage)


    # Concat the files together
    concat_command = [
        "ffmpeg",
        "-y", # allow overwrite
        "-i", f"concat:{'|'.join(str(p) for p in part_filepaths)}", # input is a concat
        "-c", "copy", # copy
        "-f", "mp3",
        str(output_path)
    ]

    with open(os.devnull, 'rb') as devnull:
        p = subprocess.Popen(concat_command, stdin=devnull, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p_out, p_err = p.communicate()

    # Log in case of error
    log_subprocess_output(p_out)
    log_subprocess_output(p_err)

    # Cleanup
    for part_path in part_filepaths:
        if part_path.exists():
            part_path.unlink()
