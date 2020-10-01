import requests
from bs4 import BeautifulSoup
from html_analizer import extract
import persistence
from phonenumberextractor import PhoneNumberExtractor


for url in persistence.readURL():
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')
    soup=str(soup)
    results = [extract(soup)]
    print(results)
    extractor = PhoneNumberExtractor()
    matches = extractor.extract_phone_numbers(soup)
    phones = ', '.join(matches)
    print(phones)
    results.append(phones)
    print(results)
    persistence.writeResults(url,results)
