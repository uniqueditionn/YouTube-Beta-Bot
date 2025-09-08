import os
import yt_dlp
from config import DOWNLOAD_PATH
from utils import ensure_download_folder

ensure_download_folder(DOWNLOAD_PATH)

async def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_PATH, "%(title)s.%(ext)s"),
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info).replace(info['ext'], 'mp3')
    return file_path

async def download_video(url):
    ydl_opts = {
        "format": "bestvideo+bestaudio",
        "outtmpl": os.path.join(DOWNLOAD_PATH, "%(title)s.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
    return file_path
