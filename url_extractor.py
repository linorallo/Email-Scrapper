from urlextract import URLExtract
import requests
from bs4 import BeautifulSoup


url= "https://www.infovinos.es/bodegas"

extractor = URLExtract()
response=requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup=BeautifulSoup(response.text,'html.parser')
print(str(soup))
urls=extractor.find_urls(str(soup))
print(urls)