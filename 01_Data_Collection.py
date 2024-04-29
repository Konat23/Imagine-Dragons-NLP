import requests
from bs4 import BeautifulSoup
import pandas as pd

def getsoup(url):
        """Obtiene el soup de una pagina web con requests y beautifulsoup"""
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        return soup

def soup2htmlSave(soup, filname="lading.html"):
    html = soup.prettify()
    # Guardar Html de la pagina de grupos
    with open(filname, "w", encoding="utf-8") as archivo:
        archivo.write(html) 

soup = getsoup("https://www.azlyrics.com/i/imaginedragons.html")

_album = ""
_year = ""
album = []
year = []
song_name = []
url = []

rows = soup.find("div", id="listAlbum").find_all("div")
for row in rows:
      
    if row.get("class") == ["album"]:
        _album = row.find("b").text.strip('"')      
        if _album == "other songs:": 
            _year = None
        else:
            _year = row.contents[2].strip('()')
    else:
        album.append(_album)
        year.append(_year)
        song_name.append(row.text)
        url.append(row.get("href"))

df = pd.DataFrame({"album": album, "year": year, "song_name": song_name, "url": url})
df.to_csv("01_Data_Collection.csv", index=False)
