"""
 * @date 04 Oktober 2023 - 16:45
 * @project Aniworld.to download script
 * @version 1.1
 * @author Spoty
"""

import requests
from bs4 import BeautifulSoup
import youtube_dl


URL = input("Link: ")
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
title = soup.find('title').text.strip()


job_elements = soup.find_all("a", class_="watchEpisode")
all_links = []

for ahref in job_elements:
    href = ahref.get('href')
    href = href.strip()
    all_links.append(href)

appa = f'https://aniworld.to{all_links[2]}'

ydl_opts = {
    'outtmpl': f'{title}.%(ext)s'
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([f'{appa}'])