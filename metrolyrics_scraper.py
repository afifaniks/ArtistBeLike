from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


class Scraper():
    def __init__(self, url):
        self.url = url

    def scrap(self):
        try:
            page = urlopen(self.url)
            soup_data = BeautifulSoup(page, 'html.parser')
            verses = soup_data.findAll("p", {"class": "verse"})
            lyrics = ""

            for verse in verses:
                lyrics += re.sub(r"<.*?>", "", str(verse)) + "\n"

            return lyrics

        except:
            print("Error opening the URL")



Scraper('https://www.metrolyrics.com/feeling-myself-lyrics-nicki-minaj.html').scrap()
