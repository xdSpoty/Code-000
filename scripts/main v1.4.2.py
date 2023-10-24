"""
 * @date 24 Oktober 2023 - 02:00
 * @project Aniworld.to download script
 * @version 1.4.2
 * @author Spoty
"""

from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import youtube_dl
from rich.progress import ( BarColumn, Progress )
                            

hURL = input("Link: ")
st = int(input("Season: "))
ep = int(input("Episode: "))
lang = int(input("(1 = German, 2 = eng_sub, 3 = germ_sub) Language: "))
num = 0

with Progress("[progress.description]{task.description:>}",BarColumn(bar_width=None),"[progress.percentage]{task.percentage:>3.1f}%",) as progress:
    
    episode = progress.add_task("[cyan]Episode...", total=100)
    series = progress.add_task("[cyan]Season...", total=ep)
    
    while not progress.finished:

        for i in range(ep):
            num = num +1 
            URL = f'{hURL}/staffel-{st}/episode-{num}'
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            title = soup.find('title').text.strip()
            lang_key = soup.find_all("li", {"data-lang-key": lang})
            all_links = []
            

            for ahref in lang_key:
                href = ahref.get('data-link-target')
                all_links.append(href)
                    
            appa = f'https://aniworld.to{all_links[2]}'
                
            class MyLogger(object):
                def debug(self, msg):
                    pass

                def warning(self, msg):
                    pass

                def error(self, msg):
                    print(msg)


            def my_hook(d):
                if d['status'] == 'downloading':
                    percent = float(float(d['downloaded_bytes']) / float(d['total_bytes']) *100)
                    progress.update(episode, completed=percent)
                if d['status'] == 'finished':
                    progress.update(series, advance=1)

            ydl_opts = {
                'outtmpl': f'{title}.%(ext)s',
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f'{appa}'])
