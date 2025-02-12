import os
import subprocess

import ffmpeg
import PySimpleGUI as sg
from pytubefix import YouTube
from pytubefix.cli import on_progress


# create the interface layout
def app_interface():
    # layout = [
    #     [
    #         sg.Text("Row 1"),
    #         sg.Button("Row 1 - #1"),
    #         sg.Checkbox("Row 1 - #2"),
    #         sg.Button("Row - #3"),
    #     ],
    #     [
    #         sg.Text("Row 2"),
    #         sg.Checkbox("Row 2 - #1"),
    #         sg.Checkbox("Row 2 - #2"),
    #         sg.Checkbox("Row 2 - #3"),
    #     ],
    #     [
    #         sg.Text("Row 3"),
    #         sg.Button("Row 3 - #1"),
    #         sg.Button("Row 3 - #2"),
    #     ],
    # ]
    layout = [
        [
            sg.Text("ROW 1"),
            sg.Button("Row 1 - #1"),
            sg.Checkbox("Row 1 - #2"),
            sg.Button("Row 1 - #3"),
        ],
        [
            sg.Text("ROW 2"),
            sg.Checkbox("Row 2 - #1"),
            sg.Checkbox("Row 2 - #2"),
            sg.Checkbox("Row 2 - #3"),
        ],
        [
            sg.Text("ROW 3"),
            sg.Button("Row 3 - #1"),
            sg.Button("Row 3 - #2"),
        ],
    ]

    window = sg.Window("HR-YDL", layout)
    window.close()


def pull_stream(yt_url):
    """
    This function pulls the yt stream from the input

    :param yt_url: any valid yt url
    :type yt_url: str
    :return: returns the video_stream, audio_stream, and title
    :rtype: StreamQuery, StreamQuery, str
    """

    yt = YouTube(yt_url, on_progress_callback=on_progress)
    # get highest quality of video and audio
    video_stream = (
        yt.streams.filter(
            adaptive="True",
            only_video="True",
            file_extension="mp4",
        )
        .order_by("resolution")
        .desc()
        .first()
    )
    audio_stream = (
        yt.streams.filter(
            adaptive="True",
            only_audio="True",
            file_extension="mp4",
        )
        .order_by("abr")
        .desc()
        .first()
    )
    title = yt.title
    return video_stream, audio_stream, title


def output_directory():
    """
    This function creates output directory if it doesn't exist yet.
    """

    output_path = r".\outputs"
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def clean_input(v_stream, a_stream):
    """
    This function deletes the source stream after using it to free up space.

    :param v_stream: _description_
    :type v_stream: _type_
    :param a_stream: _description_
    :type a_stream: _type_
    """

    try:
        os.remove(v_stream)
        os.remove(a_stream)
    except OSError as e:
        print(f"Error: {e.filename} {e.strerror}")


def process_stream(video_stream, audio_stream, title):
    """
    This function downloads the loaded stream and splits in into two then
    processes the them as input. Deletes them after.

    :param video_stream: the vid stream extracted from pull_stream()
    :type video_stream: StreamQuery
    :param audio_stream: the aud stream extracted from pull_stream()
    :type audio_stream: StreamQuery
    :param title: the yt vid title passed as str
    :type title: str
    """

    video_input = ffmpeg.input(video_stream.download(filename="video.mp4"))
    audio_input = ffmpeg.input(audio_stream.download(filename="audio.mp4"))
    v_input = video_input.node.short_repr
    a_input = audio_input.node.short_repr
    input_str = f"-i {v_input} -i {a_input}"
    codec = "copy"
    out_dir = ".\\outputs\\"

    # process inputs using ffmpeg via subprocess
    command = f'ffmpeg {input_str} -c {codec} -y "{out_dir}{title}.mp4"'
    subprocess.run(command)
    clean_input(video_input.node.short_repr, audio_input.node.short_repr)


if __name__ == "__main__":
    # app_interface()
    layout = [
        [
            sg.Text("ROW 1"),
            sg.Button("Row 1 - #1"),
            sg.Checkbox("Row 1 - #2"),
            sg.Button("Row 1 - #3"),
        ],
        [
            sg.Text("ROW 2"),
            sg.Checkbox("Row 2 - #1"),
            sg.Checkbox("Row 2 - #2"),
            sg.Checkbox("Row 2 - #3"),
        ],
        [
            sg.Text("ROW 3"),
            sg.Button("Row 3 - #1"),
            sg.Button("Row 3 - #2"),
        ],
    ]

    window = sg.Window("HR-YDL", layout)
    event, values = window.read()
    # while True:
    #     event, values = window.read()
    #     if event == sg.WIN_CLOSED or event == "Row 3 - #2":
    #         break
    #     print("test")

    window.close()
    # print("insert yt url:")
    # yt_url = input("URL: ")
    # output_directory()
    # video_stream, audio_stream, title = pull_stream(yt_url)
    # process_stream(video_stream, audio_stream, title)
