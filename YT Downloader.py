# Playlists are accepted and the whole playlist is downloaded

import tkinter as tk
from tkinter import filedialog
import yt_dlp as youtube_dl # In order to have this script functional you have to apply this patch https://levelup.gitconnected.com/fix-error-unable-to-extract-uploader-id-3fad389322a7

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        location_entry.delete(0, tk.END)
        location_entry.insert(0, directory)

def download_playlist():
    url = entry.get()
    save_location = location_entry.get()
    format_choice = format_var.get()
    audio_quality = quality_var.get()
    video_quality = video_quality_var.get()

    ydl_opts = {
        'ignoreerrors': True,
        'playlistend': 300,  # Limit the number of videos to download (change as needed)
        'outtmpl': save_location + '/%(title)s.%(ext)s',  # Filename template with chosen save location
    }

    if format_choice == "MP3":
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': audio_quality,
        }]
    else:
        ydl_opts['format'] = 'bestvideo[height<={}]+bestaudio/best'.format(video_quality)

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.config(text="Download complete!", fg="green")
    except Exception as e:
        status_label.config(text="Error: " + str(e), fg="red")

# Create the main window
window = tk.Tk()
window.title("YouTube Playlist Downloader")
window.geometry("400x450")
window.configure(bg="#F0F0F0")

# Create the input label and entry
url_label = tk.Label(window, text="Enter YouTube Playlist URL:", bg="#F0F0F0", fg="#333333")
url_label.pack(pady=10)
entry = tk.Entry(window, width=50)
entry.pack()

# Create the save location label, entry, and button
location_label = tk.Label(window, text="Save Location:", bg="#F0F0F0", fg="#333333")
location_label.pack()
location_entry = tk.Entry(window, width=50)
location_entry.pack()
location_button = tk.Button(window, text="Browse", command=select_directory)
location_button.pack(pady=5)

# Create the format selection label and radio buttons
format_label = tk.Label(window, text="Download Format:", bg="#F0F0F0", fg="#333333")
format_label.pack()
format_var = tk.StringVar(value="MP3")
format_radio_mp3 = tk.Radiobutton(window, text="MP3", variable=format_var, value="MP3", bg="#F0F0F0", fg="#333333")
format_radio_mp3.pack()
format_radio_video = tk.Radiobutton(window, text="Video", variable=format_var, value="Video", bg="#F0F0F0", fg="#333333")
format_radio_video.pack()

# Create the audio quality selection label and dropdown menu
quality_label = tk.Label(window, text="Audio Quality:", bg="#F0F0F0", fg="#333333")
quality_label.pack()
quality_var = tk.StringVar(value="192")
quality_dropdown = tk.OptionMenu(window, quality_var, "64", "128", "192", "256", "320")
quality_dropdown.pack()

# Create the video quality selection label and dropdown menu
video_quality_label = tk.Label(window, text="Video Quality:", bg="#F0F0F0", fg="#333333")
video_quality_label.pack()
video_quality_var = tk.StringVar(value="720")
video_quality_dropdown = tk.OptionMenu(window, video_quality_var, "240", "360", "480", "720", "1080", "1440", "2160")
video_quality_dropdown.pack()

# Create the download button
download_button = tk.Button(window, text="Download", command=download_playlist, bg="#4CAF50", fg="#FFFFFF", relief="raised")
download_button.pack(pady=15)

# Create the status label
status_label = tk.Label(window, text="", bg="#F0F0F0", fg="#333333")
status_label.pack()

# Start the main loop
window.mainloop()
