from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json


class Scraper():
    def __init__(self, url):
        self.url = url

    def scrap_lyrics(self, song_url):
        print("Processing URL:", song_url)
        try:
            soup_data = self.invoke_page(song_url)

            song_name_div = soup_data.find("div", {"class": "banner-heading"})
            song_name = song_name_div.find("h1").text
            song_name = re.sub(r" [Ll]yrics", "", song_name)

            verses = soup_data.findAll("p", {"class": "verse"})
            lyrics = ""
            for verse in verses:
                lyrics += re.sub(r"<.*?>", "", str(verse)) + "\n"

            return {song_name: lyrics}

        except:
            print("Error opening the URL")

    def invoke_page(self, url):
        page = urlopen(url)
        html = BeautifulSoup(page, 'html.parser')

        return html

    def get_song_links(self, html):
        song_links = []
        index_div = html.find("div", {"class": "module", "id": "popular"})
        song_index = index_div.findAll("a", {"class": "title"})

        for song in song_index:
            song_links.append(song['href'])

        return song_links

    def scrap(self):
        song_links = []
        song_lyrics_list = []
        try:
            # Get landing page links
            html = self.invoke_page(self.url)
            song_links += self.get_song_links(html)

            # Get links from pagination block
            song_links += self.handle_pagination()

            #Get Lyrics for the links
            for song_link in song_links:
                lyrics = self.scrap_lyrics(song_link)
                song_lyrics_list.append(lyrics)

            return song_lyrics_list

        except:
            print("Error opening the URL")

    def handle_pagination(self):
        try:
            html = self.invoke_page(self.url)
            pagination_block = html.find("span", {"class": "pages"})
            song_links = []

            page_links = pagination_block.findAll("a")

            for page in page_links:
                page_url = page['href']
                html = self.invoke_page(page_url)
                songs = self.get_song_links(html)

                song_links += songs

            return song_links
        except:
            print("Error opening the URL")


data = Scraper('https://www.metrolyrics.com/katy-perry-lyrics.html').scrap()

with open('katy-perry-data.json', 'w') as file:
    json.dump(data, file)
