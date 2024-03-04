import os
import yt_dlp
from tkinter import *
from tkinter import messagebox, filedialog, scrolledtext
from threading import Thread
from urllib.parse import urlparse, parse_qs
from ttkthemes import ThemedTk
from tkinter.ttk import Progressbar


def validate_url(url):
    # Check if the URL is a valid YouTube video URL
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
    # Check if the path is a valid directory
    return os.path.isdir(path)


def download_video():
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


def my_hook(d):
    if d['status'] == 'downloading':
        pbar['value'] = int(float(d['_percent_str'][:-1]))


def start_download_thread():
    download_thread = Thread(target=download_video)
    download_thread.start()


class MyLogger(object):
    def debug(self, msg):
        output_text.insert(END, msg + '\n')

    def warning(self, msg):
        output_text.insert(END, msg + '\n')

    def error(self, msg):
        output_text.insert(END, msg + '\n')


root = ThemedTk(theme="vista")  # Use the "vista" theme

Label(root, text="YouTube Video Downloader", font=("Helvetica", 20)).grid(row=0, column=0, columnspan=2, pady=10)

Label(root, text="Video URL:").grid(row=1, column=0, sticky=E)
url_entry = Entry(root, width=50)
url_entry.grid(row=1, column=1)

Label(root, text="Output Path:").grid(row=2, column=0, sticky=E)
path_entry = Entry(root, width=50)
path_entry.grid(row=2, column=1)

Label(root, text="Quality:").grid(row=3, column=0, sticky=E)
quality_var = StringVar(root)
quality_var.set("best")
OptionMenu(root, quality_var, "best", "worst").grid(row=3, column=1)

Button(root, text="Download", command=start_download_thread).grid(row=4, column=0, columnspan=2, pady=10)

pbar = Progressbar(root, length=400, mode='determinate')
pbar.grid(row=5, column=0, columnspan=2, pady=10)

output_text = scrolledtext.ScrolledText(root, width=70, height=10)
output_text.grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()