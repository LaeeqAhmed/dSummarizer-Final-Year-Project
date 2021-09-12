from bs4 import *
from requests import *
from imdb import IMDb
class Poster():
    def __init__(self, name, year):
        movie_name = name

        self.url = f"""https://www.imdb.com/find?q={movie_name.replace(" ", "+")}&ref_=nv_sr_sm"""

        page = get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.findAll('table', {"class": "findList"})
        anchor = table[0].findAll('a')

        self.url = f"""https://www.imdb.com{anchor[0]['href']}"""
        page = get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        links = soup.findAll(href=True)
        self.poster = links[11]

    def getPoster(self):
        return self.poster['href']

    def get_poster_link(self):
        return self.url.split("/")[4][2:]

    def getImage(self):
        ia = IMDb()
        the_matrix = ia.get_movie(self.get_poster_link())
        return the_matrix['full-size cover url']