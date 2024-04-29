import requests
from bs4 import BeautifulSoup
import pandas as pd
import tqdm
import time
import random

base_url = "https://www.azlyrics.com"

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

def get_lyrics(url, save_txt=False, file_name=""):
    soup = getsoup(url)
    lyrics = soup.find("div", class_="ringtone").find_next_sibling("div").text
    if save_txt:        
        with open("lyrics/"+file_name+".txt", "w", encoding="utf-8") as archivo:
            archivo.write(lyrics)
    return lyrics

soup = getsoup(base_url+"/i/imaginedragons.html")

_album = ""
_year = ""
album = []
year = []
song_name = []
comments = []
file_name = []
url = []
lyric = []

rows = soup.find("div", id="listAlbum").find_all("div")
for row in tqdm.tqdm(rows):
      
    if row.get("class") == ["album"]:
        _album = row.find("b").text.strip('"')      
        if _album == "other songs:": 
            _year = None
        else:
            _year = row.contents[2].strip('( )')
        
        continue
    if row.get("class") == ["listalbum-item"]:
        #print("-"*50)
        #print(row.text)
        album.append(_album)
        year.append(_year) 
        _song_name = row.find('a').text.strip('" ')       
        song_name.append(_song_name)
        if row.find('div'):
            comments.append(row.find('div').text.strip('" '))
        else:
            comments.append(None)
        _filename = _song_name.replace(" ", "_").replace("/", "_").replace(":", "_").replace("!", "_")
        file_name.append(_filename)
        href = row.find("a").get("href")
        #print(href)
        # Si el href empieza con / es que es una url relativa
        if href.startswith("/"):
            _url = base_url+href
            
        else:
            _url = href
        url.append(_url)       
        
        lyric_raw = get_lyrics(_url, save_txt=True, file_name=_filename)
        # Quitar saltos de linea y espacios al principio y final
        lyric.append(lyric_raw.replace("\n", " ").strip())

        tqdm.tqdm.write(f"{_song_name} saved")
             
        time.sleep(random.randint(10, 15))
        

df = pd.DataFrame({"album": album, "year": year, "song_name": song_name, "url": url, "lyric": lyric, "file_name": file_name})
df.to_csv("songs.tsv", sep="\t", index=False, encoding="utf-8")
