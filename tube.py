import os
import yt_dlp
from tqdm import tqdm


def progress_hook(d):
    if d['status'] == 'downloading':
        pbar.update(d['downloaded_bytes'])


def download_video(video_url, output_path='.'):
    try:
        # Check if the output folder exists, create it if not
        os.makedirs(output_path, exist_ok=True)

        # Initialize the progress bar
        global pbar
        pbar = tqdm(unit='B', unit_scale=True, desc="Downloading")

        # Set up the downloader options
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
        }

        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Close the progress bar
        pbar.close()

        print(f"\nVideo downloaded successfully to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage with user input
video_url = input("Enter the YouTube video URL: ")
output_path = input("Enter the output path (press Enter for default): ") or "C:\\Users\\IT\\Downloads\\videos"
download_video(video_url, output_path)
