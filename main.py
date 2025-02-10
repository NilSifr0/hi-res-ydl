from pytubefix import YouTube
import ffmpeg
import subprocess

yt_url = "url"
yt = YouTube(yt_url)

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

# async def dl_files():
#     async with asyncio.TaskGroup() as tg:
#         task_1 = tg.create_task(
#             ffmpeg.input(video_stream.download(filename="video.mp4"))
#         )
#         task_2 = tg.create_task(
#             ffmpeg.input(audio_stream.download(filename="audio.mp4"))
#         )
# asyncio.run(dl_files())

video_input = ffmpeg.input(video_stream.download(filename="video.mp4"))
audio_input = ffmpeg.input(audio_stream.download(filename="audio.mp4"))
output_file = f"{yt.title}.mp4"


codec = "copy"
title = yt.title
# merge video and audio inputs into output using subprocess
# https://stackoverflow.com/questions/56973205/how-to-combine-the-video-and-audio-files-in-ffmpeg-python
# subprocess.run(f"ffmpeg -i {video_input} -i {audio_input} -c {codec} {output_file}")
# ffmpeg -i video.mp4 -i audio.m4a -c copy testvid.mp4
# command = "ffmpeg -i ", video_input.node.short_repr, ' -i ', audio_input.node.short_repr, ' -c', codec, ' output1.mp4'
command = f"ffmpeg -i {video_input.node.short_repr} -i {audio_input.node.short_repr} -c {codec} output1.mp4"
# subprocess.run(['ffmpeg ', '-i ', video_input, ' -i', audio_input, ' -c', codec, ' output.mp4'])
subprocess.run(command)
# rename_command = f"Rename-Item output.mp4 -NewName {title}.mp4"
# subprocess.run(rename_command)

# ffmpeg.concat(video_input, audio_input, v=1, a=1).output(output_file).run() // expensive solution
