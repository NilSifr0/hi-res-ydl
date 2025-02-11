from pytubefix import YouTube
from pytubefix.cli import on_progress
import ffmpeg
import subprocess
import os


# function that process user input url
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
    title = yt.title
    return video_stream, audio_stream, title


# create output directory if it doesnt exist yet
def output_directory():
    output_path = r'.\outputs'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

# clean input files
def clean_input(v_stream, a_stream):
    try:
        os.remove(v_stream)
        os.remove(a_stream)
    except OSError as e:
        print(f"Error: {e.filename} {e.strerror}")

# dowload pulled stream and split it into two
def process_stream(video_stream, audio_stream, title):
    video_input = ffmpeg.input(video_stream.download(filename="video.mp4"))
    audio_input = ffmpeg.input(audio_stream.download(filename="audio.mp4"))
    codec = "copy"
    output_directory = ".\\outputs\\"

    # process inputs using ffmpeg via subprocess
    command = f'ffmpeg -i {video_input.node.short_repr} -i {audio_input.node.short_repr} -c {codec} -y "{output_directory}{title}.mp4"'
    subprocess.run(command)
    clean_input(video_input.node.short_repr, audio_input.node.short_repr)


if __name__ == "__main__":
    print("insert yt url:")
    yt_url = input("URL: ")
    output_directory()
    video_stream, audio_stream, title = pull_stream(yt_url)
    process_stream(video_stream, audio_stream, title)
