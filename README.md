# hi-res-ydl

This project aims to create a simple yt vid downloader. The videos shall be of  
the highest quality and at the same time the lowest file size.  It uses `pytubefix`  
to pull yt vids then process them using `ffmpeg`. The interface is  displayed  
using `pysimplegui`.

## TODO

1. Search Bar
Include a search bar and display the results. The results should show the  
the title, channel name, date, views, and thumbnail. It should also include  
a function to allow downloading. (This implies that the download function  
will be revised to cater this change.)

2. Sort Options
The results should be able to be ordered in terms of time, view count, etc.

3. Filter Options
Include filters for date, resolution, and other important categories.

4. Threads

5. FFMPEG progress bar
The post-processing of the video and audio output should show a progress indicator.  
Note. This task has low prio since most of the time, post-processing happens in  
under 1 second if the codecs and containers are left unchanged.  
