import requests

url = 'https://www.azlyrics.com/lyrics/a1/bethefirsttobelieve.html'
response = requests.get(url)

from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, "lxml")

print(soup)

