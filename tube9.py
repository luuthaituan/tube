import os
import yt_dlp
from tkinter import *
from tkinter import messagebox, ttk
from threading import Thread
from urllib.parse import urlparse, parse_qs
from ttkthemes import ThemedTk
from tkinter.ttk import Progressbar

# Global variable to control the download thread
download_stopped = False
download_paused = False

def validate_url(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.netloc != 'www.youtube.com':
            return False
        if 'v' not in parse_qs(parsed_url.query):
            return False
        return True
    except Exception:
        return False

def validate_path(path):
    return os.path.isdir(path)

def stop_download():
    global download_stopped
    download_stopped = True

def pause_resume_download():
    global download_paused
    download_paused = not download_paused

def download_video_thread():
    global download_stopped, download_paused

    video_url = url_entry.get()
    output_path = path_entry.get()
    quality = quality_var.get()

    if not video_url or not output_path or not validate_url(video_url) or not validate_path(output_path):
        messagebox.showerror("Error", "Please check your inputs")
        return

    try:
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': quality,
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        messagebox.showinfo("Success", "Video downloaded successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def download_video():
    global download_stopped, download_paused

    download_stopped = False
    download_paused = False

    download_thread = Thread(target=download_video_thread)
    download_thread.start()

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass

def my_hook(d):
    global download_stopped, download_paused

    if download_stopped:
        pbar['value'] = 0
        raise yt_dlp.DownloadError("Download stopped by user")

    if download_paused:
        # Simulate a pause by sleeping
        while download_paused:
            pass

    if d['status'] == 'downloading':
        percent = d.get('percent', None)
        if percent is not None:
            pbar['value'] = int(percent)
        else:
            percent_str = ''.join(c for c in d['_percent_str'] if c.isdigit() or c == '.')
            try:
                pbar['value'] = int(float(percent_str))
            except (ValueError, TypeError):
                pbar['value'] = 0

root = ThemedTk(theme="vista")

# Title
Label(root, text="YouTube Video Downloader", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)

# Video URL
Label(root, text="Video URL:").grid(row=1, column=0, sticky=E)
url_entry = Entry(root, width=50)
url_entry.grid(row=1, column=1)

# Output Path
Label(root, text="Output Path:").grid(row=2, column=0, sticky=E)
path_entry = Entry(root, width=50)
path_entry.grid(row=2, column=1)

# Quality
Label(root, text="Quality:").grid(row=3, column=0, sticky=E)
quality_var = StringVar(root)
quality_var.set("best")
OptionMenu(root, quality_var, "best", "worst").grid(row=3, column=1)

# Download Button
Button(root, text="Download", command=download_video).grid(row=4, column=0, columnspan=2, pady=10)

# Progress Bar
pbar = Progressbar(root, length=400, mode='determinate')
pbar.grid(row=5, column=0, columnspan=2, pady=10)

# Stop Button
stop_button = ttk.Button(root, text="Stop", command=stop_download)
stop_button.grid(row=6, column=0, pady=5)

# Pause/Resume Button
pause_resume_button = ttk.Button(root, text="Pause/Resume", command=pause_resume_download)
pause_resume_button.grid(row=6, column=1, pady=5)

root.mainloop()
