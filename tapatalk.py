import re
import requests
from pathlib import Path
import os
import logging
import sys

whole_url_regex = "https://uploads.tapatalk-cdn.com/[0-9]+/[abcdef0-9]+.jpg"
file_regex = "[0-9]+/[abcdef0-9]+.jpg"
download_path = "./downloads/"
log_file = "./tapatalk.log"
input_file = "./tapatalkposts.input"

file_handler = logging.FileHandler(filename=log_file)
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [file_handler, stdout_handler]
logging.basicConfig(handlers=handlers, level=logging.ERROR)

with open(input_file, 'r') as file:
    posts = file.read().replace('\n', '')

urls = re.findall(whole_url_regex, posts)

for url in urls:
    file_path = download_path + re.findall(file_regex, url)[0]
    file = Path(file_path)
    if file.exists():
        print("File " + file_path + " already exists. Not downloading.")
    else:
        print("File " + file_path + " not found. Downloading.")
        result = requests.get(url)
        if result.status_code == 404:
            logging.error("File " + file_path + " not found at Tapatalk.")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            f.write(result.content)

print("Finished")
