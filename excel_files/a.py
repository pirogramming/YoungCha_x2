import requests
from bs4 import BeautifulSoup as BS

response = requests.get('https://www.youtube.com/watch?v=jyoqkm9tZ08')

html = response.text

soup = BS(html, 'html.parser')

for tag in soup.select('#description'):
    print(tag.text)
