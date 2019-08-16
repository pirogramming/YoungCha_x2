# TODO : 파일 제목을 보고 해당 기능을 추론하기 쉽지 않음
# TODO : 이름 알기 쉽게 붙이는게 좋음

import requests
from bs4 import BeautifulSoup as BS

response = requests.get('https://www.youtube.com/watch?v=jyoqkm9tZ08')

html = response.text

soup = BS(html, 'html.parser')

for tag in soup.select('#description'):
    print(tag.text)
