import os
import subprocess

import ffmpeg
import PySimpleGUI as sg
from pytubefix import YouTube
from pytubefix.cli import on_progress


def pull_stream(yt_url):
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
    video_input = video_stream.download()
    audio_input = audio_stream.download()
    title = yt.title
    return video_input, audio_input, title


def output_directory():
    output_path = r".\outputs"
    if not os.path.exists(output_path):
        os.makedirs(output_path)


def clean_input(v_stream, a_stream):
    try:
        os.remove(v_stream)
        os.remove(a_stream)
    except OSError as e:
        print(f"Error: {e.filename} {e.strerror}")


def process_stream(video_input, audio_input, title):
    v_input = ffmpeg.input(video_input).node.short_repr
    a_input = ffmpeg.input(audio_input).node.short_repr
    input_str = f'-i "{v_input}" -i "{a_input}"'
    codec = "copy"
    out_dir = ".\\outputs\\"

    # process inputs using ffmpeg via subprocess
    command = f'ffmpeg {input_str} -c {codec} -y "{out_dir}{title}.mp4"'
    subprocess.run(command)
    clean_input(v_input, a_input)


def app_interface():
    sg.theme("Dark Grey 15")
    layout = [
        [
            sg.Text("URL:  "),
            sg.Input(do_not_clear=False, k="-URL-"),
            sg.Button("Get", k="-GET-"),
        ],
    ]

    window = sg.Window("HR-YDL", layout)

    # sg.theme_previewer()
    # theme_list = sg.theme_list()
    # print(theme_list)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-GET-":
            output_directory()
            video_input, audio_input, title = pull_stream(values["-URL-"])
            process_stream(video_input, audio_input, title)

    window.close()


if __name__ == "__main__":
    app_interface()
