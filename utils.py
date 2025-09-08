import os

def clean_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def ensure_download_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
