import os

download_path = os.path.join(os.getcwd(), "download")

if not os.path.exists(download_path):
    os.mkdir(download_path)