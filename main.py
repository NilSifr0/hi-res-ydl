import os
import subprocess
from time import sleep

import ffmpeg
import PySimpleGUI as sg
from pytubefix import YouTube

# from pytubefix.cli import on_progress


def dl_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    dl_progress_bar(bytes_downloaded, total_size)
    # percentage_of_completion = bytes_downloaded / total_size * 100
    # print(f"{round(percentage_of_completion, 2)} %")


def dl_progress_bar(bytes_downloaded, total_size):
    dl_pb.update(bytes_downloaded, total_size)


def pull_stream(yt_url, status):
    status.update("Status: Downloading")
    yt = YouTube(yt_url, on_progress_callback=dl_progress)
    # get highest quality of video and audio
    # video_stream = (
    #     yt.streams.filter(
    #         adaptive="True",
    #         only_video="True",
    #         file_extension="mp4",
    #     )
    #     .order_by("resolution")
    #     .desc()
    #     .first()
    # )

    video_stream = yt.streams.filter(
        adaptive=True,
        only_video=True,
        file_extension="mp4",
        resolution="2160p",
        fps=60,
    ).first()
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

    status.update("Status: Compiling")

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


def process_stream(video_input, audio_input, title, status):
    sleep(10)
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
        [sg.Text("Status: ", k="-STATUS-")],
        [
            sg.ProgressBar(
                k="-DLP-",
                expand_x=True,
                orientation="h",
                max_value=None,
                bar_color=("DeepSkyBlue", "azure"),
                s=(0, 20),
            )
        ],
    ]

    window = sg.Window("HR-YDL", layout)

    status = window["-STATUS-"]
    global dl_pb
    dl_pb = window["-DLP-"]

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-GET-":
            output_directory()
            video_input, audio_input, title = pull_stream(
                values["-URL-"],
                status,
            )

            process_stream(video_input, audio_input, title, status)
            window["-STATUS-"].update("Status: Done")
        else:
            pass

    window.close()


if __name__ == "__main__":
    app_interface()
