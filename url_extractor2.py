from bs4 import BeautifulSoup
import requests
import re
import persistence

i = 0
for url in persistence.readURL():
    i +=1 
    print(i)
    html_page=requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(html_page.text,'html.parser')
    result_url = []
    for link in soup.findAll('a', attrs={'href': re.compile("^/")}):
        result_url.append('https://empresite.eleconomista.es'+str(link.get('href')))
    persistence.writeResults(url,result_url,i)