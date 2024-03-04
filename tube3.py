import os
import yt_dlp
from tkinter import *
from tkinter import messagebox, filedialog


def download_video():
    video_url = url_entry.get()
    output_path = path_entry.get()
    quality = quality_var.get()

    if not video_url or not output_path:
        messagebox.showerror("Error", "Please enter both URL and output path")
        return

    try:
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': quality
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        messagebox.showinfo("Success", "Video downloaded successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


root = Tk()

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

Button(root, text="Download", command=download_video).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()
