import requests
from bs4 import BeautifulSoup
from html_analizer import extract
import persistence

for url in persistence.readURL():
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    results = extract(str(soup))
    print(results)
    persistence.writeResults(url,results)
