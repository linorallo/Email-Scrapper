import requests
from bs4 import BeautifulSoup
from html_analizer import extract
import persistence
from phonenumberextractor import PhoneNumberExtractor

i=0
for url in persistence.readURL():
    i+=1
    print(i)
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    soup=str(soup)
    results = [extract(soup)]
    extractor = PhoneNumberExtractor()
    matches = extractor.extract_phone_numbers(soup)
    phones = ', '.join(matches)
    results.append(phones)
    print(results)
    persistence.writeResults(url,results)
